# 03. ПЕРВЫЕ и УПОРЯДОЧИТЬ ПО

**Где в типовой конфигурации:** Catalogs.ВидыНалоговВзносов, модуль менеджера, метод `ПолучитьСсылкуПредопределенногоЭлемента`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ ПЕРВЫЕ 1
	ВидыНалоговВзносов.Ссылка КАК Ссылка
ИЗ
	Справочник.ВидыНалоговВзносов КАК ВидыНалоговВзносов
ГДЕ
	НРЕГ(ВидыНалоговВзносов.ИдентификаторЭлемента) = &Идентификатор
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Идентификатор = ВЫБРАТЬ ПЕРВЫЕ 1 НРЕГ(Т.ИдентификаторЭлемента) ИЗ Справочник.ВидыНалоговВзносов КАК Т ГДЕ Т.ИдентификаторЭлемента <> ""
```

## Тот же запрос в SQL

```sql
DECLARE @Identifikator NVARCHAR(500) = NULL; -- Идентификатор

SELECT TOP 1
  T1._IDRRef AS [Ссылка]
FROM dbo._Reference156588 AS T1
WHERE LOWER(T1._Fld204423) = @Identifikator
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
