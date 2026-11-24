# 10. ВЫРАЗИТЬ

**Где в типовой конфигурации:** DataProcessors.СверткаИнформационнойБазы, модуль объекта, метод `ОбработатьДокументыДоступностьРабочихЦентров`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ
	Регистратор КАК Ссылка
ИЗ РегистрСведений.ДоступностьРабочихЦентров
ГДЕ Окончание > &ДатаОст И ВЫРАЗИТЬ(Регистратор КАК Документ.ДоступностьРабочихЦентров).Дата <= &ДатаОст
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ДатаОст = 2018-01-01
```

## Тот же запрос в SQL

```sql
DECLARE @DataOst DATETIME2 = NULL; -- ДатаОст

SELECT DISTINCT
  T1._RecorderRRef AS [Ссылка],
  T1._RecorderTRef AS [Ссылка_RTRef],
  T1._RecorderRRef AS [Ссылка_RRRef]
FROM dbo._InfoRg42509 AS T1
  LEFT JOIN dbo._Document565 AS T2
    ON T1._RecorderTRef = 0x00000235 AND T2._IDRRef = T1._RecorderRRef
WHERE T1._Fld42512 > @DataOst
  AND T2._Date_Time <= @DataOst
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
