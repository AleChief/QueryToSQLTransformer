# 29. Чужая временная таблица и пролог

**Где в типовой конфигурации:** CommonForms.AccessRights, модуль, метод `OutputAccessGroups`

Сам по себе этот запрос не переводится — он читает временную таблицу,
которую создаёт другой запрос того же метода:

```
{ExternalDataProcessor.QueryToSQLTransformer.ObjectModule(745)}: AllowedAccessGroups is a temporary table that some other query creates - this text does not create it itself. Paste the query that fills AllowedAccessGroups into the "Missing queries" field above and translate again.
```

Это не предел транслятора, а недостающий контекст. Текст, создающий таблицу,
передаётся настройкой `Prologue` — и запрос переводится.

## Пролог: запрос, создающий временную таблицу

```sql
SELECT ALLOWED
	AccessGroups.Ref
INTO AllowedAccessGroups
FROM
	Catalog.AccessGroups AS AccessGroups
```

## Запрос на языке запросов 1С

```sql
SELECT
	AllowedAccessGroups.Ref
FROM
	AllowedAccessGroups AS AllowedAccessGroups
WHERE
	(NOT AllowedAccessGroups.Ref.DeletionMark)
	AND (NOT AllowedAccessGroups.Ref.Profile.DeletionMark)
```

## Что получилось в SQL

```sql
WITH [AllowedAccessGroups] AS (
SELECT
  T1._IDRRef AS [Ref]
FROM dbo._Reference47 AS T1
)
SELECT
  T1.[Ref] AS [Ref]
FROM [AllowedAccessGroups] AS T1
  LEFT JOIN dbo._Reference47 AS T2
    ON T2._IDRRef = T1.[Ref]
  LEFT JOIN dbo._Reference46 AS T3
    ON T3._IDRRef = T2._Fld11439RRef
WHERE NOT (T2._Marked = 0x01)
  AND NOT (T3._Marked = 0x01)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
