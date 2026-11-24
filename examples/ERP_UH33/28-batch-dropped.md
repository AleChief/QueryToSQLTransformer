# 28. Пакет с несколькими результатами

**Где в типовой конфигурации:** Documents.ЗаказКлиента, модуль менеджера, метод `ПередВыполнениемДействийВСпискеЗаказов`

Этот пример показывает **ограничение**. В пакете несколько запросов,
возвращающих результат, и в SQL попадает только последний — так же, как
`Запрос.Выполнить()` отдаёт результат только последнего запроса пакета.
Если нужны остальные выборки, переводите их по одной.

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	Таблица.Ссылка КАК Ссылка
ИЗ
	Документ.ЗаказКлиента КАК Таблица
ГДЕ
	Таблица.Ссылка В (&Заказы)
		И НЕ Таблица.ЭтоЗаказКакСчет
;
ВЫБРАТЬ
	Таблица.Ссылка КАК Ссылка
ИЗ
	Документ.ЗаказКлиента КАК Таблица
ГДЕ
	Таблица.Ссылка В (&Заказы)
	И Таблица.ЭтоЗаказКакСчет
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Заказы = ВЫБРАТЬ ПЕРВЫЕ 20 Т.Ссылка ИЗ Документ.ЗаказКлиента КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Zakazy BINARY(16) = NULL; -- Заказы

SELECT
  T1._IDRRef AS [Ссылка]
FROM dbo._Document572 AS T1
WHERE T1._IDRRef IN(@Zakazy)
  AND (T1._Fld188603 = 0x01)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has 2 queries returning a result. Only the last one is translated, the way Query.Execute() behaves; the earlier result sets are not in the SQL. Translate such queries separately if you need them.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
