# 26. АВТОУПОРЯДОЧИВАНИЕ

**Где в типовой конфигурации:** CommonModules.ФинансоваяОтчетностьСервер, модуль, метод `ТаблицаИндексовКартинок`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	ПланыСчетовМеждународногоУчета.Ссылка
ИЗ
	Справочник.ПланыСчетовМеждународногоУчета КАК ПланыСчетовМеждународногоУчета
ГДЕ
	НЕ ПланыСчетовМеждународногоУчета.ПометкаУдаления

АВТОУПОРЯДОЧИВАНИЕ
```

## Что получилось в SQL

```sql
SELECT
  T1._IDRRef AS [Ссылка]
FROM dbo._Reference162235 AS T1
WHERE NOT (T1._Marked = 0x01)
```

## Предупреждения обработки

- AUTOORDER is ignored: the platform adds ordering by reference presentation there, and that happens outside the DBMS query. The rows come back in a different order.
- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
