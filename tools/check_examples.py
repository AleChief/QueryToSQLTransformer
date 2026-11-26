# -*- coding: utf-8 -*-
"""Проверка примеров на своей базе: каждый запрос переводится обработкой, исполняется в 1С и
в MS SQL, и результаты сверяются построчно.

Берёт все файлы `*.md` и `*.txt` из папки примеров (вложенные папки тоже), в том числе
добавленные вами:

- `.md` - запрос 1С из первого блока кода в разделе «Запрос на языке запросов 1С»;
  необязательные разделы «Пролог…» (запросы, создающие временные таблицы) и «Параметры»;
- `.txt` - весь файл и есть текст запроса 1С, без параметров.

Раздел «Параметры» - строки `Имя = значение`. Значение - литерал (`2018-01-01`,
`2018-01-01 10:30:00`, `10`, `1.5`, `ИСТИНА`, `ЛОЖЬ`, `"строка"`) или запрос 1С
(`ВЫБРАТЬ ПЕРВЫЕ 5 Ссылка ИЗ Справочник.Организации`), который выполняется в вашей базе:
одна строка результата - одно значение, несколько - список.

Подключение (аргументы или переменные окружения):

    --ib     строка соединения 1С: Srvr="сервер";Ref="база";  или  File="C:\\Base";   (Q2S_IB)
    --user   пользователь 1С (Q2S_IB_USER); пароль - Q2S_IB_PASSWORD или запрос при запуске
    --sql    строка ODBC к базе MS SQL этой же информационной базы (Q2S_SQL), например
             Driver={ODBC Driver 18 for SQL Server};Server=сервер;Database=база;
             Trusted_Connection=yes;TrustServerCertificate=yes
             пароль входа SQL, если он нужен, - Q2S_SQL_PASSWORD (в строку его не пишите)
    --bin    каталог bin платформы (Q2S_V8_BIN), если COM-коннектор не зарегистрирован
             или зарегистрирован от другой версии

    python tools\\check_examples.py --examples examples\\ERP_UH33

Нужно: Windows, Python 3.11+, pywin32, pyodbc; полные права пользователя 1С; одна свободная
лицензия (COM-соединение - это сеанс 1С). Пароли нигде не сохраняются.

Код возврата: 0 - расхождений нет, 1 - есть расхождение или ошибка исполнения.
"""
import argparse
import base64
import ctypes
import datetime
import decimal
import getpass
import os
import re
import sys
from ctypes import POINTER, byref, c_long, c_void_p
from ctypes.wintypes import BYTE, DWORD, WORD

import pyodbc
import pythoncom
import win32com.client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMPTY_REFERENCE = "0" * 32
NUMBER_TOLERANCE = decimal.Decimal("1e-6")


# ---------------------------------------------------------------------------
# Подключение к 1С по COM. Коннектор поднимается из comcntr.dll нужной версии: регистрация
# в реестре у всех версий платформы общая, и установка соседней версии её перезаписывает.
# ---------------------------------------------------------------------------

class GUID(ctypes.Structure):
    _fields_ = [("Data1", DWORD), ("Data2", WORD), ("Data3", WORD), ("Data4", BYTE * 8)]


def _guid(text):
    value = GUID()
    ctypes.oledll.ole32.CLSIDFromString(text, byref(value))
    return value


def connector(bin_dir):
    if not bin_dir or not os.path.isdir(bin_dir):
        return win32com.client.Dispatch("V83.COMConnector")
    os.add_dll_directory(bin_dir)
    library = ctypes.WinDLL(os.path.join(bin_dir, "comcntr.dll"))
    factory = c_void_p()
    result = library.DllGetClassObject(byref(_guid("{181E893D-73A4-4722-B61D-D604B3D67D47}")),
                                       byref(_guid("{00000001-0000-0000-C000-000000000046}")), byref(factory))
    if result != 0 or not factory.value:
        raise RuntimeError("comcntr.dll: DllGetClassObject 0x%08X" % (result & 0xFFFFFFFF))
    table = ctypes.cast(factory, POINTER(POINTER(c_void_p)))[0]
    create = ctypes.WINFUNCTYPE(c_long, c_void_p, c_void_p, POINTER(GUID), POINTER(c_void_p))(table[3])
    instance = c_void_p()
    result = create(factory, None, byref(_guid("{00020400-0000-0000-C000-000000000046}")), byref(instance))
    if result != 0 or not instance.value:
        raise RuntimeError("comcntr.dll: CreateInstance 0x%08X" % (result & 0xFFFFFFFF))
    return win32com.client.Dispatch(pythoncom.ObjectFromAddress(instance.value, pythoncom.IID_IDispatch))


