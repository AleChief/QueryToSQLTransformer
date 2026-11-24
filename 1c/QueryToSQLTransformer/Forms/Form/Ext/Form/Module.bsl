// QueryToSQLTransformer 0.3.0 - translates a 1C query into T-SQL (MS SQL Server) / PostgreSQL.
// Author:   Aleksei Iaskeliainen
// Licence:  MIT + Commons Clause - free to use, change and embed, including in a company;
//           selling the processor or a paid service built on it is not allowed.
// Infostart: https://infostart.ru/1c/tools/2855868/
// GitHub:    https://github.com/AleChief/QueryToSQLTransformer
// Free download on GitHub; the article and the file are also on Infostart. New versions are published only on GitHub.
//
// The form is a thin wrapper: it collects options and calls the object module,
// so a COM or headless run goes through exactly the same code.

#Region FormEventHandlers

&AtServer
Procedure OnCreateAtServer(Cancel, StandardProcessing)

	Items.Dialect.ChoiceList.Add("MSSQL", "MS SQL Server (T-SQL)");
	Items.Dialect.ChoiceList.Add("PostgreSQL", "PostgreSQL");

	Dialect = "MSSQL";
	DateOffset = 2000;
	// A year offset is a count, not an amount: no digit grouping.
	Items.DateOffset.Format = "NG=0";
	Items.DateOffset.EditFormat = "NG=0";
	SchemaName = "dbo";

EndProcedure

#EndRegion

#Region FormCommandHandlers

&AtClient
Procedure Transform(Command)

	TransformAtServer();

EndProcedure

&AtClient
Procedure ClearAll(Command)

	QueryText = "";
	SQLText = "";
	ErrorText = "";

EndProcedure

&AtClient
Procedure OpenQueryBuilder(Command)

	// The query builder is a client object. Its AutoAddViews property exists only in the
	// thick client, so referring to the builder directly would break compilation of the
	// thin client. The call is assembled as text and executed - the same trick the
	// standard managed query consoles use.
	Attempts = New Array;
	Attempts.Add("Builder = New QueryWizard(QueryText);");
	Attempts.Add("Builder = New " + "КонструкторЗапроса" + "(QueryText);");

	Created = False;
	LastError = "";
	For Each Attempt In Attempts Do
		Try
			Execute(Attempt + "
				|Builder.Show(New NotifyDescription(""AfterQueryBuilder"", ThisObject));");
			Created = True;
			Break;
		Except
			LastError = ErrorDescription();
		EndTry;
	EndDo;

	If Not Created Then
		ErrorText = QueryBuilderUnavailable() + Chars.LF + LastError;
	EndIf;

EndProcedure

&AtClient
Procedure AfterQueryBuilder(Text, AdditionalParameters) Export

	If Text <> Undefined Then
		QueryText = Text;
	EndIf;

EndProcedure

&AtClient
Procedure OpenProject(Command)

	GotoURL(ProjectPage());

EndProcedure

&AtClient
Procedure OpenArticle(Command)

	GotoURL(ArticlePage());

EndProcedure

#EndRegion

#Region Private

&AtServer
Procedure TransformAtServer()

	SQLText = "";
	ErrorText = "";

	Processor = FormAttributeToValue("Object");

	Options = Processor.DefaultOptions();
	Options.Dialect = Dialect;
	Options.DateOffset = DateOffset;
	Options.SchemaName = SchemaName;
	Options.ParameterValues = Processor.ParseParameterValues(ParameterText);
	Options.SubstituteParameters = True;
	Options.Prologue = PrologueText;
	Options.Language = Processor.SessionLanguage();

	Result = Processor.Transform(QueryText, Options);

	Notes = New Array;
	Missing = New Array;
	For Each Name In Processor.QueryParameterNames(QueryText) Do
		If Options.ParameterValues.Get(Name) = Undefined Then
			Missing.Add(Name);
		EndIf;
	EndDo;
	If Missing.Count() > 0 Then
		Notes.Add(StrTemplate(?(Options.Language = "ru",
			"Не заданы значения: %1. Добавьте выше строки ""Имя = значение"", иначе в SQL останутся заглушки, и как есть он не выполнится.",
			"No value given for: %1. Add lines ""Name = value"" above, otherwise the SQL keeps placeholders and will not run as is."),
			StrConcat(Missing, ", ")));
	EndIf;

	If Result.Success Then
		SQLText = Result.SQL;
		For Each Warning In Result.Warnings Do
			Notes.Add(Warning);
		EndDo;
		If Notes.Count() = 0 Then
			Notes.Add(?(Options.Language = "ru",
				"Переведено. Прежде чем использовать результат в отчёте, сверьте его с тем же запросом, выполненным в 1С.",
				"Translated. Check the result against the same query run in 1C before using it in a report."));
		EndIf;
	Else
		Notes.Insert(0, Result.ErrorDescription);
	EndIf;

	ErrorText = StrConcat(Notes, Chars.LF);

EndProcedure

// Free download on GitHub; the article and the file are also on Infostart. New versions are published only on GitHub.
// The language of the session is read on the server, the same way the object module reads it.
&AtServerNoContext
Function QueryBuilderUnavailable()

	Code = "";
	Try
		Code = CurrentLanguage().LanguageCode;
	Except
		Code = "";
	EndTry;
	Return ?(Lower(Left(Code, 2)) = "ru", "Конструктор запроса недоступен в этом клиенте:",
		"The query builder is not available in this client:");

EndFunction

&AtClient
Function ProjectPage()

	Return "https://github.com/AleChief/QueryToSQLTransformer";

EndFunction

&AtClient
Function ArticlePage()

	Return "https://infostart.ru/1c/tools/2855868/";

EndFunction

#EndRegion
