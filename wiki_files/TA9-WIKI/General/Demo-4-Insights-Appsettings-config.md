# **Editing Appsettings config file**
Before making any changes to this file, please make sure you have a back up to the former version.

1. Edit the config file and perform the changes that you like.
2. In Portainer, go to the relevant service's configs and click on Clone config ![{D588F886-8EE8-49A8-B201-2A1A6A015246}.png](/.attachments/{D588F886-8EE8-49A8-B201-2A1A6A015246}-3734d5cb-9690-475e-981f-81a4c7a0a81b.png)
3. Paste the edited file and click on "Create config" ![{C09FA106-50AD-4415-ADED-ABAFF40E1421}.png](/.attachments/{C09FA106-50AD-4415-ADED-ABAFF40E1421}-63e97df0-0bcb-4794-9fad-1ee833a632a2.png)
4. Return to the service's config section and choose the new config file. click "add config". ![{F6F86174-2D90-4A18-97D2-94436F27563F}.png](/.attachments/{F6F86174-2D90-4A18-97D2-94436F27563F}-94ce8fa7-8c78-423a-8436-b782be2be098.png)
5. Change the config's path to the required one and click on "apply changes" ![{851CD059-9C80-469C-86F5-79BCA3562BD4}.png](/.attachments/{851CD059-9C80-469C-86F5-79BCA3562BD4}-37d70816-858c-49ba-ad64-21a1c9f89feb.png)




## Current version:

