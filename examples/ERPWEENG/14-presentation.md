# 14. ПРЕДСТАВЛЕНИЕ ссылки

**Где в типовой конфигурации:** CommonForms.TransactionGLAccountsSettings, модуль, метод `AddDetailsElementsOfInternationalAccounting`

## Запрос на языке запросов 1С

```sql
SELECT ALLOWED
	ChartsOfAccounts.Ref AS Ref,
	REFPRESENTATION(ChartsOfAccounts.Ref) AS RefPresentation
FROM
	Catalog.FinancialAccountingChartsOfAccounts AS ChartsOfAccounts
WHERE
	NOT ChartsOfAccounts.DeletionMark
```

## Что получилось в SQL

```sql
SELECT
  T1._IDRRef AS [Ref],
  (CASE WHEN T1._IDRRef IS NULL THEN NULL ELSE COALESCE((CASE WHEN T2._Description = N'' THEN N'<>' ELSE T2._Description END), N'') END) AS [RefPresentation]
FROM dbo._Reference30072 AS T1
  LEFT JOIN dbo._Reference30072 AS T2
    ON T2._IDRRef = T1._IDRRef
WHERE NOT (T1._Marked = 0x01)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- PRESENTATION of Catalog.FinancialAccountingChartsOfAccounts returns the stored Description. If the configuration builds the presentation in the manager module, the platform shows something else.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
