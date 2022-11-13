import deployment from './deployment.json';

export const env = deployment.env;
export const branch = deployment.branch;
export const commitSha = deployment['commit-sha'];


export const wpPluginDownload = () => {
  return `${appUrl}/static/rapaygo-for-woocommerce-1.0.18.zip`
}

// API Key
// 1b144141-440b-4fbc-a064-bfd1bdd3b0ce

// API Secret
// 7acffb42-4c95-4456-aab2-c85d1784bdf7
export const xummConfig = (() => {
  switch (deployment.env) {
    case 'mock':
      return {};
    case 'local':
      return {'api-key': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'api-secret': '7acffb42-4c95-4456-aab2-c85d1784bdf7'};
    case 'dev':
      return {'api-key': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'api-secret': '7acffb42-4c95-4456-aab2-c85d1784bdf7'};
    case 'prd':
      return {'api-key': '1b144141-440b-4fbc-a064-bfd1bdd3b0ce', 'api-secret': '7acffb42-4c95-4456-aab2-c85d1784bdf7'};
  }
})();

export const backendBaseUrl = (() => {
  switch (deployment.env) {
    case 'mock':
      return 'http://localhost:3100'; //use the mock server 
    case 'local':
      return 'http://localhost:5000'; //use the local api server
    case 'dev':
      return 'https://devapi.xurlpay.org/v1';
    case 'prd':
      return 'https://api.xurlpay.org/v1';
  }
})();

export const appUrl = (() => {
  switch (deployment.env) {
    case 'mock':
      return 'https://localhost:3001'; //use the mock server
    case 'local':
      return 'https://localhost:3001'; //use the local api server
    case 'dev':
      return 'https://dev.xurlpay.org';
    case 'prd':
      return 'https://xurlpay.org';
  }
})();

export const deploymentInfo = (() => {
  deployment.dateVal = new Date(parseInt(deployment.timestamp, 10)*1000);
  return deployment;
})();

export const deploymentEnv = (() => {
  return deployment.env;
})();

