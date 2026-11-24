# 03. ПЕРВЫЕ и УПОРЯДОЧИТЬ ПО

**Где в типовой конфигурации:** CommonModules.InteractionsEvents, модуль, метод `OnWriteEmailAccount`

## Запрос на языке запросов 1С

```sql
SELECT TOP 1
	EmailMessageFolders.Ref
FROM
	Catalog.EmailMessageFolders AS EmailMessageFolders
WHERE
	EmailMessageFolders.PredefinedFolder
	AND EmailMessageFolders.Owner = &Account
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Account = SELECT TOP 1 T.Owner FROM Catalog.EmailMessageFolders AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Account BINARY(16) = NULL; -- Account

SELECT TOP 1
  T1._IDRRef AS [Ref]
FROM dbo._Reference135 AS T1
WHERE (T1._Fld13902 = 0x01)
  AND T1._OwnerIDRRef = @Account
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