{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    },
    "Console": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft": "Warning",
        "Microsoft.Hosting.Lifetime": "Information",
        "TA9": "Information"
      },
      "FormatterName": "simple",
      "FormatterOptions": {
        "TimestampFormat": "yyyy-MM-dd HH:mm:ss "
      }
    }
  },
	"AllowedHosts": "*",
	"DataSamplePath": "DataSample/InsightsDataSample.json",
	"InsightDemoData": [
		{
			"InsightTitle": "Repeating gap",
			"InsightMessage": "Amikam David Construction Ltd Invoices to Lev Hasharon Building Materials Ltd have a feature of permanent repeating gap",
			"FIeldName": "Amount",
			"InsightCriterias": {
				"0": [
					""
				]
			},
				"Type": 3
		},
		{
			"InsightTitle": "Duplicate Invoice number 10201311",
			"InsightMessage": "The invoice number: 10201311 repeats 2 times for company 'Lev Hasharon Building Materials Ltd",
			"FIeldName": "InvoiceNumber",
			"InsightCriterias": {
				"96": [
					"10201311"
				]
			},
				"Type": 3
		},
		{
			"InsightTitle": "Identical Transactions",
			"InsightMessage": "Identical transaction amount between 'Lev Hasharon Building Materials Ltd' and 'Amikam David Construction Ltd",
			"FIeldName": "Amount",
			"InsightCriterias": {
				"0": [
					"120000"
				]
			},
				"Type": 2
		},
		{
			"InsightTitle": "Exceeds a recognized average",
			"InsightMessage": "Lev Hasharon Building Materials Ltd' total expenses exceeds in 20% of similar companies' average",
			"FIeldName": "FromCompanyNumber",
			"InsightCriterias": {
				"57": [
					"516868432"
				]
			},
				"Type": 2
		},
		{
			"InsightTitle": "Same establish day",
			"InsightMessage": "Company 'Lev Hasharon Building Materials Ltd' and 'Amikam David Construction Ltd' established on same day 07/01/2015",
			"FIeldName": "FromCompanyNumber",
			"InsightCriterias": {
				"57": [
					"516868432"
				]
			},
				"Type": 2
		},
		{
			"InsightTitle": "Exclusive one-way Transaction",
			"InsightMessage": "Amikam David Construction Ltd' invoiced only 'Lev Hasharon Building Materials Ltd",
			"FIeldName": "FromCompanyNumber",
			"InsightCriterias": {
				"57": [
					"516868432"
				]
			},
				"Type": 1
		},
		{
			"InsightTitle": "Registro criminal",
			"InsightMessage": "O número 62813934591 fez parte de uma investigação de fraude há 3 anos.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813934591"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Restrições",
			"InsightMessage": "O SIM 51010563527476 está proibido de sair do país.",
			"FIeldName": "ToImsi",
			"InsightCriterias": {
				"2": [
					"51010563527476"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Vários dispositivos",
			"InsightMessage": "Número 62813782146 troca SIM entre 2 IMEI.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813782146"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Registros forenses",
			"InsightMessage": "O número de telefone 62813103783 foi decodificado forensemente nos últimos 3 anos.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813103783"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Incompatibilidade de formato",
			"InsightMessage": "IMEI 000000886184689 não é um número IMEI válido.",
			"FIeldName": "FromImei",
			"InsightCriterias": {
				"3": [
					"000000886184689"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Números Sequenciais",
			"InsightMessage": "Números de telefone 62813100089, 62813100090, 62813100091 Telefones sequenciais.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813100089",
					"62813100090",
					"62813100091"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Atividade de tipo de chamada",
			"InsightMessage": "Número de telefone 62813100231 Só tem SMS.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813100231"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Licença de armas",
			"InsightMessage": "Número de telefone 62813103974, possui licença de porte de arma.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"62813103974"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Criminal Record",
			"InsightMessage": "Number 972551934591 was part of Fraud investigation 3 years ago.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972551934591"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Format Mismatch",
			"InsightMessage": "IMEI 000000886184688 is not a valid IMEI number.",
			"FIeldName": "FromImei",
			"InsightCriterias": {
				"3": [
					"000000886184688"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Multi Devices",
			"InsightMessage": "Number 972551782146 switch SIM between 2 IMEI.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972551782146"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Sequential Numbers",
			"InsightMessage": "Phone Numbers 972554100089, 972554100091, 972554100090 Sequential phones.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972554100089",
					"972554100091",
					"972554100090"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Call Type Activity",
			"InsightMessage": "Phone Number 972554100231 Only have SMS.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972554100231"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Forensic records",
			"InsightMessage": "Phone Number 972554103783 has been forensically decoded in recent 3 years.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972554103783"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Restrictions",
			"InsightMessage": "SIM 42507563527476 is prohibited from leaving the country.",
			"FIeldName": "ToImsi",
			"InsightCriterias": {
				"2": [
					"42507563527476"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Weapons license",
			"InsightMessage": "Phone numbers : 972554103974, 972554104001 have a weapons license.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"972554103974",
					"972554104001"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Registro criminal",
			"InsightMessage": "O número 55419934591 fez parte de uma investigação de fraude há 3 anos.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419934591"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Incompatibilidade de formato",
			"InsightMessage": "IMEI 886184688 não é um número IMEI válido.",
			"FIeldName": "FromImei",
			"InsightCriterias": {
				"3": [
					"886184688"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Vários dispositivos",
			"InsightMessage": "Número 55419782146 alterna SIM entre 2 IMEI.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419782146"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Números Sequenciais",
			"InsightMessage": "Números de telefone 55419100089, 55419100091, 55419100090 Telefones sequenciais.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419100089",
					"55419100091",
					"55419100090"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Atividade de tipo de chamada",
			"InsightMessage": "Número de telefone 55419100231 Só possui SMS.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419100231"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Registros forenses",
			"InsightMessage": "O número de telefone 55419103783 foi decodificado forensemente nos últimos 3 anos.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419103783"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Restrições",
			"InsightMessage": "O SIM 72403563527476 está proibido de sair do país.",
			"FIeldName": "ToImsi",
			"InsightCriterias": {
				"2": [
					"72403563527476"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Licença de armas",
			"InsightMessage": "Os números de telefone: 55419103974, 55419104001 possuem licença de porte de arma.",
			"FIeldName": "FromNumber",
			"InsightCriterias": {
				"1": [
					"55419103974",
					"55419104001"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Lack of substance and employees",
			"InsightMessage": "The number of employees at FRANGAO ROTISSERIE LTDA,  is relatively small compared to cash flow and the number of transactions.",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"5156787571"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "High-risk cross-border flow",
			"InsightMessage": "Company ADRIANA CARATORI GONCALVES has a Frequent cross-border flow of transactions, especially with high-risk countries : Malta, Bermuda and Mauritius.",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"2791696325"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Unexplained Cash transaction",
			"InsightMessage": "The account belonging to: MARCOS ANTONIO GONCALVES has a large amount of cash withdrawn in small installments.",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"9456736667"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "High Value non-profit Transactions",
			"InsightMessage": "Many recurring deposits to a non-profit company called: Hamza Traders Limited.",
			"FIeldName": "counterHolderName",
			"InsightCriterias": {
				"86": [
					"Hamza Traders Limited"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Paying unusually high fees",
			"InsightMessage": "Paying a significantly higher fees for accounting than the average market.",
			"FIeldName": "counterHolderName",
			"InsightCriterias": {
				"86": [
					"Accounting Consulting LTD"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Deposit without any specific justification",
			"InsightMessage": "Many deposits in high amounts with an online gambling company.",
			"FIeldName": "counterHolderName",
			"InsightCriterias": {
				"86": [
					"Poker Online SA"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Multiple similar transactions",
			"InsightMessage": "Deposit of P2P transaction in amounts which fall consistently just below identification or reporting threshold.",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"2293641165"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Inconsistent with customer’s profile",
			"InsightMessage": "The account profile has a domains mismatch in the accounts from which it receives deposits.",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"5156787571"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Darknet Indication",
			"InsightMessage": "Crypto address found in darknet marketplace.",
			"FIeldName": "fromAddress",
			"InsightCriterias": {
				"85": [
					"1PFa2VjpU8mRGb4FygKPqTDtxU6FvVPMfU"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Suspicious Mixer transaction",
			"InsightMessage": "Multi transactions were found from a Mixer who was involved in money laundering.",
			"FIeldName": "MixerName",
			"InsightCriterias": {
				"88": [
					"YoMix.IO"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Gambling sites transactions",
			"InsightMessage": "Multi transactions were found Gambling online crypto address.",
			"FIeldName": "fromName",
			"InsightCriterias": {
				"88": [
					"Poker Online SA"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Cash out transaction",
			"InsightMessage": "Cash transaction with a value higher than $100K.",
			"FIeldName": "TransactionID",
			"InsightCriterias": {
				"95": [
					"abd48059-e155-11ee-9c3c-02420a000303"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Cash out transaction",
			"InsightMessage": "Transactions with a value higher than allowed.",
			"FIeldName": "TransactionID",
			"InsightCriterias": {
				"95": [
					"abd27238-e155-11ee-9c3c-02420a000303",
					"abd27238-e155-11ee-9c3c-02420a000303",
					"abd20296-e155-11ee-9c3c-02420a000303",
					"abd2cf30-e155-11ee-9c3c-02420a000303",
					"abd2cd54-e155-11ee-9c3c-02420a000303"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "ATM Withdrawal",
			"InsightMessage": "ATM withdrawal in foreign country.",
			"FIeldName": "TransactionID",
			"InsightCriterias": {
				"95": [
					"abd4809f-e155-11ee-9c3c-02420a000303",
					"abd480d4-e155-11ee-9c3c-02420a000303",
					"abd48102-e155-11ee-9c3c-02420a000303",
					"abd4812d-e155-11ee-9c3c-02420a000303",
					"abd48158-e155-11ee-9c3c-02420a000303",
					"abd48184-e155-11ee-9c3c-02420a000303"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Echo Correlation",
			"InsightMessage": "Potential matching of IFA Identities and locations.",
			"FIeldName": "fromIP",
			"InsightCriterias": {
				"6": [
					"103.21.207.99",
					"129.78.110.124",
					"183.89.36.226"
				]
			},
			"Type": 1
		},
{
			"InsightTitle": "Copilot AI",
			"InsightMessage": "The relatively high transaction fee compared to the transaction amount could raise questions.",
			"FIeldName": "TransactionID",
			"InsightCriterias": {
				"95": [
					"abd16177-e155-11ee-9c3c-02420a000303"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Transaction Timing",
			"InsightMessage": "The quick turnaround of funds between the accounts could be a red flag",
			"FIeldName": "accountNumber",
			"InsightCriterias": {
				"9": [
					"7869660",
					"7763461"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Unusual Business Relationships",
			"InsightMessage": "The nature  of these transactions might not align with the account  typical business activities. ",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"837637867",
					"825433533",
					"835646335",
					"821134424",
					"868024575"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Lack of substance and employees",
			"InsightMessage": "The number of employees at Metal security LTD, is relatively small compared to cash flow and the number of transactions.",
			"FIeldName": "accountNumber",
			"InsightCriterias": {
				"9": [
					"7869660"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "Common shareholders",
			"InsightMessage": "Two external accounts of Shield Construction and Car Rent LTD  are held by the same shareholders",
			"FIeldName": "counterAccount",
			"InsightCriterias": {
				"9": [
					"82763988",
					"142107"
				]
			},
			"Type": 1
		},
		{
			"InsightTitle": "Prepaid Deposit",
			"InsightMessage": "Recurring deposits to prepaid cards in small amounts",
			"FIeldName": "accountNumber",
			"InsightCriterias": {
				"9": [
					"7869660",
					"7763461"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Recurring Transactions",
			"InsightMessage": "Recurring deposits between several companies at a fixed percentage.",
			"FIeldName": "accountNumber",
			"InsightCriterias": {
				"9": [
					"7869660",
					"7763461"
				]
			},
			"Type": 3
		},
		{
			"InsightTitle": "High Value non-profit Transactions",
			"InsightMessage": "Many recurring deposits to a non-profit organization: Friends non-profit.",
			"FIeldName": "counterHolderName",
			"InsightCriterias": {
				"9": [
					"Friends"
				]
			},
			"Type": 2
		},
		{
			"InsightTitle": "Transactions between relatives",
			"InsightMessage": "Transactions between accounts of relatives.",
			"FIeldName":"toHolder",
			"InsightCriterias": {
				"9": [
					"Shield Construction",
					"PM MA 24 LTD"
				]
			},
			"Type": 1
		}

	]
}	