export const currencyLang = {
  //   ar-SA Arabic Saudi Arabia
  // cs-CZ Czech Czech Republic
  // da-DK Danish Denmark
  // de-DE German Germany
  // el-GR Modern Greek Greece
  // en-AU English Australia
  // en-GB English United Kingdom
  // en-IE English Ireland
  // en-US English United States
  // en-ZA English South Africa
  // es-ES Spanish Spain
  // es-MX Spanish Mexico
  // fi-FI Finnish Finland
  // fr-CA French Canada
  // fr-FR French France
  // he-IL Hebrew Israel
  // hi-IN Hindi India
  // hu-HU Hungarian Hungary
  // id-ID Indonesian Indonesia
  // it-IT Italian Italy
  // ja-JP Japanese Japan
  // ko-KR Korean Republic of Korea
  // nl-BE Dutch Belgium
  // nl-NL Dutch Netherlands
  // no-NO Norwegian Norway
  // pl-PL Polish Poland
  // pt-BR Portuguese Brazil
  // pt-PT Portuguese Portugal
  // ro-RO Romanian Romania
  // ru-RU Russian Russian Federation
  // sk-SK Slovak Slovakia
  // sv-SE Swedish Sweden
  // th-TH Thai Thailand
  // tr-TR Turkish Turkey
  // zh-CN Chinese China
  // zh-HK Chinese Hong Kong
  // zh-TW Chinese Taiwan
      'USD': 'en-US',
      'EUR': 'en-US',
      'GBP': 'en-GB',
      'AUD': 'en-AU',
      'CAD': 'en-CA',
      'CHF': 'fr-FR',
      'CNY': 'zh-CN',
      'HKD': 'zh-HK',
      'JPY': 'ja-JP',
      'KRW': 'ko-KR',
      'NZD': 'en-NZ',
      'SGD': 'en-SG',
      'THB': 'th-TH',
      'TRY': 'tr-TR',
      'ZAR': 'en-ZA',
      'EUR': 'en-US',
      'MXN': 'es-MX',
  
  }
  
  export const currenciesLookup = {
    "AED": "United Arab Emirates Dirham",
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "AMD": "Armenian Dram",
    "ANG": "Netherlands Antillean Gulden",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat",
    "BAM": "Bosnia and Herzegovina Convertible Mark",
    "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka",
    "BGN": "Bulgarian Lev",
    "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc",
    "BMD": "Bermudian Dollar",
    "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano",
    "BRL": "Brazilian Real",
    "BSD": "Bahamian Dollar",
    "BTN": "Bhutanese Ngultrum",
    "BWP": "Botswana Pula",
    "BYN": "Belarusian Ruble",
    "BYR": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    "CAD": "Canadian Dollar",
    "CDF": "Congolese Franc",
    "CHF": "Swiss Franc",
    "CLF": "Unidad de Fomento",
    "CLP": "Chilean Peso",
    "CNH": "Chinese Renminbi Yuan Offshore",
    "CNY": "Chinese Renminbi Yuan",
    "COP": "Colombian Peso",
    "CRC": "Costa Rican Colón",
    "CUC": "Cuban Convertible Peso",
    "CVE": "Cape Verdean Escudo",
    "CZK": "Czech Koruna",
    "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone",
    "DOP": "Dominican Peso",
    "DZD": "Algerian Dinar",
    "EGP": "Egyptian Pound",
    "ERN": "Eritrean Nakfa",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    "FJD": "Fijian Dollar",
    "FKP": "Falkland Pound",
    "GBP": "British Pound",
    "GEL": "Georgian Lari",
    "GGP": "Guernsey Pound",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GMD": "Gambian Dalasi",
    "GNF": "Guinean Franc",
    "GTQ": "Guatemalan Quetzal",
    "GYD": "Guyanese Dollar",
    "HKD": "Hong Kong Dollar",
    "HNL": "Honduran Lempira",
    "HRK": "Croatian Kuna",
    "HTG": "Haitian Gourde",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Sheqel",
    "IMP": "Isle of Man Pound",
    "INR": "Indian Rupee",
    "IQD": "Iraqi Dinar",
    "IRT": "Iranian Toman",
    "ISK": "Icelandic Króna",
    "JEP": "Jersey Pound",
    "JMD": "Jamaican Dollar",
    "JOD": "Jordanian Dinar",
    "JPY": "Japanese Yen",
    "KES": "Kenyan Shilling",
    "KGS": "Kyrgyzstani Som",
    "KHR": "Cambodian Riel",
    "KMF": "Comorian Franc",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "KYD": "Cayman Islands Dollar",
    "KZT": "Kazakhstani Tenge",
    "LAK": "Lao Kip",
    "LBP": "Lebanese Pound",
    "LKR": "Sri Lankan Rupee",
    "LRD": "Liberian Dollar",
    "LSL": "Lesotho Loti",
    "LYD": "Libyan Dinar",
    "MAD": "Moroccan Dirham",
    "MDL": "Moldovan Leu",
    "MGA": "Malagasy Ariary",
    "MKD": "Macedonian Denar",
    "MMK": "Myanmar Kyat",
    "MNT": "Mongolian Tögrög",
    "MOP": "Macanese Pataca",
    "MRO": "Mauritanian Ouguiya",
    "MUR": "Mauritian Rupee",
    "MVR": "Maldivian Rufiyaa",
    "MWK": "Malawian Kwacha",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "MZN": "Mozambican Metical",
    "NAD": "Namibian Dollar",
    "NGN": "Nigerian Naira",
    "NIO": "Nicaraguan Córdoba",
    "NOK": "Norwegian Krone",
    "NPR": "Nepalese Rupee",
    "NZD": "New Zealand Dollar",
    "OMR": "Omani Rial",
    "PAB": "Panamanian Balboa",
    "PEN": "Peruvian Sol",
    "PGK": "Papua New Guinean Kina",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PLN": "Polish Złoty",
    "PYG": "Paraguayan Guaraní",
    "QAR": "Qatari Riyal",
    "RON": "Romanian Leu",
    "RSD": "Serbian Dinar",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan Franc",
    "SAR": "Saudi Riyal",
    "SBD": "Solomon Islands Dollar",
    "SCR": "Seychellois Rupee",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "SHP": "Saint Helenian Pound",
    "SLL": "Sierra Leonean Leone",
    "SOS": "Somali Shilling",
    "SRD": "Surinamese Dollar",
    "SSP": "South Sudanese Pound",
    "STD": "São Tomé and Príncipe Dobra",
    "SVC": "Salvadoran Colón",
    "SZL": "Swazi Lilangeni",
    "THB": "Thai Baht",
    "TJS": "Tajikistani Somoni",
    "TMT": "Turkmenistani Manat",
    "TND": "Tunisian Dinar",
    "TOP": "Tongan Paʻanga",
    "TRY": "Turkish Lira",
    "TTD": "Trinidad and Tobago Dollar",
    "TWD": "New Taiwan Dollar",
    "TZS": "Tanzanian Shilling",
    "UAH": "Ukrainian Hryvnia",
    "UGX": "Ugandan Shilling",
    "USD": "US Dollar",
    "UYU": "Uruguayan Peso",
    "UZS": "Uzbekistan Som",
    "VEF": "Venezuelan Bolívar",
    "VES": "Venezuelan Bolívar Soberano",
    "VND": "Vietnamese Đồng",
    "VUV": "Vanuatu Vatu",
    "WST": "Samoan Tala",
    "XAF": "Central African Cfa Franc",
    "XAG": "Silver (Troy Ounce)",
    "XAU": "Gold (Troy Ounce)",
    "XCD": "East Caribbean Dollar",
    "XDR": "Special Drawing Rights",
    "XOF": "West African Cfa Franc",
    "XPD": "Palladium",
    "XPF": "Cfp Franc",
    "XPT": "Platinum",
    "YER": "Yemeni Rial",
    "ZAR": "South African Rand",
    "ZMW": "Zambian Kwacha",
    "ZWL": "Zimbabwean Dollar",
  }
  

