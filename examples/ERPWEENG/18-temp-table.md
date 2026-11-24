# 18. Временные таблицы

**Где в типовой конфигурации:** Documents.GiftCertificateSale, модуль менеджера, метод `QueryTextTTTableAmountByPaymentCards`

## Запрос на языке запросов 1С

```sql
SELECT
	SUM(TabularSection.Sum) AS Sum
INTO TTTableAmountByPaymentCards
FROM
	Document.GiftCertificateSale.PaymentWithPaymentCards AS TabularSection
WHERE
	TabularSection.Ref = &Ref
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Ref = SELECT TOP 1 T.Ref FROM Document.GiftCertificateSale AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Ref BINARY(16) = NULL; -- Ref

SELECT
  CAST(SUM(T1._Fld4612 ) AS NUMERIC(21, 2)) AS [Sum]
FROM dbo._Document419_VT4608 AS T1
WHERE T1._Document419_IDRRef = @Ref
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has no final query; the result of the last temporary table "TTTableAmountByPaymentCards" is returned.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
