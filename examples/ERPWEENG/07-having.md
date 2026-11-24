# 07. ИМЕЮЩИЕ

**Где в типовой конфигурации:** Catalogs.BillsOfMaterials, форма ItemForm, модуль формы, метод `FillInServiceDetailsOfProductionProcess`

## Запрос на языке запросов 1С

```sql
SELECT TOP 1
	TRUE
FROM
	Catalog.ManufacturingOperations AS T
WHERE
	NOT T.DeletionMark
	AND T.BillOfMaterials = &BillOfMaterials
GROUP BY
	T.Owner

HAVING
	COUNT(DISTINCT T.Ref) > 1
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
BillOfMaterials = SELECT TOP 1 T.BillOfMaterials FROM Catalog.ManufacturingOperations AS T
```

## Тот же запрос в SQL

```sql
DECLARE @BillOfMaterials BINARY(16) = NULL; -- BillOfMaterials

SELECT TOP 1
  0x01 AS [Field1]
FROM dbo._Reference30093 AS T1
WHERE NOT (T1._Marked = 0x01)
  AND T1._Fld31571RRef = @BillOfMaterials
GROUP BY T1._OwnerID_TYPE, T1._OwnerID_RTRef, T1._OwnerID_RRRef
HAVING CAST(COUNT_BIG(DISTINCT T1._IDRRef ) AS NUMERIC(12, 0)) > 1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
