# 18. Временные таблицы

**Где в типовой конфигурации:** CommonModules.ЭлектронныеДокументыЭДОСлужебный, модуль, метод `ТекстЗапросаСообщенийПоЭлектроннымДокументам`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	&СвойстваСообщения
ПОМЕСТИТЬ ИмяВременнойТаблицы
ИЗ
	Документ.СообщениеЭДО КАК СообщениеЭДО
ГДЕ
	СообщениеЭДО.ЭлектронныйДокумент В (&ИмяПараметраОтбора)
	И &УсловиеОтбора
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
СвойстваСообщения = "x"
ИмяПараметраОтбора = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Ссылка ИЗ Документ.РеализацияТоваровУслуг КАК Т
УсловиеОтбора = ИСТИНА
```

## Тот же запрос в SQL

```sql
DECLARE @ImyaParametraOtbora BINARY(16) = NULL; -- ИмяПараметраОтбора
DECLARE @SvoystvaSoobscheniya BINARY(16) = NULL; -- СвойстваСообщения
DECLARE @UslovieOtbora BINARY(16) = NULL; -- УсловиеОтбора

SELECT
  @SvoystvaSoobscheniya AS [СвойстваСообщения]
FROM dbo._Document167450 AS T1
WHERE (T1._Fld167693_TYPE = 0x08 AND T1._Fld167693_RRRef = @ImyaParametraOtbora)
  AND (@UslovieOtbora = 0x01)
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has no final query; the result of the last temporary table "ИмяВременнойТаблицы" is returned.
- Field ЭлектронныйДокумент is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
