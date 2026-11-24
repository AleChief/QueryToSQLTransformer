# 19. Пакет запросов

**Где в типовой конфигурации:** CommonModules.ИнтеграцияИСМП, модуль, метод `СостояниеОбмена`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	1 КАК ОтправкаПолучениеДанныхИСМП
ПОМЕСТИТЬ ВТ_ОтправкаПолучениеДанныхИСМП
ГДЕ
	&ОтправкаПолучениеДанныхИСМП
;

////////////////////////////////////////////////////////////////////////////////
ВЫБРАТЬ
	ВТ_ОтправкаПолучениеДанныхИСМП.ОтправкаПолучениеДанныхИСМП
ИЗ
	ВТ_ОтправкаПолучениеДанныхИСМП КАК ВТ_ОтправкаПолучениеДанныхИСМП
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ОтправкаПолучениеДанныхИСМП = ИСТИНА
```

## Тот же запрос в SQL

```sql
DECLARE @OtpravkaPoluchenieDannyhISMP BINARY(16) = NULL; -- ОтправкаПолучениеДанныхИСМП

WITH [ВТ_ОтправкаПолучениеДанныхИСМП] AS (
SELECT
  CAST(1 AS NUMERIC(1, 0)) AS [ОтправкаПолучениеДанныхИСМП]

WHERE (@OtpravkaPoluchenieDannyhISMP = 0x01)
)
SELECT
  T1.[ОтправкаПолучениеДанныхИСМП] AS [ОтправкаПолучениеДанныхИСМП]
FROM [ВТ_ОтправкаПолучениеДанныхИСМП] AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
