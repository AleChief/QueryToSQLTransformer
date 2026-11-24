# 19. Пакет запросов

**Где в типовой конфигурации:** CommonModules.TMPeripheralsServerCall, модуль, метод `CashRegisterRelatedToEquipment`

## Запрос на языке запросов 1С

```sql
SELECT
	T.Ref AS Ref
INTO SettingUpTheRMK
FROM
	Catalog.CWPSettings AS T
WHERE
	T.Workplace = &Workplace

;
SELECT TOP 1
   CashAccounts.CashAccount AS CashAccount
FROM
	Catalog.CWPSettings.CashAccounts AS CashAccounts
		INNER JOIN SettingUpTheRMK AS SettingUpTheRMK
		ON SettingUpTheRMK.Ref = CashAccounts.Ref
WHERE
	CashAccounts.Peripherals = &CREEquipment
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Workplace = SELECT TOP 1 T.Workplace FROM Catalog.CWPSettings AS T
CREEquipment = SELECT TOP 1 T.Peripherals FROM Catalog.CWPSettings.CashAccounts AS T
```

## Тот же запрос в SQL

```sql
DECLARE @CREEquipment BINARY(16) = NULL; -- CREEquipment
DECLARE @Workplace BINARY(16) = NULL; -- Workplace

WITH [SettingUpTheRMK] AS (
SELECT
  T1._IDRRef AS [Ref]
FROM dbo._Reference114 AS T1
WHERE T1._Fld13476RRef = @Workplace
)
SELECT TOP 1
  T1._Fld13482RRef AS [CashAccount]
FROM dbo._Reference114_VT13480 AS T1
  INNER JOIN [SettingUpTheRMK] AS T2
    ON T2.[Ref] = T1._Reference114_IDRRef
WHERE T1._Fld13483RRef = @CREEquipment
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
