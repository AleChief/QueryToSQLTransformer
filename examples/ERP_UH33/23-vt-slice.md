# 23. Срез последних и первых

**Где в типовой конфигурации:** Catalogs.ОбъектыЭксплуатации, модуль менеджера, метод `ВладелецУзлаКомпонентаАмортизации`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	УзлыКомпоненты.ОсновноеСредство КАК ОсновноеСредство
ИЗ
	РегистрСведений.УзлыКомпонентыАмортизации.СрезПоследних(&Период, УзелКомпонент = &УзелКомпонент) КАК УзлыКомпоненты
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Период = 2018-03-15
УзелКомпонент = ВЫБРАТЬ ПЕРВЫЕ 1 Т.УзелКомпонент ИЗ РегистрСведений.УзлыКомпонентыАмортизации КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Period DATETIME2 = NULL; -- Период
DECLARE @UzelKomponent BINARY(16) = NULL; -- УзелКомпонент

SELECT
  T1.[ОсновноеСредство] AS [ОсновноеСредство]
FROM (
    SELECT * FROM (
      SELECT
        VT._Fld1551 AS [ОбластьДанныхОсновныеДанные],
        VT._Fld171279RRef AS [ОсновноеСредство],
        VT._Fld171280 AS [ИдентификаторСтроки],
        VT._Fld171278RRef AS [УзелКомпонент],
        VT._Active AS [Активность],
        VT._LineNo AS [НомерСтроки],
        VT._RecorderRRef AS [Регистратор],
        VT._RecorderTRef AS [Регистратор_RTRef],
        VT._RecorderRRef AS [Регистратор_RRRef],
        VT._Period AS [Период]
        , ROW_NUMBER() OVER (PARTITION BY VT._Fld171278RRef ORDER BY VT._Period DESC, VT._RecorderTRef DESC, VT._RecorderRRef DESC, VT._LineNo DESC) AS SliceRowNumber
      FROM dbo._InfoRg171277 AS VT
      WHERE VT._Active = 0x01
        AND (@Period IS NULL OR @Period = CAST('2001-01-01 00:00:00' AS DATETIME2) OR VT._Period <= @Period)
        AND (VT._Fld171278RRef = @UzelKomponent)
    ) AS SliceRows WHERE SliceRowNumber = 1
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
