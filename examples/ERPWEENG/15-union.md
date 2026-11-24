# 15. ОБЪЕДИНИТЬ

**Где в типовой конфигурации:** InformationRegisters.UsersInfo, модуль менеджера, метод `ResetOpenIDConnectAuthenticationForAllUsers`

## Запрос на языке запросов 1С

```sql
SELECT
	Users.Ref AS Ref,
	Users.IBUserID AS IBUserID
FROM
	Catalog.Users AS Users

UNION ALL

SELECT
	ExternalUsers.Ref,
	ExternalUsers.IBUserID
FROM
	Catalog.ExternalUsers AS ExternalUsers
```

## Тот же запрос в SQL

```sql
SELECT
  T1._IDRRef AS [Ref],
  0x08 AS [Ref_TYPE],
  0x00000159 AS [Ref_RTRef],
  T1._IDRRef AS [Ref_RRRef],
  T1._Fld18786 AS [IBUserID]
FROM dbo._Reference345 AS T1
UNION ALL
SELECT
  T1._IDRRef,
  0x08,
  0x0000008C,
  T1._IDRRef,
  T1._Fld13969
FROM dbo._Reference140 AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
