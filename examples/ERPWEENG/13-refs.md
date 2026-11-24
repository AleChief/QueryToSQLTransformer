# 13. ССЫЛКА и ТИПЗНАЧЕНИЯ

**Где в типовой конфигурации:** Catalogs.ControlledLots, модуль менеджера, метод `RegisterDataToProcessForMigrationToNewVersion`

## Запрос на языке запросов 1С

```sql
SELECT
	Lots.Ref AS Ref
FROM
	Catalog.ControlledLots AS Lots
WHERE
	NOT Lots.DeleteBusinessUnitProcessed
	AND NOT VALUETYPE(Lots.Lot) = TYPE(Document.RequestForGoodsQualityControl)
```

## Тот же запрос в SQL

```sql
SELECT
  T1._IDRRef AS [Ref]
FROM dbo._Reference43335 AS T1
WHERE NOT (T1._Fld43546 = 0x01)
  AND NOT (T1._Fld43531_TYPE + T1._Fld43531_RTRef) = 0x080000A97B
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
