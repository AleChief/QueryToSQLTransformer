# 08. ВЫБОР КОГДА

**Где в типовой конфигурации:** CommonModules.БронированиеЛокализация, модуль, метод `ТекстЗапросаТаблицаОтражениеДокументовВРеглУчете`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ
	&Период КАК Период,
	&Организация КАК Организация,
	НАЧАЛОПЕРИОДА(ВЫБОР
					КОГДА &ДатаПрибытия < &Период
						ТОГДА &Период
					ИНАЧЕ &ДатаПрибытия
				КОНЕЦ, ДЕНЬ) КАК ДатаОтражения
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Период = 2018-01-01
ДатаПрибытия = 2018-02-15
Организация = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Ссылка ИЗ Справочник.Организации КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @DataPribytiya BINARY(16) = NULL; -- ДатаПрибытия
DECLARE @Organizaciya BINARY(16) = NULL; -- Организация
DECLARE @Period BINARY(16) = NULL; -- Период

SELECT DISTINCT
  @Period AS [Период],
  @Organizaciya AS [Организация],
  DATEADD(day, DATEDIFF(day, 0, CASE WHEN @DataPribytiya < @Period THEN @Period ELSE @DataPribytiya END), 0) AS [ДатаОтражения]
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
