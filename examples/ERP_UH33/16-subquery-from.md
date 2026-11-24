# 16. Вложенный запрос в источнике

**Где в типовой конфигурации:** CommonModules.ОбработчикиОбновленияОПК, модуль, метод `СостояниеРегистровПараметровОПК`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	СУММА(Запрос.КолвоПОП) КАК КоличествоЗаписейПараметровОП
ИЗ
	(ВЫБРАТЬ
		КОЛИЧЕСТВО(*) КАК КолвоПОП
	ИЗ
		РегистрСведений.ПараметрыЛимитирования КАК ПараметрыЛимитирования) КАК Запрос
```

## Тот же запрос в SQL

```sql
SELECT
  CAST(SUM(T1.[КолвоПОП] ) AS NUMERIC(18, 0)) AS [КоличествоЗаписейПараметровОП]
FROM (
SELECT
  CAST(COUNT_BIG(* ) AS NUMERIC(12, 0)) AS [КолвоПОП]
FROM dbo._InfoRg193878 AS TA1
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
