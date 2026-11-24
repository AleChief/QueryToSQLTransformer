# 12. В ИЕРАРХИИ

**Где в типовой конфигурации:** Catalogs.ГруппыДоступаОрганизацииВидыОтчетов, форма ФормаЭлемента_Управляемая, модуль формы, метод `ЗаполнитьОрганизации`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	Организации.Ссылка КАК Организация
ИЗ
	Справочник.Организации КАК Организации
ГДЕ
	Организации.Ссылка В ИЕРАРХИИ(&Организация)
	И НЕ Организации.Ссылка В (&МассивИсключений)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Организация = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Ссылка ИЗ Справочник.Организации КАК Т
МассивИсключений = ВЫБРАТЬ ПЕРВЫЕ 2 Т.Ссылка ИЗ Справочник.Организации КАК Т УПОРЯДОЧИТЬ ПО Т.Наименование УБЫВ
```

## Тот же запрос в SQL

```sql
DECLARE @MassivIsklyucheniy BINARY(16) = NULL; -- МассивИсключений
DECLARE @Organizaciya BINARY(16) = NULL; -- Организация

WITH H1 AS (
  SELECT HA._IDRRef AS [Ref] FROM dbo._Reference230 AS HA
    WHERE HA._IDRRef IN (@Organizaciya)
  UNION ALL
  SELECT HB._IDRRef FROM dbo._Reference230 AS HB
    WHERE HB._ParentIDRRef IN (@Organizaciya)
  UNION ALL
  SELECT HC._IDRRef FROM dbo._Reference230 AS HC
    INNER JOIN H1 AS HP ON HC._ParentIDRRef = HP.[Ref]
)
SELECT
  T1._IDRRef AS [Организация]
FROM dbo._Reference230 AS T1
WHERE T1._IDRRef IN (SELECT [Ref] FROM H1 UNION ALL SELECT HV.[Ref] FROM (VALUES (@Organizaciya)) AS HV([Ref]) WHERE NOT EXISTS (SELECT 1 FROM H1))
  AND NOT T1._IDRRef IN(@MassivIsklyucheniy)
OPTION (MAXRECURSION 0)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
