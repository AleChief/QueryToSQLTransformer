# 09. ЕСТЬNULL

**Где в типовой конфигурации:** InformationRegisters.JobsForUpdatingFixedAssetRecords, модуль менеджера, метод `CalculationStart`

## Запрос на языке запросов 1С

```sql
SELECT
	ISNULL(MIN(Jobs.Month), DATETIME(1, 1, 1)) AS CalculationStart
FROM
	InformationRegister.JobsForUpdatingFixedAssetRecords AS Jobs
WHERE
	Jobs.Organization IN (&CompaniesList)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
CompaniesList = SELECT T.Ref FROM Catalog.Companies AS T
```

## Тот же запрос в SQL

```sql
DECLARE @CompaniesList BINARY(16) = NULL; -- CompaniesList

SELECT
  COALESCE(MIN(T1._Fld40597), CAST('1753-01-01 00:00:00' AS DATETIME2)) AS [CalculationStart]
FROM dbo._InfoRg40596 AS T1
WHERE T1._Fld40598RRef IN(@CompaniesList)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
