# 20. УНИЧТОЖИТЬ

**Где в типовой конфигурации:** CommonModules.МобильноеПриложениеЗаказыКлиентовПереопределяемый, модуль, метод `РеализацияПоЗаказу`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ ПЕРВЫЕ 2
	РеализацияТоваровУслуг.Ссылка
ПОМЕСТИТЬ РТУ
ИЗ
	Документ.РеализацияТоваровУслуг КАК РеализацияТоваровУслуг
ГДЕ
	РеализацияТоваровУслуг.ЗаказКлиента = &ЗаказКлиента
	И РеализацияТоваровУслуг.Проведен

ОБЪЕДИНИТЬ ВСЕ

ВЫБРАТЬ РАЗЛИЧНЫЕ ПЕРВЫЕ 2
	РеализацияТоваровУслугТовары.Ссылка
ИЗ
	Документ.РеализацияТоваровУслуг.Товары КАК РеализацияТоваровУслугТовары
ГДЕ
	РеализацияТоваровУслугТовары.ЗаказКлиента = &ЗаказКлиента
;

////////////////////////////////////////////////////////////////////////////////
ВЫБРАТЬ РАЗЛИЧНЫЕ
	РТУ.Ссылка
ИЗ
	РТУ КАК РТУ
;

////////////////////////////////////////////////////////////////////////////////
УНИЧТОЖИТЬ РТУ
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ЗаказКлиента = ВЫБРАТЬ ПЕРВЫЕ 1 Т.ЗаказКлиента ИЗ Документ.РеализацияТоваровУслуг КАК Т ГДЕ Т.Проведен
```

## Тот же запрос в SQL

```sql
DECLARE @ZakazKlienta BINARY(16) = NULL; -- ЗаказКлиента

WITH [РТУ] AS (
SELECT DISTINCT TOP 2
  T1._IDRRef AS [Ссылка]
FROM dbo._Document769 AS T1
WHERE (T1._Fld26092_TYPE = 0x08 AND T1._Fld26092_RRRef = @ZakazKlienta)
  AND (T1._Posted = 0x01)
UNION ALL
SELECT DISTINCT TOP 2
  T1._Document769_IDRRef
FROM dbo._Document769_VT26149 AS T1
WHERE (T1._Fld26172_TYPE = 0x08 AND T1._Fld26172_RRRef = @ZakazKlienta)
)
SELECT DISTINCT
  T1.[Ссылка] AS [Ссылка]
FROM [РТУ] AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Field ЗаказКлиента is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
