# 29. Чужая временная таблица и пролог

**Где в типовой конфигурации:** CommonModules.УчетПособийСоциальногоСтрахования, модуль, метод `РасчетПоказателей_РСВ_2017`

Сам по себе этот запрос не переводится — он читает временную таблицу,
которую создаёт другой запрос того же метода:

```
{ВнешняяОбработка.QueryToSQLTransformer.МодульОбъекта(745)}: ВТДанныеУчета is a temporary table that some other query creates - this text does not create it itself. Paste the query that fills ВТДанныеУчета into the "Missing queries" field above and translate again.
```

Это не предел транслятора, а недостающий контекст. Текст, создающий таблицу,
передаётся настройкой `Prologue` — и запрос переводится.

## Пролог: запрос, создающий временную таблицу

```sql
ВЫБРАТЬ
	Пособия.ФизическоеЛицо КАК ФизическоеЛицо,
	Пособия.ВидЗанятости КАК ВидЗанятости,
	Пособия.ВидЗанятости КАК ПроверяемыйВидЗанятости,
	Пособия.ВидПособияСоциальногоСтрахования КАК ВидПособияСоциальногоСтрахования,
	Пособия.ФинансированиеФедеральнымБюджетом КАК ФинансированиеФедеральнымБюджетом,
	НАЧАЛОПЕРИОДА(Пособия.Период, МЕСЯЦ) КАК Период,
	СУММА(Пособия.СтраховыеСлучаи) КАК СтраховыеСлучаиОборот,
	СУММА(Пособия.ОплаченныеДни) КАК ОплаченныеДниОборот,
	СУММА(Пособия.СуммаВсего) КАК СуммаВсегоОборот,
	СУММА(Пособия.СуммаСверхНорм) КАК СуммаСверхНормОборот,
	Пособия.ФизическоеЛицо КАК ФизЛицоДляСвязей
ПОМЕСТИТЬ ВТДанныеУчета
ИЗ
	РегистрНакопления.ПособияПоСоциальномуСтрахованию КАК Пособия
ГДЕ
	Пособия.Период МЕЖДУ &НачалоОтчетногоПериода И &КонецОтчетногоПериода
	И Пособия.Организация В(&Организация)

СГРУППИРОВАТЬ ПО
	Пособия.ФизическоеЛицо,
	Пособия.ВидЗанятости,
	Пособия.ВидПособияСоциальногоСтрахования,
	Пособия.ФинансированиеФедеральнымБюджетом,
	НАЧАЛОПЕРИОДА(Пособия.Период, МЕСЯЦ),
	Пособия.ВидЗанятости,
	Пособия.ФизическоеЛицо
```

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ РАЗЛИЧНЫЕ
	&ГоловнаяОрганизация КАК ГоловнаяОрганизация,
	ДанныеУчета.ФизическоеЛицо,
	ДанныеУчета.Период
ПОМЕСТИТЬ ВТПериодыФизЛицОрганизаций
ИЗ
	ВТДанныеУчета КАК ДанныеУчета
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
НачалоОтчетногоПериода = 2017-01-01
КонецОтчетногоПериода = 2018-12-31
Организация = ВЫБРАТЬ Т.Ссылка ИЗ Справочник.Организации КАК Т
ГоловнаяОрганизация = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Ссылка ИЗ Справочник.Организации КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @GolovnayaOrganizaciya BINARY(16) = NULL; -- ГоловнаяОрганизация
DECLARE @KonecOtchetnogoPerioda DATETIME2 = NULL; -- КонецОтчетногоПериода
DECLARE @NachaloOtchetnogoPerioda DATETIME2 = NULL; -- НачалоОтчетногоПериода
DECLARE @Organizaciya BINARY(16) = NULL; -- Организация

WITH [ВТДанныеУчета] AS (
SELECT
  T1._Fld37552RRef AS [ФизическоеЛицо],
  T1._Fld37553RRef AS [ВидЗанятости],
  T1._Fld37553RRef AS [ПроверяемыйВидЗанятости],
  T1._Fld37551RRef AS [ВидПособияСоциальногоСтрахования],
  T1._Fld37554RRef AS [ФинансированиеФедеральнымБюджетом],
  DATEADD(month, DATEDIFF(month, 0, T1._Period), 0) AS [Период],
  CAST(SUM(T1._Fld37555 ) AS NUMERIC(11, 0)) AS [СтраховыеСлучаиОборот],
  CAST(SUM(T1._Fld37556 ) AS NUMERIC(11, 0)) AS [ОплаченныеДниОборот],
  CAST(SUM(T1._Fld37557 ) AS NUMERIC(21, 2)) AS [СуммаВсегоОборот],
  CAST(SUM(T1._Fld37558 ) AS NUMERIC(21, 2)) AS [СуммаСверхНормОборот],
  T1._Fld37552RRef AS [ФизЛицоДляСвязей]
FROM dbo._AccumRg37549 AS T1
WHERE T1._Period BETWEEN @NachaloOtchetnogoPerioda AND @KonecOtchetnogoPerioda
  AND T1._Fld37550RRef IN(@Organizaciya)
GROUP BY T1._Fld37552RRef, T1._Fld37553RRef, T1._Fld37551RRef, T1._Fld37554RRef, DATEADD(month, DATEDIFF(month, 0, T1._Period), 0)
)
SELECT DISTINCT
  @GolovnayaOrganizaciya AS [ГоловнаяОрганизация],
  T1.[ФизическоеЛицо] AS [ФизическоеЛицо],
  T1.[Период] AS [Период]
FROM [ВТДанныеУчета] AS T1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- The batch has no final query; the result of the last temporary table "ВТПериодыФизЛицОрганизаций" is returned.
- Values are missing for 4 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
