# 15. ОБЪЕДИНИТЬ

**Где в типовой конфигурации:** CommonModules.БухгалтерскийУчетПереопределяемый, модуль, метод `ВсяОрганизация`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗРЕШЕННЫЕ
	Организации.Ссылка КАК Организация
ИЗ
	Справочник.Организации КАК Организации
ГДЕ
	Организации.ГоловнаяОрганизация = &Организация

ОБЪЕДИНИТЬ

ВЫБРАТЬ
	&Организация

УПОРЯДОЧИТЬ ПО
	Организация
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Организация = ВЫБРАТЬ ПЕРВЫЕ 1 Т.ГоловнаяОрганизация ИЗ Справочник.Организации КАК Т
```

## Что получилось в SQL

```sql
DECLARE @Organizaciya BINARY(16) = NULL; -- Организация

SELECT
  T1._IDRRef AS [Организация]
FROM dbo._Reference230 AS T1
WHERE T1._Fld5946RRef = @Organizaciya
UNION
SELECT
  @Organizaciya

ORDER BY [Организация]
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- ORDER BY applies to the whole union.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
