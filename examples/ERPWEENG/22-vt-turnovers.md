# 22. Виртуальная таблица оборотов

**Где в типовой конфигурации:** Documents.AllocationOfOtherCosts, форма SettingsFormOfCostCenters, модуль формы, метод `DetermineVisibilityAndAmountOfExpensesForArticle`

## Запрос на языке запросов 1С

```sql
SELECT TOP 1
	*
FROM
	AccumulationRegister.RegisterRecordsProductsIncomeExpenses.Turnovers(
			&StartDate,
			&EndDate,
			,
			DimensionOfExpenses = &Dimension) AS RegisterRecords
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
StartDate = 2000-01-01
EndDate = 2030-01-01
Dimension = SELECT TOP 1 T.DimensionOfExpenses FROM AccumulationRegister.RegisterRecordsProductsIncomeExpenses AS T
```

## Тот же запрос в SQL

```sql
DECLARE @Dimension BINARY(16) = NULL; -- Dimension
DECLARE @EndDate DATETIME2 = NULL; -- EndDate
DECLARE @StartDate DATETIME2 = NULL; -- StartDate

SELECT TOP 1
  T1.[BusinessOperation] AS [BusinessOperation],
  T1.[Organization] AS [Organization],
  T1.[Department] AS [Department],
  T1.[ProductLineOfBusiness] AS [ProductLineOfBusiness],
  T1.[ItemsLocationAttributes] AS [ItemsLocationAttributes],
  T1.[Warehouse] AS [Warehouse],
  T1.[Warehouse_TYPE] AS [Warehouse_TYPE],
  T1.[Warehouse_RTRef] AS [Warehouse_RTRef],
  T1.[Warehouse_RRRef] AS [Warehouse_RRRef],
  T1.[InventoryType] AS [InventoryType],
  T1.[InventoryOwnerAttribute] AS [InventoryOwnerAttribute],
  T1.[LineOfBusinessItems] AS [LineOfBusinessItems],
  T1.[IncomeAndExpenseItem] AS [IncomeAndExpenseItem],
  T1.[IncomeAndExpenseItem_TYPE] AS [IncomeAndExpenseItem_TYPE],
  T1.[IncomeAndExpenseItem_RTRef] AS [IncomeAndExpenseItem_RTRef],
  T1.[IncomeAndExpenseItem_RRRef] AS [IncomeAndExpenseItem_RRRef],
  T1.[DimensionOfRevenue] AS [DimensionOfRevenue],
  T1.[DimensionOfRevenue_TYPE] AS [DimensionOfRevenue_TYPE],
  T1.[DimensionOfRevenue_RTRef] AS [DimensionOfRevenue_RTRef],
  T1.[DimensionOfRevenue_RRRef] AS [DimensionOfRevenue_RRRef],
  T1.[DimensionOfExpenses] AS [DimensionOfExpenses],
  T1.[DimensionOfExpenses_TYPE] AS [DimensionOfExpenses_TYPE],
  T1.[DimensionOfExpenses_RTRef] AS [DimensionOfExpenses_RTRef],
  T1.[DimensionOfExpenses_RRRef] AS [DimensionOfExpenses_RRRef],
  T1.[AssetsLiabilitiesDimension] AS [AssetsLiabilitiesDimension],
  T1.[AssetsLiabilitiesDimension_TYPE] AS [AssetsLiabilitiesDimension_TYPE],
  T1.[AssetsLiabilitiesDimension_RTRef] AS [AssetsLiabilitiesDimension_RTRef],
  T1.[AssetsLiabilitiesDimension_RRRef] AS [AssetsLiabilitiesDimension_RRRef],
  CAST(T1.[CountTurnover] AS NUMERIC(21, 3)) AS [CountTurnover],
  CAST(T1.[CostTurnover] AS NUMERIC(21, 2)) AS [CostTurnover],
  CAST(T1.[CostExcludingVATTurnover] AS NUMERIC(21, 2)) AS [CostExcludingVATTurnover],
  CAST(T1.[CostManTurnover] AS NUMERIC(21, 2)) AS [CostManTurnover],
  CAST(T1.[LocalCostTurnover] AS NUMERIC(21, 2)) AS [LocalCostTurnover],
  CAST(T1.[OffBalanceCostTurnover] AS NUMERIC(21, 2)) AS [OffBalanceCostTurnover],
  CAST(T1.[OffBalanceCostLocalTurnover] AS NUMERIC(21, 2)) AS [OffBalanceCostLocalTurnover],
  CAST(T1.[AddExpensesForGoodsTurnover] AS NUMERIC(21, 2)) AS [AddExpensesForGoodsTurnover],
  CAST(T1.[AdditionalExpensesExcludingVATTurnover] AS NUMERIC(21, 2)) AS [AdditionalExpensesExcludingVATTurnover],
  CAST(T1.[AddExpensesManTurnover] AS NUMERIC(21, 2)) AS [AddExpensesManTurnover],
  CAST(T1.[AddExpensesLocalTurnover] AS NUMERIC(21, 2)) AS [AddExpensesLocalTurnover],
  CAST(T1.[ItemizedFixedCostsIncludingVATTurnover] AS NUMERIC(21, 2)) AS [ItemizedFixedCostsIncludingVATTurnover],
  CAST(T1.[ItemizedFixedCostsExcludingVATTurnover] AS NUMERIC(21, 2)) AS [ItemizedFixedCostsExcludingVATTurnover],
  CAST(T1.[ItemizedFixedCostsManagTurnover] AS NUMERIC(21, 2)) AS [ItemizedFixedCostsManagTurnover],
  CAST(T1.[ItemizedFixedCostsComplTurnover] AS NUMERIC(21, 2)) AS [ItemizedFixedCostsComplTurnover],
  CAST(T1.[LaborCostsTurnover] AS NUMERIC(21, 2)) AS [LaborCostsTurnover],
  CAST(T1.[LaborCostsManTurnover] AS NUMERIC(21, 2)) AS [LaborCostsManTurnover],
  CAST(T1.[LaborCostsLocalTurnover] AS NUMERIC(21, 2)) AS [LaborCostsLocalTurnover],
  CAST(T1.[ItemizedVariableCostsIncludingVATTurnover] AS NUMERIC(21, 2)) AS [ItemizedVariableCostsIncludingVATTurnover],
  CAST(T1.[ItemizedVariableCostsExcludingVATTurnover] AS NUMERIC(21, 2)) AS [ItemizedVariableCostsExcludingVATTurnover],
  CAST(T1.[ItemizedVariableCostsManagTurnover] AS NUMERIC(21, 2)) AS [ItemizedVariableCostsManagTurnover],
  CAST(T1.[ItemizedVariableCostsComplTurnover] AS NUMERIC(21, 2)) AS [ItemizedVariableCostsComplTurnover],
  CAST(T1.[PermanentDifferenceTurnover] AS NUMERIC(21, 2)) AS [PermanentDifferenceTurnover],
  CAST(T1.[CostTDTurnover] AS NUMERIC(21, 2)) AS [CostTDTurnover],
  CAST(T1.[ProvisionForImpairmentLocalTurnover] AS NUMERIC(21, 2)) AS [ProvisionForImpairmentLocalTurnover],
  CAST(T1.[ProvisionForImpairmentManTurnover] AS NUMERIC(21, 2)) AS [ProvisionForImpairmentManTurnover]
FROM (
    SELECT Z.* FROM (
    SELECT
      VT._Fld26018RRef AS [BusinessOperation],
      VT._Fld26019RRef AS [Organization],
      VT._Fld26020RRef AS [Department],
      VT._Fld26021RRef AS [ProductLineOfBusiness],
      VT._Fld26022RRef AS [ItemsLocationAttributes],
      VT._Fld26023_RRRef AS [Warehouse],
      VT._Fld26023_TYPE AS [Warehouse_TYPE],
      VT._Fld26023_RTRef AS [Warehouse_RTRef],
      VT._Fld26023_RRRef AS [Warehouse_RRRef],
      VT._Fld26024RRef AS [InventoryType],
      VT._Fld26025RRef AS [InventoryOwnerAttribute],
      VT._Fld26026RRef AS [LineOfBusinessItems],
      VT._Fld26027_RRRef AS [IncomeAndExpenseItem],
      VT._Fld26027_TYPE AS [IncomeAndExpenseItem_TYPE],
      VT._Fld26027_RTRef AS [IncomeAndExpenseItem_RTRef],
      VT._Fld26027_RRRef AS [IncomeAndExpenseItem_RRRef],
      VT._Fld26028_RRRef AS [DimensionOfRevenue],
      VT._Fld26028_TYPE AS [DimensionOfRevenue_TYPE],
      VT._Fld26028_RTRef AS [DimensionOfRevenue_RTRef],
      VT._Fld26028_RRRef AS [DimensionOfRevenue_RRRef],
      VT._Fld26029_RRRef AS [DimensionOfExpenses],
      VT._Fld26029_TYPE AS [DimensionOfExpenses_TYPE],
      VT._Fld26029_RTRef AS [DimensionOfExpenses_RTRef],
      VT._Fld26029_RRRef AS [DimensionOfExpenses_RRRef],
      VT._Fld26030_RRRef AS [AssetsLiabilitiesDimension],
      VT._Fld26030_TYPE AS [AssetsLiabilitiesDimension_TYPE],
      VT._Fld26030_RTRef AS [AssetsLiabilitiesDimension_RTRef],
      VT._Fld26030_RRRef AS [AssetsLiabilitiesDimension_RRRef],
      SUM(VT._Fld26031) AS [CountTurnover],
      SUM(VT._Fld26032) AS [CostTurnover],
      SUM(VT._Fld26033) AS [CostExcludingVATTurnover],
      SUM(VT._Fld26034) AS [CostManTurnover],
      SUM(VT._Fld26035) AS [LocalCostTurnover],
      SUM(VT._Fld26036) AS [OffBalanceCostTurnover],
      SUM(VT._Fld26037) AS [OffBalanceCostLocalTurnover],
      SUM(VT._Fld26038) AS [AddExpensesForGoodsTurnover],
      SUM(VT._Fld26039) AS [AdditionalExpensesExcludingVATTurnover],
      SUM(VT._Fld26040) AS [AddExpensesManTurnover],
      SUM(VT._Fld26041) AS [AddExpensesLocalTurnover],
      SUM(VT._Fld26042) AS [ItemizedFixedCostsIncludingVATTurnover],
      SUM(VT._Fld26043) AS [ItemizedFixedCostsExcludingVATTurnover],
      SUM(VT._Fld26044) AS [ItemizedFixedCostsManagTurnover],
      SUM(VT._Fld26045) AS [ItemizedFixedCostsComplTurnover],
      SUM(VT._Fld26046) AS [LaborCostsTurnover],
      SUM(VT._Fld26047) AS [LaborCostsManTurnover],
      SUM(VT._Fld26048) AS [LaborCostsLocalTurnover],
      SUM(VT._Fld26049) AS [ItemizedVariableCostsIncludingVATTurnover],
      SUM(VT._Fld26050) AS [ItemizedVariableCostsExcludingVATTurnover],
      SUM(VT._Fld26051) AS [ItemizedVariableCostsManagTurnover],
      SUM(VT._Fld26052) AS [ItemizedVariableCostsComplTurnover],
      SUM(VT._Fld26053) AS [PermanentDifferenceTurnover],
      SUM(VT._Fld26054) AS [CostTDTurnover],
      SUM(VT._Fld26055) AS [ProvisionForImpairmentLocalTurnover],
      SUM(VT._Fld26056) AS [ProvisionForImpairmentManTurnover]
    FROM dbo._AccumRg26017 AS VT
    WHERE VT._Active = 0x01
      AND VT._Period >= @StartDate
      AND VT._Period <= @EndDate
      AND ((VT._Fld26029_TYPE = 0x08 AND VT._Fld26029_RRRef = @Dimension))
    GROUP BY VT._Fld26018RRef, VT._Fld26019RRef, VT._Fld26020RRef, VT._Fld26021RRef, VT._Fld26022RRef, VT._Fld26023_RRRef, VT._Fld26023_TYPE, VT._Fld26023_RTRef, VT._Fld26023_RRRef, VT._Fld26024RRef, VT._Fld26025RRef, VT._Fld26026RRef, VT._Fld26027_RRRef, VT._Fld26027_TYPE, VT._Fld26027_RTRef, VT._Fld26027_RRRef, VT._Fld26028_RRRef, VT._Fld26028_TYPE, VT._Fld26028_RTRef, VT._Fld26028_RRRef, VT._Fld26029_RRRef, VT._Fld26029_TYPE, VT._Fld26029_RTRef, VT._Fld26029_RRRef, VT._Fld26030_RRRef, VT._Fld26030_TYPE, VT._Fld26030_RTRef, VT._Fld26030_RRRef
    HAVING SUM(VT._Fld26031) <> 0
       OR SUM(VT._Fld26032) <> 0
       OR SUM(VT._Fld26033) <> 0
       OR SUM(VT._Fld26034) <> 0
       OR SUM(VT._Fld26035) <> 0
       OR SUM(VT._Fld26036) <> 0
       OR SUM(VT._Fld26037) <> 0
       OR SUM(VT._Fld26038) <> 0
       OR SUM(VT._Fld26039) <> 0
       OR SUM(VT._Fld26040) <> 0
       OR SUM(VT._Fld26041) <> 0
       OR SUM(VT._Fld26042) <> 0
       OR SUM(VT._Fld26043) <> 0
       OR SUM(VT._Fld26044) <> 0
       OR SUM(VT._Fld26045) <> 0
       OR SUM(VT._Fld26046) <> 0
       OR SUM(VT._Fld26047) <> 0
       OR SUM(VT._Fld26048) <> 0
       OR SUM(VT._Fld26049) <> 0
       OR SUM(VT._Fld26050) <> 0
       OR SUM(VT._Fld26051) <> 0
       OR SUM(VT._Fld26052) <> 0
       OR SUM(VT._Fld26053) <> 0
       OR SUM(VT._Fld26054) <> 0
       OR SUM(VT._Fld26055) <> 0
       OR SUM(VT._Fld26056) <> 0
    ) AS Z
    WHERE Z.[CountTurnover] <> 0
       OR Z.[CostTurnover] <> 0
       OR Z.[CostExcludingVATTurnover] <> 0
       OR Z.[CostManTurnover] <> 0
       OR Z.[LocalCostTurnover] <> 0
       OR Z.[OffBalanceCostTurnover] <> 0
       OR Z.[OffBalanceCostLocalTurnover] <> 0
       OR Z.[AddExpensesForGoodsTurnover] <> 0
       OR Z.[AdditionalExpensesExcludingVATTurnover] <> 0
       OR Z.[AddExpensesManTurnover] <> 0
       OR Z.[AddExpensesLocalTurnover] <> 0
       OR Z.[ItemizedFixedCostsIncludingVATTurnover] <> 0
       OR Z.[ItemizedFixedCostsExcludingVATTurnover] <> 0
       OR Z.[ItemizedFixedCostsManagTurnover] <> 0
       OR Z.[ItemizedFixedCostsComplTurnover] <> 0
       OR Z.[LaborCostsTurnover] <> 0
       OR Z.[LaborCostsManTurnover] <> 0
       OR Z.[LaborCostsLocalTurnover] <> 0
       OR Z.[ItemizedVariableCostsIncludingVATTurnover] <> 0
       OR Z.[ItemizedVariableCostsExcludingVATTurnover] <> 0
       OR Z.[ItemizedVariableCostsManagTurnover] <> 0
       OR Z.[ItemizedVariableCostsComplTurnover] <> 0
       OR Z.[PermanentDifferenceTurnover] <> 0
       OR Z.[CostTDTurnover] <> 0
       OR Z.[ProvisionForImpairmentLocalTurnover] <> 0
       OR Z.[ProvisionForImpairmentManTurnover] <> 0
  ) AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by DataAreaAuxiliaryData, DataAreaMainData, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Field DimensionOfExpenses is of a composite type and is compared with a parameter. The condition pins the type byte, so it no longer matches rows that hold no value at all, but the table of the reference type is only known once a value is supplied. Where every stored value is an empty reference - access kinds, for instance - the reference column carries no information and the condition stays wider than the platform's. Supply the parameter value, compare with VALUE(...), or add a VALUETYPE(...) condition.
- Values are missing for 3 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
