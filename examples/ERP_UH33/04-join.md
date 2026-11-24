# 04. Соединения таблиц

**Где в типовой конфигурации:** CommonModules.ИнтеграцияКабинетСотрудникаРасширенный, модуль, метод `ПереносИзмененияДляОбменаКабинетСотрудника`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	Сотрудники.ФизическоеЛицо КАК Ссылка
ИЗ
	РегистрСведений.УдалитьСотрудникиДляОбновленияПубликацииПравНаОтпуск КАК Таблица
		ВНУТРЕННЕЕ СОЕДИНЕНИЕ Справочник.Сотрудники КАК Сотрудники
		ПО Таблица.Сотрудник = Сотрудники.Ссылка
```

## Тот же запрос в SQL

```sql
SELECT
  T2._Fld9758RRef AS [Ссылка]
FROM dbo._InfoRg161249 AS T1
  INNER JOIN dbo._Reference388 AS T2
    ON T1._Fld161250RRef = T2._IDRRef
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
