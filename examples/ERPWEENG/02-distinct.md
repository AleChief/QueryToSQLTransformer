# 02. РАЗЛИЧНЫЕ

**Где в типовой конфигурации:** Catalogs.ExchangeMessageTransportSettings, модуль менеджера, метод `TransferTransportSettingsForExchangeScenarios`

## Запрос на языке запросов 1С

```sql
SELECT DISTINCT
	ExchangeSettings.Ref AS Ref
FROM
	Catalog.DataExchangeScenarios.ExchangeSettings AS ExchangeSettings
WHERE
	(CAST(ExchangeSettings.TransportID AS STRING(100))) = ""
```

## Тот же запрос в SQL

```sql
SELECT DISTINCT
  T1._Reference119_IDRRef AS [Ref]
FROM dbo._Reference119_VT13590 AS T1
WHERE (CAST(T1._Fld40724 AS NVARCHAR(100))) = N''
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
