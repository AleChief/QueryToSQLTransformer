# 22. Виртуальная таблица оборотов

**Где в типовой конфигурации:** Documents.ОперацияПоЯндексКассе, модуль объекта, метод `ОплаченоПоОбъектуРасчета`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	РасчетыСКлиентамиОбороты.СуммаРасход КАК СуммаРасход
ИЗ
	РегистрНакопления.РасчетыСКлиентами.Обороты(, &НаДату, , ОбъектРасчетов = &ОбъектРасчета) КАК РасчетыСКлиентамиОбороты
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
НаДату = 2030-01-01
ОбъектРасчета = ВЫБРАТЬ ПЕРВЫЕ 1 Т.ОбъектРасчетов ИЗ РегистрНакопления.РасчетыСКлиентами КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @NaDatu DATETIME2 = NULL; -- НаДату
DECLARE @ObektRascheta BINARY(16) = NULL; -- ОбъектРасчета

SELECT
  CAST(T1.[СуммаExpense] AS NUMERIC(21, 2)) AS [СуммаРасход]
FROM (
    SELECT Z.* FROM (
    SELECT
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37857 ELSE 0 END) AS [СуммаReceipt],
      SUM(CASE WHEN VT._RecordKind = 1 THEN VT._Fld37857 ELSE 0 END) AS [СуммаExpense],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37857 ELSE -VT._Fld37857 END) AS [СуммаTurnover],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37858 ELSE 0 END) AS [КОплатеReceipt],
      SUM(CASE WHEN VT._RecordKind = 1 THEN VT._Fld37858 ELSE 0 END) AS [КОплатеExpense],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37858 ELSE -VT._Fld37858 END) AS [КОплатеTurnover],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37859 ELSE 0 END) AS [ОплачиваетсяReceipt],
      SUM(CASE WHEN VT._RecordKind = 1 THEN VT._Fld37859 ELSE 0 END) AS [ОплачиваетсяExpense],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37859 ELSE -VT._Fld37859 END) AS [ОплачиваетсяTurnover],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37860 ELSE 0 END) AS [КОтгрузкеReceipt],
      SUM(CASE WHEN VT._RecordKind = 1 THEN VT._Fld37860 ELSE 0 END) AS [КОтгрузкеExpense],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37860 ELSE -VT._Fld37860 END) AS [КОтгрузкеTurnover],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37861 ELSE 0 END) AS [ОтгружаетсяReceipt],
      SUM(CASE WHEN VT._RecordKind = 1 THEN VT._Fld37861 ELSE 0 END) AS [ОтгружаетсяExpense],
      SUM(CASE WHEN VT._RecordKind = 0 THEN VT._Fld37861 ELSE -VT._Fld37861 END) AS [ОтгружаетсяTurnover]
    FROM dbo._AccumRg37853 AS VT
    WHERE VT._Active = 0x01
      AND VT._Period <= @NaDatu
      AND (VT._Fld160404RRef = @ObektRascheta)
    ) AS Z
    WHERE Z.[СуммаExpense] <> 0
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 2 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
