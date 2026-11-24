# 17. Вложенный запрос в условии

**Где в типовой конфигурации:** Catalogs.ШаблоныАнкет, форма ФормаЭлемента, модуль формы, метод `ОпределитьЕстьЛиДанномуШаблонуАнкеты`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ ПЕРВЫЕ 1
	Анкета.Ссылка
ИЗ
	Документ.Анкета КАК Анкета
ГДЕ
	(НЕ Анкета.ПометкаУдаления)
	И Анкета.Опрос В
			(ВЫБРАТЬ
				НазначениеОпросов.Ссылка
			ИЗ
				Документ.НазначениеОпросов КАК НазначениеОпросов
			ГДЕ
				НазначениеОпросов.ШаблонАнкеты = &ШаблонАнкеты)
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ШаблонАнкеты = ВЫБРАТЬ ЗНАЧЕНИЕ(Справочник.ШаблоныАнкет.ПустаяСсылка)
```

## Тот же запрос в SQL

```sql
DECLARE @ShablonAnkety BINARY(16) = NULL; -- ШаблонАнкеты

SELECT TOP 1
  T1._IDRRef AS [Ссылка]
FROM dbo._Document515 AS T1
WHERE NOT (T1._Marked = 0x01)
  AND T1._Fld12408RRef IN(
SELECT
  TA1._IDRRef AS [Ссылка]
FROM dbo._Document638 AS TA1
WHERE TA1._Fld19161RRef = @ShablonAnkety
)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
