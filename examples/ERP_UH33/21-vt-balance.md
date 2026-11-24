# 21. Виртуальная таблица остатков

**Где в типовой конфигурации:** Documents.СчетНаОплатуКлиенту, форма ФормаСозданияСчетовНаОплату, модуль формы, метод `ОбновитьСервер`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	РасчетыСКлиентами.ОплачиваетсяОстаток КАК Оплачивается
ИЗ
	РегистрНакопления.РасчетыСКлиентами.Остатки(, АналитикаУчетаПоПартнерам.Договор = &Договор) КАК РасчетыСКлиентами
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Договор = ВЫБРАТЬ ПЕРВЫЕ 1 Т.АналитикаУчетаПоПартнерам.Договор ИЗ РегистрНакопления.РасчетыСКлиентами КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Dogovor BINARY(16) = NULL; -- Договор

SELECT
  CAST(T1.[ОплачиваетсяBalance] AS NUMERIC(27, 2)) AS [Оплачивается]
FROM (
    SELECT COALESCE(Z.[ОплачиваетсяBalance], 0) AS [ОплачиваетсяBalance] FROM (
    SELECT
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37857 ELSE -VT._Fld37857 END), 0) AS [СуммаBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37858 ELSE -VT._Fld37858 END), 0) AS [КОплатеBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37859 ELSE -VT._Fld37859 END), 0) AS [ОплачиваетсяBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37860 ELSE -VT._Fld37860 END), 0) AS [КОтгрузкеBalance],
      ISNULL(SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37861 ELSE -VT._Fld37861 END), 0) AS [ОтгружаетсяBalance]
    FROM dbo._AccumRg37853 AS VT
      LEFT JOIN dbo._Reference181 AS TA1 ON TA1._IDRRef = VT._Fld37854RRef
    WHERE VT._Active = 0x01
      AND ((TA1._Fld45487_TYPE = 0x08 AND TA1._Fld45487_RRRef = @Dogovor))
    ) AS Z
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Balances: if you group the result further, add HAVING SUM(<balance>) <> 0 - otherwise rows that add up to zero appear, which 1C would not show.
- Field Договор is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
