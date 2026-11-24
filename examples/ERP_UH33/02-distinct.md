# 02. РАЗЛИЧНЫЕ

**Где в типовой конфигурации:** Catalogs.Номенклатура, модуль менеджера, метод `ЗаголовкиЭлементов`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ
	НоменклатураСегмента.Сегмент КАК Сегмент
ИЗ
	РегистрСведений.НоменклатураСегмента КАК НоменклатураСегмента
ГДЕ
	НоменклатураСегмента.Номенклатура = &Номенклатура
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Номенклатура = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Номенклатура ИЗ РегистрСведений.НоменклатураСегмента КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Nomenklatura BINARY(16) = NULL; -- Номенклатура

SELECT DISTINCT
  T1._Fld32788RRef AS [Сегмент]
FROM dbo._InfoRg32787 AS T1
WHERE T1._Fld32789RRef = @Nomenklatura
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
