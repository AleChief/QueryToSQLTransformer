# 13. ССЫЛКА и ТИПЗНАЧЕНИЯ

**Где в типовой конфигурации:** DataProcessors.РаботаСФайлами, форма СписокЗанятыхСВопросом, модуль формы, метод `НастроитьДинамическийСписок`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗРЕШЕННЫЕ РАЗЛИЧНЫЕ
	ТИПЗНАЧЕНИЯ(СведенияОФайлах.Файл) КАК ТипФайла
ИЗ
	РегистрСведений.СведенияОФайлах КАК СведенияОФайлах
ГДЕ
	СведенияОФайлах.Редактирует = &Редактирует
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Редактирует = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Редактирует ИЗ РегистрСведений.СведенияОФайлах КАК Т
```

## Что получилось в SQL

```sql
DECLARE @Redaktiruet BINARY(16) = NULL; -- Редактирует

SELECT DISTINCT
  (T1._Fld115246_TYPE + T1._Fld115246_RTRef) AS [ТипФайла]
FROM dbo._InfoRg115245 AS T1
WHERE (T1._Fld115257_TYPE = 0x08 AND T1._Fld115257_RRRef = @Redaktiruet)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- ALLOWED is ignored: record level security is not applied, the SQL returns every row.
- Field Редактирует is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
