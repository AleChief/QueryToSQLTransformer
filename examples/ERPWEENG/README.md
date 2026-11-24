# Примеры: ERPWEENG 2.5.27.50

Каждый пример - запрос из **типовой части** конфигурации ERPWEENG 2.5.27.50 и SQL, который
получен из него обработкой. Запросы не придуманы для показа - это короткие цитаты из
типовой конфигурации, приведённые чтобы показать, во что обработка переводит ту или иную
конструкцию языка запросов. Каждый приведён с указанием модуля и метода, откуда он взят.
Права на код конфигурации принадлежат её правообладателю; здесь приведены отдельные
запросы, в среднем по девять строк, и восстановить по ним конфигурацию невозможно.

| Конфигурация | Имя метаданных | Платформа | Диалект |
|---|---|---|---|
| ERPWEENG 2.5.27.50 | ERPWEENG | 8.3.27.2214 | MSSQL |

Каждый SQL здесь СУБД разобрала и связала все имена
(`sys.dm_exec_describe_first_result_set`), то есть он не только синтаксически верен,
но и ссылается на существующие таблицы и колонки. Физические имена (`_Reference123`, `_Fld4567`)
принадлежат той базе, где обработка запускалась: **в другой базе они другие**,
и запрос из примера надо получить заново на своей базе.

| № | Класс конструкции | Где в конфигурации |
|---|---|---|
| [01](01-select-where.md) | простая выборка с условием | Catalogs.ControlledLots, модуль менеджера, `RegisterDataToProcessForMigrationToNewVersion` |
| [02](02-distinct.md) | РАЗЛИЧНЫЕ | Catalogs.ExchangeMessageTransportSettings, модуль менеджера, `TransferTransportSettingsForExchangeScenarios` |
| [03](03-top-order.md) | ПЕРВЫЕ и УПОРЯДОЧИТЬ ПО | CommonModules.InteractionsEvents, модуль, `OnWriteEmailAccount` |
| [04](04-join.md) | соединения таблиц | InformationRegisters.SegmentProducts, форма ProductSegmentsParameter, модуль формы, `DetermineUseOfCharacteristics` |
| [05](05-dot-reference.md) | обращение через точку к реквизиту ссылки | CommonModules.DiscountsMarkupsServer, модуль, `ApplyCalculationResultForBonusPoints` |
| [06](06-group-by.md) | группировка и агрегатные функции | CommonModules.ObjectsVersioning, модуль, `OnCollectConfigurationStatisticsParameters` |
| [07](07-having.md) | ИМЕЮЩИЕ | Catalogs.BillsOfMaterials, форма ItemForm, модуль формы, `FillInServiceDetailsOfProductionProcess` |
| [08](08-case.md) | ВЫБОР КОГДА | Catalogs.Assignments, модуль менеджера, `AddDescriptionOfYourOrders` |
| [09](09-isnull.md) | ЕСТЬNULL | InformationRegisters.JobsForUpdatingFixedAssetRecords, модуль менеджера, `CalculationStart` |
| [10](10-cast.md) | ВЫРАЗИТЬ | Catalogs.ExchangeMessageTransportSettings, модуль менеджера, `TransferTransportSettingsForExchangeScenarios` |
| [11](11-like.md) | ПОДОБНО | CommonModules.Common, модуль, `DeleteVersionCacheRecords` |
| [12](12-in-hierarchy.md) | В ИЕРАРХИИ | CommonModules.WarehousesServer, модуль, `ListOfSubordinateWarehouses` |
| [13](13-refs.md) | ССЫЛКА и ТИПЗНАЧЕНИЯ | Catalogs.ControlledLots, модуль менеджера, `RegisterDataToProcessForMigrationToNewVersion` |
| [14](14-presentation.md) | ПРЕДСТАВЛЕНИЕ ссылки | CommonForms.TransactionGLAccountsSettings, модуль, `AddDetailsElementsOfInternationalAccounting` |
| [15](15-union.md) | ОБЪЕДИНИТЬ | InformationRegisters.UsersInfo, модуль менеджера, `ResetOpenIDConnectAuthenticationForAllUsers` |
| [16](16-subquery-from.md) | вложенный запрос в источнике | Documents.ProductionStage2_2, модуль объекта, `CheckDetailsOfChainOfStages` |
| [17](17-subquery-in.md) | вложенный запрос в условии | CommonModules.MobileWarehouseKeeperWorkspace, модуль, `FindAmbiguousIBUsers` |
| [18](18-temp-table.md) | временные таблицы | Documents.GiftCertificateSale, модуль менеджера, `QueryTextTTTableAmountByPaymentCards` |
| [19](19-batch.md) | пакет запросов | CommonModules.TMPeripheralsServerCall, модуль, `CashRegisterRelatedToEquipment` |
| [20](20-drop-table.md) | УНИЧТОЖИТЬ | CommonModules.MobileApplicationSalesOrdersOverridable, модуль, `CustomImplementation` |
| [21](21-vt-balance.md) | виртуальная таблица остатков | Documents.CustomerCommercialInvoice, форма CommercialInvoiceCreationForm, модуль формы, `RefreshServer` |
| [22](22-vt-turnovers.md) | виртуальная таблица оборотов | Documents.AllocationOfOtherCosts, форма SettingsFormOfCostCenters, модуль формы, `DetermineVisibilityAndAmountOfExpensesForArticle` |
| [23](23-vt-slice.md) | срез последних и первых | CommonModules.PartnerPricesFillingServer, модуль, `QueryTextsForFillingInPricesBatchProcessing` |
| [24](24-vt-postings.md) | виртуальные таблицы бухрегистра | DataProcessors.DocumentPostingInFinancialAccounting, форма FinancialAccountingPostings, модуль формы, `ReadTransactions` |
| [25](25-totals.md) | ИТОГИ | DataProcessors.VendorPriceLists, форма FormSettings, модуль формы, `InitializePartnerProductHierarchyTree` |
| [26](26-auto-order.md) | АВТОУПОРЯДОЧИВАНИЕ | Catalogs.CompaniesBankAccounts, модуль менеджера, `ChoiceDataGetProcessing` |
| [27](27-parameters.md) | параметры запроса | Catalogs.DiscountsMarkups, форма SettingOfValidityStatus, модуль формы, `CustomizeForm` |
| [28](28-batch-dropped.md) | пакет с несколькими результатами | Documents.SalesOrder, модуль менеджера, `BeforePerformingActionsInOrderList` |
| [29](29-prologue.md) | чужая временная таблица и пролог | CommonForms.AccessRights, модуль, `OutputAccessGroups` |

## Чего здесь нет, и почему

- **Таблица-параметр в источнике** (`ИЗ &Таблица`) — в SQL непереводима в принципе:
  значение живёт в памяти процесса 1С, в базе его нет.
- **`ДЛЯ ИЗМЕНЕНИЯ`** — в типовой конфигурации не встречается ни разу, показывать
  пример не на чем.
- **Запросы, читающие временную таблицу из другого запроса** — такой текст сам по
  себе не переводится, и это не предел транслятора: таблицы, на которую он
  ссылается, в базе нет. Пакет, который сам создаёт временную таблицу, переводится —
  см. классы `batch` и `temp-table`.
