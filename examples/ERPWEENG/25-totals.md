# 25. ИТОГИ

**Где в типовой конфигурации:** DataProcessors.VendorPriceLists, форма FormSettings, модуль формы, метод `InitializePartnerProductHierarchyTree`

## Запрос на языке запросов 1С

```sql
SELECT
	T.Ref AS Ref,
	T.Description AS Description,
	FALSE AS Selected
FROM
	Catalog.ProductCrossReferences AS T
WHERE
	T.IsFolder
	AND T.Owner = &Partner
TOTALS BY
	Ref HIERARCHY
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Partner = SELECT TOP 1 T.Owner FROM Catalog.ProductCrossReferences AS T
```

## Что получилось в SQL

```sql
DECLARE @Partner BINARY(16) = NULL; -- Partner

SELECT
  T1._IDRRef AS [Ref],
  T1._Description AS [Description],
  0x00 AS [Selected]
FROM dbo._Reference256 AS T1
WHERE ((CASE WHEN T1._Folder = 0x00 THEN 0x01 WHEN NOT (T1._Folder = 0x00) THEN 0x00 END) = 0x01)
  AND T1._OwnerIDRRef = @Partner
```

## Предупреждения обработки

- TOTALS is ignored: totals are post-processing done by the platform, there is no SQL counterpart. The SQL returns the detailed rows only.
- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
