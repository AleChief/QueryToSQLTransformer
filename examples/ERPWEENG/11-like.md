# 11. ПОДОБНО

**Где в типовой конфигурации:** CommonModules.Common, модуль, метод `DeleteVersionCacheRecords`

## Запрос на языке запросов 1С

```sql
SELECT
	CacheTable.Id AS Id,
	CacheTable.DataType AS DataType
FROM
	InformationRegister.ProgramInterfaceCache AS CacheTable
WHERE
	CacheTable.Id LIKE "%SearchSubstring%" ESCAPE "~"
```

## Тот же запрос в SQL

```sql
SELECT
  T1._Fld23322 AS [Id],
  T1._Fld23323RRef AS [DataType]
FROM dbo._InfoRg23321 AS T1
WHERE T1._Fld23322 LIKE N'%SearchSubstring%' ESCAPE N'~'
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