def connection_string(base, user, password):
    text = base.strip()
    if not text.endswith(";"):
        text += ";"
    if user:
        text += 'Usr="%s";' % user.replace('"', '""')
    if password:
        text += 'P' + 'wd="%s";' % password.replace('"', '""')
    return text


def open_processor(ib, path):
    """Обработка через временный файл на стороне 1С: путь к ней сервер 1С может и не видеть."""
    with open(path, "rb") as stream:
        data = ib.Base64Value(base64.b64encode(stream.read()).decode("ascii"))
    target = ib.GetTempFileName("epf")
    data.Write(target)
    return ib.ExternalDataProcessors.Create(target, False)


# ---------------------------------------------------------------------------
# Файлы примеров
# ---------------------------------------------------------------------------

FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def sections(text):
    """Разделы markdown второго уровня: заголовок -> тело."""
    result = {}
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    for index in range(1, len(parts) - 1, 2):
        result[parts[index].strip()] = parts[index + 1]
    return result


def read_example(path):
    """(запрос, пролог, параметры-строки); запрос None - в файле его нет."""
    with open(path, encoding="utf-8-sig") as stream:
        text = stream.read()
    if path.lower().endswith(".txt"):
        return text.strip(), "", []
    parts = sections(text)
    query, prologue, parameters = None, "", []
    for title, body in parts.items():
        lowered = title.lower()
        block = FENCE.search(body)
        if query is None and ("языке запросов" in lowered or "query language" in lowered) and block:
            query = block.group(1).strip()
        elif lowered.startswith("пролог") or lowered.startswith("prologue"):
            prologue = "\n;\n".join(item.strip() for item in FENCE.findall(body))
        elif lowered.startswith("параметры") or lowered.startswith("parameters"):
            source = block.group(1) if block else body
            parameters = [line.strip() for line in source.splitlines()
                          if "=" in line and not line.strip().startswith(("#", "//", "-"))]
    return query, prologue, parameters


def parameter_value(ib, raw):
    """Значение параметра для 1С по тексту из раздела «Параметры»."""
    text = raw.strip()
    upper = text.upper()
    if upper.startswith(("ВЫБРАТЬ", "SELECT")):
        query = ib.NewObject("Query")
        query.Text = text
        table = query.Execute().Unload()
        if table.Count() == 0:
            raise LookupError("в базе нет данных для значения")
        if table.Count() == 1:
            return table.Get(0).Get(0)
        return table.UnloadColumn(0)
    if upper in ("ИСТИНА", "TRUE"):
        return True
    if upper in ("ЛОЖЬ", "FALSE"):
        return False
    if len(text) >= 2 and text[0] == text[-1] == '"':
        return text[1:-1].replace('""', '"')
    if re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", text):
        return ib.NewObject("UUID", text)
    for form in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            # Дата с поясом UTC доходит до 1С без сдвига: наивную pywin32 переводит из местного времени.
            return datetime.datetime.strptime(text, form).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            pass
    try:
        number = decimal.Decimal(text)
        return int(number) if number == number.to_integral_value() else float(number)
    except decimal.InvalidOperation:
        return text


def statements(text):
    """Запросы пакета: текст делится по `;` вне строк и комментариев."""
    parts, current, index, quoted = [], [], 0, False
    while index < len(text):
        char = text[index]
        if not quoted and text.startswith("//", index):
            end = text.find("\n", index)
            index = len(text) if end < 0 else end
            continue
        if char == '"':
            quoted = not quoted
        if char == ";" and not quoted:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
        index += 1
    parts.append("".join(current))
    return [part for part in parts if part.strip()]


