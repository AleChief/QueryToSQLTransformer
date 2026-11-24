# 12. В ИЕРАРХИИ

**Где в типовой конфигурации:** CommonModules.WarehousesServer, модуль, метод `ListOfSubordinateWarehouses`

## Запрос на языке запросов 1С

```sql
SELECT ALLOWED
	Warehouses.Ref
FROM
	Catalog.Warehouses AS Warehouses
WHERE
	Warehouses.Ref IN HIERARCHY(&Warehouse)
	AND (NOT Warehouses.IsFolder
			OR &ConditionForWarehouseGroup)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Warehouse = SELECT TOP 1 T.Ref FROM Catalog.Warehouses AS T
ConditionForWarehouseGroup = TRUE
```

## Что получилось в SQL

```sql
DECLARE @ConditionForWarehouseGroup BINARY(1) = NULL; -- ConditionForWarehouseGroup
DECLARE @Warehouse BINARY(16) = NULL; -- Warehouse

WITH H1 AS (
  SELECT HA._IDRRef AS [Ref] FROM dbo._Reference356 AS HA
    WHERE HA._IDRRef IN (@Warehouse)
  UNION ALL
  SELECT HB._IDRRef FROM dbo._Reference356 AS HB
    WHERE HB._ParentIDRRef IN (@Warehouse)
  UNION ALL
  SELECT HC._IDRRef FROM dbo._Reference356 AS HC
    INNER JOIN H1 AS HP ON HC._ParentIDRRef = HP.[Ref]
)
SELECT
  T1._IDRRef AS [Ref]
FROM dbo._Reference356 AS T1
WHERE T1._IDRRef IN (SELECT [Ref] FROM H1 UNION ALL SELECT HV.[Ref] FROM (VALUES (@Warehouse)) AS HV([Ref]) WHERE NOT EXISTS (SELECT 1 FROM H1))
  AND (NOT ((CASE WHEN T1._Folder = 0x00 THEN 0x01 WHEN NOT (T1._Folder = 0x00) THEN 0x00 END) = 0x01) OR (@ConditionForWarehouseGroup = 0x01))
OPTION (MAXRECURSION 0)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
