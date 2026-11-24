# 09. ЕСТЬNULL

**Где в типовой конфигурации:** InformationRegisters.ЗаданияКРасчетуСтоимостиВНА, модуль менеджера, метод `НачалоРасчета`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	ЕСТЬNULL(МИНИМУМ(Задания.Месяц), ДАТАВРЕМЯ(1, 1, 1)) КАК НачалоРасчета
ИЗ
	РегистрСведений.ЗаданияКРасчетуСтоимостиВНА КАК Задания
ГДЕ
	Задания.Организация В (&СписокОрганизаций)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
СписокОрганизаций = ВЫБРАТЬ Т.Ссылка ИЗ Справочник.Организации КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @SpisokOrganizaciy BINARY(16) = NULL; -- СписокОрганизаций

SELECT
  COALESCE(MIN(T1._Fld114816), CAST('2001-01-01 00:00:00' AS DATETIME2)) AS [НачалоРасчета]
FROM dbo._InfoRg114815 AS T1
WHERE T1._Fld114817RRef IN(@SpisokOrganizaciy)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
