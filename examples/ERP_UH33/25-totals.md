# 25. ИТОГИ

**Где в типовой конфигурации:** Reports.МониторБюджетныхПроцессов, модуль менеджера, метод `ЗаполнитьДиаграмму`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	ЭтапыПодготовкиБюджетов.Ссылка КАК Ссылка
ИЗ
	Справочник.ЭтапыПодготовкиБюджетов КАК ЭтапыПодготовкиБюджетов
ГДЕ
	ЭтапыПодготовкиБюджетов.Ссылка В(&Ссылки)
ИТОГИ ПО
	Ссылка ИЕРАРХИЯ
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Ссылки = ВЫБРАТЬ ПЕРВЫЕ 20 Т.Ссылка ИЗ Справочник.ЭтапыПодготовкиБюджетов КАК Т
```

## Что получилось в SQL

```sql
DECLARE @Ssylki BINARY(16) = NULL; -- Ссылки

SELECT
  T1._IDRRef AS [Ссылка]
FROM dbo._Reference140646 AS T1
WHERE T1._IDRRef IN(@Ssylki)
```

## Предупреждения обработки

- TOTALS is ignored: totals are post-processing done by the platform, there is no SQL counterpart. The SQL returns the detailed rows only.
- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
