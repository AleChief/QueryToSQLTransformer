# 04. Соединения таблиц

**Где в типовой конфигурации:** InformationRegisters.SegmentProducts, форма ProductSegmentsParameter, модуль формы, метод `DetermineUseOfCharacteristics`

## Запрос на языке запросов 1С

```sql
SELECT
	ItemKinds.UseCharacteristics
FROM
	Catalog.Products AS Products
		INNER JOIN Catalog.ItemKinds AS ItemKinds
		ON Products.ProductKind = ItemKinds.Ref
WHERE
	Products.Ref = &Products
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Products = SELECT TOP 1 T.Ref FROM Catalog.Products AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Products BINARY(16) = NULL; -- Products

SELECT
  T2._Fld14722 AS [UseCharacteristics]
FROM dbo._Reference259 AS T1
  INNER JOIN dbo._Reference177 AS T2
    ON T1._Fld16589RRef = T2._IDRRef
WHERE T1._IDRRef = @Products
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
