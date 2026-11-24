# 05. Обращение через точку к реквизиту ссылки

**Где в типовой конфигурации:** Documents.ИсходящаяТранспортнаяОперацияВЕТИС, модуль менеджера, метод `ЗапросПроверкиВозможностиПеревозкиВРамкахРегионализацииXML`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ
	ЕСТЬNULL(Товары.Продукция.ВидПродукции.Идентификатор, "") КАК ВидПродукцииИдентификатор
ИЗ
	Документ.ИсходящаяТранспортнаяОперацияВЕТИС.Товары КАК Товары
ГДЕ
	Товары.Ссылка = &Ссылка
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Ссылка = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Ссылка ИЗ Документ.ИсходящаяТранспортнаяОперацияВЕТИС.Товары КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Ssylka BINARY(16) = NULL; -- Ссылка

SELECT DISTINCT
  COALESCE(T3._Fld124581, N'') AS [ВидПродукцииИдентификатор]
FROM dbo._Document124306_VT124872 AS T1
  LEFT JOIN dbo._Reference124298 AS T2
    ON T2._IDRRef = T1._Fld124875RRef
  LEFT JOIN dbo._Reference124298 AS T3
    ON T3._IDRRef = T2._Fld124587RRef
WHERE T1._Document124306_IDRRef = @Ssylka
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
