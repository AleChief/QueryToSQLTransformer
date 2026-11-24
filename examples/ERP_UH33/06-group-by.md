# 06. Группировка и агрегатные функции

**Где в типовой конфигурации:** InformationRegisters.ДополнительныеСведения, модуль набора записей, метод `ВсеОбъекты`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	ДополнительныеСведения.Объект КАК Объект
ИЗ
	РегистрСведений.ДополнительныеСведения КАК ДополнительныеСведения
ГДЕ
	&УсловиеОтбора

СГРУППИРОВАТЬ ПО
	ДополнительныеСведения.Объект
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
УсловиеОтбора = ИСТИНА
```

## Тот же запрос в SQL

```sql
DECLARE @UslovieOtbora BINARY(16) = NULL; -- УсловиеОтбора

SELECT
  T1._Fld31546_RRRef AS [Объект],
  T1._Fld31546_TYPE AS [Объект_TYPE],
  T1._Fld31546_RTRef AS [Объект_RTRef],
  T1._Fld31546_RRRef AS [Объект_RRRef]
FROM dbo._InfoRg31545 AS T1
WHERE (@UslovieOtbora = 0x01)
GROUP BY T1._Fld31546_TYPE, T1._Fld31546_RTRef, T1._Fld31546_RRRef
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
