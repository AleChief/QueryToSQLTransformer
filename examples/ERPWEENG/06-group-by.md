# 06. Группировка и агрегатные функции

**Где в типовой конфигурации:** CommonModules.ObjectsVersioning, модуль, метод `OnCollectConfigurationStatisticsParameters`

## Запрос на языке запросов 1С

```sql
SELECT
	VALUETYPE(ObjectsVersions.Object) AS ObjectType,
	COUNT(1) AS Count
FROM
	InformationRegister.ObjectsVersions AS ObjectsVersions

GROUP BY
	VALUETYPE(ObjectsVersions.Object)
```

## Тот же запрос в SQL

```sql
SELECT
  (T1._Fld23057_TYPE + T1._Fld23057_RTRef) AS [ObjectType],
  CAST(COUNT_BIG(1 ) AS NUMERIC(12, 0)) AS [Count]
FROM dbo._InfoRg23056 AS T1
GROUP BY (T1._Fld23057_TYPE + T1._Fld23057_RTRef)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
