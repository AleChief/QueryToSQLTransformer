# 26. АВТОУПОРЯДОЧИВАНИЕ

**Где в типовой конфигурации:** Catalogs.CompaniesBankAccounts, модуль менеджера, метод `ChoiceDataGetProcessing`

## Запрос на языке запросов 1С

```sql
SELECT ALLOWED
	Data.Ref
FROM
	Catalog.CompaniesBankAccounts AS Data
WHERE
	Data.Owner IN (&CompanyArray)
	AND &SearchCriteria_
	AND &OtherConditions

ORDER BY
	Data.Owner,
	Data.Description
AUTOORDER
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
CompanyArray = SELECT T.Ref FROM Catalog.Companies AS T
SearchCriteria_ = TRUE
OtherConditions = TRUE
```

## Что получилось в SQL

```sql
DECLARE @CompanyArray BINARY(16) = NULL; -- CompanyArray
DECLARE @OtherConditions BINARY(16) = NULL; -- OtherConditions
DECLARE @SearchCriteria_ BINARY(16) = NULL; -- SearchCriteria_

SELECT
  T1._IDRRef AS [Ref]
FROM dbo._Reference91 AS T1
WHERE T1._OwnerIDRRef IN(@CompanyArray)
  AND (@SearchCriteria_ = 0x01)
  AND (@OtherConditions = 0x01)
ORDER BY T1._OwnerIDRRef, T1._Description
```

## Предупреждения обработки

- AUTOORDER is ignored: the platform adds ordering by reference presentation there, and that happens outside the DBMS query. The rows come back in a different order.
- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