PLACEMENT = re.compile(r"\b(?:ПОМЕСТИТЬ|INTO)\s+([^\s,;()]+)", re.I)
DROP = re.compile(r"^\s*(?:УНИЧТОЖИТЬ|DROP)\b", re.I)
TOTALS = re.compile(r"\b(?:ИТОГИ|TOTALS)\b.*$", re.I | re.S)


def result_statement(batch):
    """Номер запроса пакета, чей результат сверяется, и имя таблицы, если это ПОМЕСТИТЬ: последняя выборка
    без ПОМЕСТИТЬ, а если её нет - последняя созданная временная таблица (её и возвращает перевод)."""
    placed = None
    for number in range(len(batch) - 1, -1, -1):
        if DROP.search(batch[number]):
            continue
        found = PLACEMENT.search(batch[number])
        if not found:
            return number, None
        if placed is None:
            placed = (number, found.group(1))
    return placed if placed else (len(batch) - 1, None)


# ---------------------------------------------------------------------------
# Значения в общем виде
# ---------------------------------------------------------------------------

class Incomparable(object):
    """Значение, которое этой проверкой не сравнить (тип, хранилище, вложенная таблица)."""

    def __repr__(self):
        return "<несравнимо>"


INCOMPARABLE = Incomparable()


STORED_REFERENCE = re.compile(r"\d+:([0-9a-f]{32})\}$")
UUID_TEXT = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def stored_uuid(text):
    """Байты хранения уникального идентификатора: группы лежат в другом порядке, как у ссылки."""
    clean = text.replace("-", "")
    return clean[16:20] + clean[20:32] + clean[12:16] + clean[8:12] + clean[0:8]


