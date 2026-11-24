# 24. Виртуальные таблицы бухрегистра

**Где в типовой конфигурации:** Reports.ВыверкаТрансляцииПроводок, форма ФормаОтчета, модуль формы, метод `ДополнитьТаблицуДанныхПараллельныйУчет`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	СУММА(ТабИсходныеДанные.Сумма) КАК Сумма	                        
ИЗ
	РегистрБухгалтерии.Хозрасчетный.ДвиженияССубконто(&ДатаНач, &ДатаКон, Активность И Организация=&Организация И СчетДт.Код=&Счет И СчетКт.Код=&КоррСчет, , ) КАК ТабИсходныеДанные
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
ДатаНач = 2017-01-01
ДатаКон = 2017-12-31
Организация = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Организация ИЗ РегистрБухгалтерии.Хозрасчетный КАК Т
Счет = "60.01"
КоррСчет = "51"
```

## Тот же запрос в SQL

```sql
DECLARE @DataKon DATETIME2 = NULL; -- ДатаКон
DECLARE @DataNach DATETIME2 = NULL; -- ДатаНач
DECLARE @KorrSchet NVARCHAR(500) = NULL; -- КоррСчет
DECLARE @Organizaciya BINARY(16) = NULL; -- Организация
DECLARE @Schet NVARCHAR(500) = NULL; -- Счет

SELECT
  CAST(SUM(T1.[Сумма] ) AS NUMERIC(21, 2)) AS [Сумма]
FROM (
  SELECT
    VT._Fld1551 AS [ОбластьДанныхОсновныеДанные],
    VT._Fld160925 AS [Сторно],
    VT._Fld117621 AS [СуммаУУ],
    VT._Fld1604Ct AS [СуммаВРКт],
    VT._Fld1603Ct AS [СуммаПРКт],
    VT._Fld1606 AS [НеКорректироватьСтоимостьАвтоматически],
    VT._Fld1603Dt AS [СуммаПРДт],
    VT._Fld1604Dt AS [СуммаВРДт],
    VT._Fld1601Ct AS [КоличествоКт],
    VT._Fld1601Dt AS [КоличествоДт],
    VT._Fld1600Ct AS [ВалютнаяСуммаКт],
    VT._Fld1602Ct AS [СуммаНУКт],
    VT._Fld1599 AS [Сумма],
    VT._Fld1597DtRRef AS [ВалютаДт],
    VT._Fld1598DtRRef AS [ПодразделениеДт],
    VT._Fld1596RRef AS [Организация],
    VT._Fld1597CtRRef AS [ВалютаКт],
    VT._Fld1600Dt AS [ВалютнаяСуммаДт],
    VT._AccountCtRRef AS [СчетКт],
    VT._Fld1598CtRRef AS [ПодразделениеКт],
    VT._AccountDtRRef AS [СчетДт],
    VT._Active AS [Активность],
    VT._Fld1602Dt AS [СуммаНУДт],
    VT._LineNo AS [НомерСтроки],
    VT._Fld117622 AS [СуммаФО],
    VT._Fld52242DtRRef AS [НаправлениеДеятельностиДт],
    VT._RecorderRRef AS [Регистратор],
    VT._RecorderTRef AS [Регистратор_RTRef],
    VT._RecorderRRef AS [Регистратор_RRRef],
    VT._Fld1605 AS [Содержание],
    VT._Period AS [Период],
    VT._Fld52242CtRRef AS [НаправлениеДеятельностиКт],
    VT._PeriodAdjustment AS [УточнениеПериода],
    VT._ValueDt1_RRRef AS [ExtDimensionDr1],
    VT._ValueDt1_TYPE AS [ExtDimensionDr1_TYPE],
    VT._ValueDt1_RTRef AS [ExtDimensionDr1_RTRef],
    VT._ValueDt1_RRRef AS [ExtDimensionDr1_RRRef],
    VT._KindDt1RRef AS [ExtDimensionTypeDr1],
    VT._ValueDt2_RRRef AS [ExtDimensionDr2],
    VT._ValueDt2_TYPE AS [ExtDimensionDr2_TYPE],
    VT._ValueDt2_RTRef AS [ExtDimensionDr2_RTRef],
    VT._ValueDt2_RRRef AS [ExtDimensionDr2_RRRef],
    VT._KindDt2RRef AS [ExtDimensionTypeDr2],
    VT._ValueDt3_RRRef AS [ExtDimensionDr3],
    VT._ValueDt3_TYPE AS [ExtDimensionDr3_TYPE],
    VT._ValueDt3_RTRef AS [ExtDimensionDr3_RTRef],
    VT._ValueDt3_RRRef AS [ExtDimensionDr3_RRRef],
    VT._KindDt3RRef AS [ExtDimensionTypeDr3],
    VT._ValueCt1_RRRef AS [ExtDimensionCr1],
    VT._ValueCt1_TYPE AS [ExtDimensionCr1_TYPE],
    VT._ValueCt1_RTRef AS [ExtDimensionCr1_RTRef],
    VT._ValueCt1_RRRef AS [ExtDimensionCr1_RRRef],
    VT._KindCt1RRef AS [ExtDimensionTypeCr1],
    VT._ValueCt2_RRRef AS [ExtDimensionCr2],
    VT._ValueCt2_TYPE AS [ExtDimensionCr2_TYPE],
    VT._ValueCt2_RTRef AS [ExtDimensionCr2_RTRef],
    VT._ValueCt2_RRRef AS [ExtDimensionCr2_RRRef],
    VT._KindCt2RRef AS [ExtDimensionTypeCr2],
    VT._ValueCt3_RRRef AS [ExtDimensionCr3],
    VT._ValueCt3_TYPE AS [ExtDimensionCr3_TYPE],
    VT._ValueCt3_RTRef AS [ExtDimensionCr3_RTRef],
    VT._ValueCt3_RRRef AS [ExtDimensionCr3_RRRef],
    VT._KindCt3RRef AS [ExtDimensionTypeCr3]
  FROM dbo._AccRg1595 AS VT
    LEFT JOIN dbo._Acc23 AS TA1 ON TA1._IDRRef = VT._AccountDtRRef
    LEFT JOIN dbo._Acc23 AS TA2 ON TA2._IDRRef = VT._AccountCtRRef
  WHERE ((VT._Active = 0x01) AND VT._Fld1596RRef = @Organizaciya AND TA1._Code = @Schet AND TA2._Code = @KorrSchet)
    AND VT._Period >= @DataNach
    AND VT._Period <= @DataKon
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 5 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
