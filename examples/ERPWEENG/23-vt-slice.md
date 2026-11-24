# 23. Срез последних и первых

**Где в типовой конфигурации:** CommonModules.PartnerPricesFillingServer, модуль, метод `QueryTextsForFillingInPricesBatchProcessing`

## Запрос на языке запросов 1С

```sql
SELECT
	TableOfVATRates.VATRate AS VATRate
INTO PurchasePrices_BasicVATRates
FROM
	InformationRegister.BasicVATRates.SliceLast(&Date, Country = &RegistrationCountry) AS TableOfVATRates
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Date = 2030-01-01
RegistrationCountry = SELECT TOP 1 T.Country FROM InformationRegister.BasicVATRates AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Date DATETIME2 = NULL; -- Date
DECLARE @RegistrationCountry BINARY(16) = NULL; -- RegistrationCountry

SELECT
  T1.[VATRate] AS [VATRate]
FROM (
    SELECT * FROM (
      SELECT
        VT._Fld1035 AS [DataAreaMainData],
        VT._Fld21451RRef AS [VATRate],
        VT._Fld21450RRef AS [Country],
        VT._Period AS [Period]
        , ROW_NUMBER() OVER (PARTITION BY VT._Fld21450RRef ORDER BY VT._Period DESC) AS SliceRowNumber
      FROM dbo._InfoRg21449 AS VT
      WHERE (@Date IS NULL OR @Date = CAST('1753-01-01 00:00:00' AS DATETIME2) OR VT._Period <= @Date)
        AND (VT._Fld21450RRef = @RegistrationCountry)
    ) AS SliceRows WHERE SliceRowNumber = 1
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has no final query; the result of the last temporary table "PurchasePrices_BasicVATRates" is returned.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
