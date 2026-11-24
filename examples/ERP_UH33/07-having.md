# 07. ИМЕЮЩИЕ

**Где в типовой конфигурации:** Catalogs.РесурсныеСпецификации, модуль объекта, метод `ПроверитьРазборкуВСтатусеДействует`

## Запрос на языке запросов 1С

```sql
ВЫБРАТЬ
	ИСТИНА
ИЗ
	Справочник.ЭтапыПроизводства КАК ЭтапыПроизводства
ГДЕ
	ЭтапыПроизводства.Владелец = &Владелец
	И НЕ ЭтапыПроизводства.ПометкаУдаления
ИМЕЮЩИЕ
	КОЛИЧЕСТВО(*) > 1
```

## Параметры

Значения для проверки скриптом `tools/check_examples.py`: литерал или запрос 1С, который выполняется в вашей базе.

```
Владелец = ВЫБРАТЬ ПЕРВЫЕ 1 Т.Владелец ИЗ Справочник.ЭтапыПроизводства КАК Т
```

## Тот же запрос в SQL

```sql
DECLARE @Vladelec BINARY(16) = NULL; -- Владелец

SELECT
  0x01 AS [Поле1]
FROM dbo._Reference501 AS T1
WHERE T1._OwnerIDRRef = @Vladelec
  AND NOT (T1._Marked = 0x01)
HAVING CAST(COUNT_BIG(* ) AS NUMERIC(12, 0)) > 1
```

## Предупреждения обработки

- Data separators are not applied: the configuration separates data by ОбластьДанныхВспомогательныеДанные, ОбластьДанныхОсновныеДанные, the platform substitutes the session values itself, and the SQL does not. It returns rows of every data area.
- Values are missing for 1 parameter(s): the query carries a DECLARE header with NULL, fill it in or set the values above.
- Record level security (RLS) is not applied, even where access restrictions are configured: the SQL returns every row the DBMS account can read.
