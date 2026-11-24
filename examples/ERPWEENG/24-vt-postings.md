# 24. Виртуальные таблицы бухрегистра

**Где в типовой конфигурации:** DataProcessors.DocumentPostingInFinancialAccounting, форма FinancialAccountingPostings, модуль формы, метод `ReadTransactions`

## Запрос на языке запросов 1С

```sql
SELECT
	*
FROM
	AccountingRegister.International.RecordsWithExtDimensions(,, Recorder = &Document,,) AS International
;

////////////////////////////////////////////////////////////////////////////////
SELECT
	*
FROM
	AccountingRegister.InternationalWithoutCorrespondence.RecordsWithExtDimensions(,, Recorder = &Document,,) AS InternationalWithoutCorrespondence
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Document = SELECT TOP 1 T.Recorder FROM AccountingRegister.International AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Document BINARY(16) = NULL; -- Document

SELECT
  T1.[Period] AS [Period],
  T1.[Recorder] AS [Recorder],
  T1.[Recorder_RTRef] AS [Recorder_RTRef],
  T1.[Recorder_RRRef] AS [Recorder_RRRef],
  T1.[LineNumber] AS [LineNumber],
  T1.[Active] AS [Active],
  T1.[Account] AS [Account],
  T1.[ExtDimension1] AS [ExtDimension1],
  T1.[ExtDimension1_TYPE] AS [ExtDimension1_TYPE],
  T1.[ExtDimension1_RTRef] AS [ExtDimension1_RTRef],
  T1.[ExtDimension1_RRRef] AS [ExtDimension1_RRRef],
  T1.[ExtDimensionType1] AS [ExtDimensionType1],
  T1.[ExtDimension2] AS [ExtDimension2],
  T1.[ExtDimension2_TYPE] AS [ExtDimension2_TYPE],
  T1.[ExtDimension2_RTRef] AS [ExtDimension2_RTRef],
  T1.[ExtDimension2_RRRef] AS [ExtDimension2_RRRef],
  T1.[ExtDimensionType2] AS [ExtDimensionType2],
  T1.[ExtDimension3] AS [ExtDimension3],
  T1.[ExtDimension3_TYPE] AS [ExtDimension3_TYPE],
  T1.[ExtDimension3_RTRef] AS [ExtDimension3_RTRef],
  T1.[ExtDimension3_RRRef] AS [ExtDimension3_RRRef],
  T1.[ExtDimensionType3] AS [ExtDimensionType3],
  T1.[ChartOfAccounts] AS [ChartOfAccounts],
  T1.[Organization] AS [Organization],
  T1.[Department] AS [Department],
  T1.[Currency] AS [Currency],
  T1.[LineOfBusiness] AS [LineOfBusiness],
  T1.[Sum] AS [Sum],
  T1.[PresentationAmount] AS [PresentationAmount],
  T1.[CurrencyAmount] AS [CurrencyAmount],
  T1.[Count] AS [Count],
  T1.[Content] AS [Content],
  T1.[PostingTemplate] AS [PostingTemplate],
  T1.[PostingType] AS [PostingType],
  T1.[AccountCompliance] AS [AccountCompliance],
  T1.[EqualityOfTurnoverTotals] AS [EqualityOfTurnoverTotals],
  T1.[ReversingEntry] AS [ReversingEntry],
  T1.[FinRecordID] AS [FinRecordID],
  T1.[BusinessTransactionSetting] AS [BusinessTransactionSetting],
  T1.[RecordType] AS [RecordType]
FROM (
  SELECT
    VT._Fld37145 AS [FinRecordID],
    VT._Fld37143 AS [EqualityOfTurnoverTotals],
    VT._Fld37142 AS [AccountCompliance],
    VT._Fld37141RRef AS [PostingType],
    VT._Fld37138 AS [Count],
    VT._Fld37140RRef AS [PostingTemplate],
    VT._Fld37136 AS [PresentationAmount],
    VT._Fld37135 AS [Sum],
    VT._Fld37137 AS [CurrencyAmount],
    VT._Fld37133RRef AS [Currency],
    VT._Fld37146RRef AS [BusinessTransactionSetting],
    VT._AccountRRef AS [Account],
    VT._Fld37132RRef AS [Department],
    VT._Fld1035 AS [DataAreaMainData],
    VT._Correspond AS [RecordType],
    VT._Active AS [Active],
    VT._Fld37130RRef AS [ChartOfAccounts],
    VT._LineNo AS [LineNumber],
    VT._Fld37144 AS [ReversingEntry],
    VT._Fld37139 AS [Content],
    VT._RecorderRRef AS [Recorder],
    VT._RecorderTRef AS [Recorder_RTRef],
    VT._RecorderRRef AS [Recorder_RRRef],
    VT._Period AS [Period],
    VT._Fld37131RRef AS [Organization],
    VT._Fld37134RRef AS [LineOfBusiness],
    VT._Value1_RRRef AS [ExtDimension1],
    VT._Value1_TYPE AS [ExtDimension1_TYPE],
    VT._Value1_RTRef AS [ExtDimension1_RTRef],
    VT._Value1_RRRef AS [ExtDimension1_RRRef],
    VT._Kind1RRef AS [ExtDimensionType1],
    VT._Value2_RRRef AS [ExtDimension2],
    VT._Value2_TYPE AS [ExtDimension2_TYPE],
    VT._Value2_RTRef AS [ExtDimension2_RTRef],
    VT._Value2_RRRef AS [ExtDimension2_RRRef],
    VT._Kind2RRef AS [ExtDimensionType2],
    VT._Value3_RRRef AS [ExtDimension3],
    VT._Value3_TYPE AS [ExtDimension3_TYPE],
    VT._Value3_RTRef AS [ExtDimension3_RTRef],
    VT._Value3_RRRef AS [ExtDimension3_RRRef],
    VT._Kind3RRef AS [ExtDimensionType3]
  FROM dbo._AccRg37129 AS VT
  WHERE ((VT._RecorderRRef = @Document))
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has 2 queries returning a result. Only the last one is translated, the way Query.Execute() behaves; the earlier result sets are not in the SQL. Translate such queries separately if you need them.
- Field Recorder is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
