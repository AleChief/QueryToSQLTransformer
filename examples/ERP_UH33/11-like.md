# 11. ПОДОБНО

**Где в типовой конфигурации:** Catalogs.ГруппировкиТоварныхОграничений, модуль менеджера, метод `ИмяНовойГруппировкиПоУмолчанию`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	СпрГруппыНастроек.Наименование КАК Наименование
ИЗ
	Справочник.ГруппировкиТоварныхОграничений КАК СпрГруппыНастроек
ГДЕ
	СпрГруппыНастроек.Наименование ПОДОБНО &ШаблонИмени
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ШаблонИмени = "%"
```

## Тот же запрос в SQL

```sql
DECLARE @ShablonImeni NVARCHAR(500) = NULL; -- ШаблонИмени

SELECT
  T1._Description AS [Наименование]
FROM dbo._Reference48410 AS T1
WHERE T1._Description LIKE @ShablonImeni
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
