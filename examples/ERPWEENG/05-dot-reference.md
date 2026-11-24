# 05. Обращение через точку к реквизиту ссылки

**Где в типовой конфигурации:** CommonModules.DiscountsMarkupsServer, модуль, метод `ApplyCalculationResultForBonusPoints`

## Запрос на языке запросов 1С

```sql
SELECT
	ISNULL(LoyaltyCards.Owner.LoyaltyProgram.DoNotAccruePointsWhenPayingWithBonuses, FALSE) AS DoNotAccruePointsWhenPayingWithBonuses
FROM
	Catalog.LoyaltyCards AS LoyaltyCards
WHERE
	LoyaltyCards.Ref = &LoyaltyCard
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
LoyaltyCard = SELECT TOP 1 T.Ref FROM Catalog.LoyaltyCards AS T
```

## Тот же запрос в SQL

```sql
DECLARE @LoyaltyCard BINARY(16) = NULL; -- LoyaltyCard

SELECT
  COALESCE(T3._Fld15291, 0x00) AS [DoNotAccruePointsWhenPayingWithBonuses]
FROM dbo._Reference198 AS T1
  LEFT JOIN dbo._Reference197 AS T2
    ON T2._IDRRef = T1._OwnerIDRRef
  LEFT JOIN dbo._Reference199 AS T3
    ON T3._IDRRef = T2._Fld15260RRef
WHERE T1._IDRRef = @LoyaltyCard
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
