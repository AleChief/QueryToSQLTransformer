# 08. ВЫБОР КОГДА

**Где в типовой конфигурации:** Catalogs.Assignments, модуль менеджера, метод `AddDescriptionOfYourOrders`

## Запрос на языке запросов 1С

```sql
SELECT ALLOWED
	CASE
		WHEN CAST(&ProductPrefix AS Catalog.Products).ItemsType = VALUE(Enum.ItemsTypes.Work_5)
			THEN &PrefixDivision
		ELSE &WarehousePrefix
	END AS Ref
INTO WarehouseParameterOverridable
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ProductPrefix = SELECT TOP 1 T.Ref FROM Catalog.Products AS T
PrefixDivision = "D"
WarehousePrefix = "W"
```

## Что получилось в SQL

```sql
DECLARE @PrefixDivision BINARY(16) = NULL; -- PrefixDivision
DECLARE @ProductPrefix BINARY(16) = NULL; -- ProductPrefix
DECLARE @WarehousePrefix BINARY(16) = NULL; -- WarehousePrefix

SELECT
  CASE WHEN T1._Fld16621RRef = 0xB1066855158DCB944EA9CADFE654EB8F THEN @PrefixDivision ELSE @WarehousePrefix END AS [Ref]
FROM (SELECT 1 AS [SDBL_DUMMY]) AS [SDBL_DUAL]
  LEFT JOIN dbo._Reference259 AS T1
    ON T1._IDRRef = @ProductPrefix
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has no final query; the result of the last temporary table "WarehouseParameterOverridable" is returned.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
