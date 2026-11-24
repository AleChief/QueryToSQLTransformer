# 17. Вложенный запрос в условии

**Где в типовой конфигурации:** CommonModules.MobileWarehouseKeeperWorkspace, модуль, метод `FindAmbiguousIBUsers`

## Запрос на языке запросов 1С

```sql
SELECT
	Users.IBUserID AS AmbiguousID
FROM
	Catalog.Users AS Users
WHERE
	Users.IBUserID IN
			(SELECT
				CatalogUsers.IBUserID
			FROM
				Catalog.Users AS CatalogUsers
			WHERE
				CatalogUsers.Ref = &User
				AND CatalogUsers.IBUserID <> &BlankUUID)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
User = SELECT TOP 1 T.Ref FROM Catalog.Users AS T
BlankUUID = 00000000-0000-0000-0000-000000000000
```

## Тот же запрос в SQL

```sql
DECLARE @BlankUUID BINARY(16) = NULL; -- BlankUUID
DECLARE @User BINARY(16) = NULL; -- User

SELECT
  T1._Fld18786 AS [AmbiguousID]
FROM dbo._Reference345 AS T1
WHERE T1._Fld18786 IN(
SELECT
  TA1._Fld18786 AS [IBUserID]
FROM dbo._Reference345 AS TA1
WHERE TA1._IDRRef = @User
  AND TA1._Fld18786 <> @BlankUUID
)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