def from_1c(ib, value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.rstrip()
    if isinstance(value, (int, float, decimal.Decimal)):
        return decimal.Decimal(str(value))
    if isinstance(value, datetime.datetime):
        # Пустую дату COM отдаёт годом 100.
        year = 1 if value.year == 100 else value.year
        return (year, value.month, value.day, value.hour, value.minute, value.second)
    # Ссылка любого вида, в том числе значение перечисления: во внутреннем представлении стоят её байты хранения
    # (`{"#",<тип>,345:819156e6…}`), их и даёт СУБД. Уникальный идентификатор - текстом.
    try:
        inner = str(ib.ValueToStringInternal(value))
    except Exception:
        return INCOMPARABLE
    found = STORED_REFERENCE.search(inner)
    if found:
        return ("ref", found.group(1))
    found = UUID_TEXT.search(inner.split(",")[-1]) if inner.startswith('{"#",') else None
    if found:
        return ("ref", stored_uuid(found.group(0)))
    return INCOMPARABLE


def from_sql(value, offset):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.rstrip()
    if isinstance(value, (int, float, decimal.Decimal)):
        return decimal.Decimal(str(value))
    if isinstance(value, datetime.datetime):
        if value.year == 1753 and offset == 0 and (value.month, value.day) == (1, 1):
            year = 1
        else:
            year = value.year - offset
        return (year, value.month, value.day, value.hour, value.minute, value.second)
    if isinstance(value, (bytes, bytearray)):
        if len(value) == 1:
            return value == b"\x01"
        if len(value) == 16:
            return ("ref", bytes(value).hex())
        return INCOMPARABLE
    return INCOMPARABLE


def composed(row, names, columns, offset):
    """Значение колонки 1С из колонок SQL: базовая колонка или части по тегу типа.

    Простую колонку даты обработка уже сдвигает сама (ShiftDates), смещение вычитается только из частей
    составного значения - их платформа, как и обработка, отдаёт в том виде, в каком они хранятся."""
    index = {name.upper(): position for position, name in enumerate(names)}
    result = []
    for name in columns:
        key = name.upper()
        tag_at = index.get(key + "_TYPE")
        if tag_at is None:
            at = index.get(key)
            result.append(INCOMPARABLE if at is None else from_sql(row[at], 0))
            continue
        tag = row[tag_at]
        if tag is None or bytes(tag) == b"\x01":
            result.append(None)
            continue
        role = {b"\x02": "_L", b"\x03": "_N", b"\x04": "_T", b"\x05": "_S", b"\x08": "_RRREF"}.get(bytes(tag))
        at = None if role is None else index.get(key + role)
        if at is None and role == "_RRREF":
            at = index.get(key)
        result.append(INCOMPARABLE if at is None else from_sql(row[at], offset))
    return result


def same(left, right):
    if isinstance(left, Incomparable) or isinstance(right, Incomparable):
        return True
    if isinstance(left, decimal.Decimal) and isinstance(right, decimal.Decimal):
        return abs(left - right) <= NUMBER_TOLERANCE * max(abs(left), abs(right), decimal.Decimal(1))
    if left is None and right == ("ref", EMPTY_REFERENCE) or right is None and left == ("ref", EMPTY_REFERENCE):
        return False
    return left == right


def sort_key(row):
    return [repr(item) if not isinstance(item, decimal.Decimal) else "%.6f" % item for item in row]


def compare(rows_1c, rows_sql, columns):
    """Пустая строка - совпало; иначе описание первого расхождения."""
    if len(rows_1c) != len(rows_sql):
        return "строк: 1С %d, SQL %d" % (len(rows_1c), len(rows_sql))
    left = sorted(rows_1c, key=sort_key)
    right = sorted(rows_sql, key=sort_key)
    for number, (row_1c, row_sql) in enumerate(zip(left, right), 1):
        for position, column in enumerate(columns):
            if not same(row_1c[position], row_sql[position]):
                return "строка %d, колонка %s: 1С %r, SQL %r" % (number, column, row_1c[position], row_sql[position])
    return ""


# ---------------------------------------------------------------------------
# Прогон
# ---------------------------------------------------------------------------

def year_offset(cursor):
    try:
        cursor.execute("SELECT TOP 1 [Offset] FROM [_YearOffset]")
        found = cursor.fetchone()
        if found is not None and found[0] is not None:
            return int(found[0])
    except pyodbc.Error:
        pass
    return 0


def check(ib, processor, cursor, offset, path):
    query_text, prologue, parameter_lines = read_example(path)
    if not query_text:
        return "пропущено", "в файле нет запроса 1С"

    values = {}
    for line in parameter_lines:
        name, raw = line.split("=", 1)
        try:
            values[name.strip().lstrip("&")] = parameter_value(ib, raw)
        except LookupError as error:
            return "пропущено", "параметр %s: %s" % (name.strip(), error)
        except Exception as error:
            return "ошибка", "параметр %s: %s" % (name.strip(), str(error).splitlines()[0][:200])
    full_text = (prologue + "\n;\n" + query_text) if prologue else query_text
    needed = [str(item) for item in processor.QueryParameterNames(full_text)]
    missing = [name for name in needed if name not in values]
    if missing:
        return "пропущено", "нет значений параметров: %s" % ", ".join(missing)

    options = processor.DefaultOptions()
    options.Insert("Dialect", "MSSQL")
    options.Insert("DateOffset", offset)
    options.Insert("ShiftDates", True)
    options.Insert("SubstituteParameters", True)
    options.Insert("Prologue", prologue)
    mapping = ib.NewObject("Map")
    for name, value in values.items():
        mapping.Insert(name, value)
    options.Insert("ParameterValues", mapping)
    result = processor.Transform(query_text, options)
    if not result.Success:
        return "отказ", str(result.ErrorDescription).strip().splitlines()[-1][:300]

    # ИТОГИ платформа строит после СУБД, перевод их не несёт - секция снимается и у 1С.
    batch = [TOTALS.sub("", item) for item in statements(full_text)]
    number, placed = result_statement(batch)
    if placed:
        batch.append("ВЫБРАТЬ * ИЗ " + placed)
        number = len(batch) - 1
    query = ib.NewObject("Query")
    query.Text = ";\n".join(batch)
    for name, value in values.items():
        query.SetParameter(name, value)
    try:
        table = query.ExecuteBatch().Get(number).Unload()
    except Exception as error:
        return "ошибка", "1С не выполнила запрос: %s" % str(error).splitlines()[0][:300]
    columns = [str(table.Columns.Get(index).Name) for index in range(table.Columns.Count())]
    rows_1c = [[from_1c(ib, table.Get(row).Get(col)) for col in range(len(columns))]
               for row in range(table.Count())]

    try:
        cursor.execute(str(result.SQL))
        while cursor.description is None and cursor.nextset():
            pass
        names = [item[0] for item in cursor.description]
        raw = cursor.fetchall()
    except pyodbc.Error as error:
        return "ошибка", "СУБД не выполнила SQL: %s" % str(error)[:300]
    rows_sql = [composed(row, names, columns, offset) for row in raw]

    difference = compare(rows_1c, rows_sql, columns)
    if difference:
        return "расходится", difference
    skipped = [column for position, column in enumerate(columns)
               if any(isinstance(row[position], Incomparable) for row in rows_1c + rows_sql)]
    note = "" if not skipped else "; не сравнивались: %s" % ", ".join(skipped)
    return ("совпало" if rows_1c else "совпало, пусто"), "строк %d%s" % (len(rows_1c), note)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--examples", default=os.path.join(ROOT, "examples"))
    parser.add_argument("--epf", default=os.path.join(ROOT, "build", "QueryToSQLTransformer.epf"))
    parser.add_argument("--ib", default=os.environ.get("Q2S_IB", ""))
    parser.add_argument("--user", default=os.environ.get("Q2S_IB_USER", ""))
    parser.add_argument("--sql", default=os.environ.get("Q2S_SQL", ""))
    parser.add_argument("--bin", default=os.environ.get("Q2S_V8_BIN", ""))
    parser.add_argument("--report", default="", help="файл отчёта .md (по умолчанию рядом с примерами)")
    arguments = parser.parse_args()
    if not arguments.ib or not arguments.sql:
        parser.error("нужны --ib и --sql (или переменные Q2S_IB и Q2S_SQL)")
    sys.stdout.reconfigure(encoding="utf-8")

    password = os.environ.get("Q2S_IB_PASSWORD")
    if password is None and arguments.user:
        password = getpass.getpass("Пароль пользователя 1С %s: " % arguments.user)
    sql_text = arguments.sql
    if os.environ.get("Q2S_SQL_PASSWORD") and "pwd=" not in sql_text.lower():
        sql_text = sql_text.rstrip(";") + ";P" + "WD={%s};" % os.environ["Q2S_SQL_PASSWORD"]

    files = []
    for folder, _, names in os.walk(arguments.examples):
        for name in sorted(names):
            if name.lower().endswith((".md", ".txt")) and name.lower() != "readme.md":
                files.append(os.path.join(folder, name))
    if not files:
        print("в %s нет файлов .md или .txt" % arguments.examples)
        return 1

    ib = connector(arguments.bin).Connect(connection_string(arguments.ib, arguments.user, password))
    try:
        processor = open_processor(ib, arguments.epf)
        connection = pyodbc.connect(sql_text, autocommit=True)
        cursor = connection.cursor()
        offset = year_offset(cursor)
        print("обработка %s, смещение дат базы %d, файлов %d" % (arguments.epf, offset, len(files)))
        outcomes = []
        for path in files:
            try:
                state, detail = check(ib, processor, cursor, offset, path)
            except Exception as error:
                state, detail = "ошибка", str(error).splitlines()[0][:300]
            label = os.path.relpath(path, arguments.examples)
            outcomes.append((label, state, detail))
            print("%-14s %s - %s" % (state, label, detail))
    finally:
        # Соединение отпускается здесь: иначе сеанс 1С остаётся висеть после выхода.
        processor = None
        ib = None

    totals = {}
    for _, state, _ in outcomes:
        totals[state] = totals.get(state, 0) + 1
    summary = ", ".join("%s %d" % item for item in sorted(totals.items()))
    print("итого: " + summary)
    report = arguments.report or os.path.join(arguments.examples, "check-report.md")
    with open(report, "w", encoding="utf-8") as stream:
        stream.write("# Проверка примеров\n\n%s\n\n| файл | итог | подробности |\n|---|---|---|\n" % summary)
        for label, state, detail in outcomes:
            stream.write("| %s | %s | %s |\n" % (label, state, detail.replace("|", "\\|")))
    print("отчёт: " + report)
    return 1 if totals.get("расходится") or totals.get("ошибка") else 0


if __name__ == "__main__":
    sys.exit(main())
