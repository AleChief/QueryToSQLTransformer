# 27. Параметры запроса

**Где в типовой конфигурации:** Catalogs.DiscountsMarkups, форма SettingOfValidityStatus, модуль формы, метод `CustomizeForm`

## Запрос на языке запросов 1С

```sql
SELECT
	MIN(T.Period) AS Period
FROM
	InformationRegister.ValidityOfDiscountsMarkups AS T
WHERE
	T.Period > &StartDate
	AND T.Source IN (&Sources)
	AND T.DiscountMarkup IN (&Table)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
StartDate = 2000-01-01
Sources = SELECT DISTINCT TOP 20 T.Source FROM InformationRegister.ValidityOfDiscountsMarkups AS T
Table = SELECT DISTINCT TOP 20 T.DiscountMarkup FROM InformationRegister.ValidityOfDiscountsMarkups AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Sources BINARY(16) = NULL; -- Sources
DECLARE @StartDate DATETIME2 = NULL; -- StartDate
DECLARE @Table BINARY(16) = NULL; -- Table

SELECT
  MIN(T1._Period) AS [Period]
FROM dbo._InfoRg24179 AS T1
WHERE T1._Period > @StartDate
  AND (T1._Fld24180_TYPE = 0x08 AND T1._Fld24180_RRRef = @Sources)
  AND T1._Fld24181RRef IN(@Table)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Field Source is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
