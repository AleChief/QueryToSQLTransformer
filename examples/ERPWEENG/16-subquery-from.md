# 16. Вложенный запрос в источнике

**Где в типовой конфигурации:** Documents.ProductionStage2_2, модуль объекта, метод `CheckDetailsOfChainOfStages`

## Запрос на языке запросов 1С

```sql
SELECT
	TRUE
FROM
	(SELECT DISTINCT
		&SubstitutionText
	FROM
		Document.ProductionStage2_2 AS ChainStages
	WHERE
		ChainStages.ProductionLot = &ProductionLot
		AND NOT ChainStages.DeletionMark) AS T

HAVING
	COUNT(*) > 1
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
SubstitutionText = "x"
ProductionLot = SELECT TOP 1 T.ProductionLot FROM Document.ProductionStage2_2 AS T
```

## Тот же запрос в SQL

```sql
DECLARE @ProductionLot BINARY(16) = NULL; -- ProductionLot
DECLARE @SubstitutionText BINARY(16) = NULL; -- SubstitutionText

SELECT
  0x01 AS [Field1]
FROM (
SELECT DISTINCT
  @SubstitutionText AS [SubstitutionText]
FROM dbo._Document30199 AS TA1
WHERE TA1._Fld35292RRef = @ProductionLot
  AND NOT (TA1._Marked = 0x01)
  ) AS T1
HAVING CAST(COUNT_BIG(* ) AS NUMERIC(12, 0)) > 1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
