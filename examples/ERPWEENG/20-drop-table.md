# 20. УНИЧТОЖИТЬ

**Где в типовой конфигурации:** CommonModules.MobileApplicationSalesOrdersOverridable, модуль, метод `CustomImplementation`

## Запрос на языке запросов 1С

```sql
SELECT DISTINCT TOP 2
	CustomerInvoice.Ref
INTO MOUTH
FROM
	Document.CustomerInvoice AS CustomerInvoice
WHERE
	CustomerInvoice.SalesOrder = &SalesOrder
	AND CustomerInvoice.Posted

UNION ALL

SELECT DISTINCT TOP 2
	SalesOfGoodsServicesGoods.Ref
FROM
	Document.CustomerInvoice.Goods AS SalesOfGoodsServicesGoods
WHERE
	SalesOfGoodsServicesGoods.SalesOrder = &SalesOrder
;

////////////////////////////////////////////////////////////////////////////////
SELECT DISTINCT
	MOUTH.Ref
FROM
	MOUTH AS MOUTH
;

////////////////////////////////////////////////////////////////////////////////
DROP MOUTH
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
SalesOrder = SELECT TOP 1 T.SalesOrder FROM Document.CustomerInvoice AS T WHERE T.Posted
```

## Тот же запрос в SQL

```sql
DECLARE @SalesOrder BINARY(16) = NULL; -- SalesOrder

WITH [MOUTH] AS (
SELECT DISTINCT TOP 2
  T1._IDRRef AS [Ref]
FROM dbo._Document402 AS T1
WHERE (T1._Fld3317_TYPE = 0x08 AND T1._Fld3317_RRRef = @SalesOrder)
  AND (T1._Posted = 0x01)
UNION ALL
SELECT DISTINCT TOP 2
  T1._Document402_IDRRef
FROM dbo._Document402_VT3390 AS T1
WHERE (T1._Fld3414_TYPE = 0x08 AND T1._Fld3414_RRRef = @SalesOrder)
)
SELECT DISTINCT
  T1.[Ref] AS [Ref]
FROM [MOUTH] AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Field SalesOrder is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
