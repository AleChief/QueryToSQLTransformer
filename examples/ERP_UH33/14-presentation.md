# 14. ПРЕДСТАВЛЕНИЕ ссылки

**Где в типовой конфигурации:** Documents.ЗаявкаНаОбеспечение, форма ФормаДокумента, модуль формы, метод `НоменклатураСтрокой`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	Номенклатура.Ссылка КАК Номенклатура,
	ПРЕДСТАВЛЕНИЕ(Номенклатура.Ссылка) КАК НоменклатураСтрокой
ИЗ
	Справочник.Номенклатура КАК Номенклатура ГДЕ Ссылка В (&Номенклатура)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Номенклатура = ВЫБРАТЬ ПЕРВЫЕ 20 Т.Ссылка ИЗ Справочник.Номенклатура КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Nomenklatura BINARY(16) = NULL; -- Номенклатура

SELECT
  T1._IDRRef AS [Номенклатура],
  (CASE WHEN T1._IDRRef IS NULL THEN NULL ELSE COALESCE((CASE WHEN T2._Description = N'' THEN N'<>' ELSE T2._Description END), N'') END) AS [НоменклатураСтрокой]
FROM dbo._Reference215 AS T1
  LEFT JOIN dbo._Reference215 AS T2
    ON T2._IDRRef = T1._IDRRef
WHERE T1._IDRRef IN(@Nomenklatura)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- PRESENTATION of Справочник.Номенклатура returns the stored Наименование. If the configuration builds the presentation in the manager module, the platform shows something else.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
