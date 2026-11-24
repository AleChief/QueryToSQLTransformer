# 21. Виртуальная таблица остатков

**Где в типовой конфигурации:** Documents.CustomerCommercialInvoice, форма CommercialInvoiceCreationForm, модуль формы, метод `RefreshServer`

## Запрос на языке запросов 1С

```sql
SELECT
	CustomersARAPAccounting.BeingPaidBalance AS BeingPaid
FROM
	AccumulationRegister.CustomersARAPAccounting.Balance(, AccountingDimensionByPartners.Contract = &Contract) AS CustomersARAPAccounting
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Contract = SELECT TOP 1 T.AccountingDimensionByPartners.Contract FROM AccumulationRegister.CustomersARAPAccounting AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Contract BINARY(16) = NULL; -- Contract

SELECT
  CAST(T1.[BeingPaidBalance] AS NUMERIC(27, 2)) AS [BeingPaid]
FROM (
    SELECT COALESCE(Z.[BeingPaidBalance], 0) AS [BeingPaidBalance] FROM (
    SELECT
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld24674 ELSE -VT._Fld24674 END), 0) AS [SumBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld24675 ELSE -VT._Fld24675 END), 0) AS [AmountDueBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld24676 ELSE -VT._Fld24676 END), 0) AS [BeingPaidBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld24677 ELSE -VT._Fld24677 END), 0) AS [ToShipBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld24678 ELSE -VT._Fld24678 END), 0) AS [BeingShippedBalance]
    FROM dbo._AccumRg24669 AS VT
      LEFT JOIN dbo._Reference124 AS TA1 ON TA1._IDRRef = VT._Fld24670RRef
    WHERE VT._Active = 0x01
      AND ((TA1._Fld13652_TYPE = 0x08 AND TA1._Fld13652_RRRef = @Contract))
    ) AS Z
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Balances: if you group the result further, add HAVING SUM(<balance>) <> 0 - otherwise rows that add up to zero appear, which 1C would not show.
- Field Contract is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
