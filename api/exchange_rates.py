import asyncio
import os
import logging
from typing import Callable, NamedTuple
import math
import httpx


lookup= {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN':logging.WARN,
    }
logging.basicConfig(level=lookup['INFO'])
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

currencies = {
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


class Provider(NamedTuple):
    name: str
    domain: str
    api_url: str
    getter: Callable


exchange_rate_providers = {
    "coinbase": Provider(
        "Coinbase",
        "coinbase.com",
        "https://api.coinbase.com/v2/exchange-rates?currency={FROM}",
        lambda data, replacements: data["data"]["rates"][replacements["TO"]],
    ),
    "kraken": Provider(
        "Kraken",
        "kraken.com",
        "https://api.kraken.com/0/public/Ticker?pair=XRP{TO}",
        lambda data, replacements: data["result"]["XXRPZ" + replacements["TO"]]["c"][0],
    ),
}


async def xrp_price(currency: str) -> float:
    replacements = {
        "FROM": "XRP",
        "from": "xrp",
        "TO": currency.upper(),
        "to": currency.lower(),
    }
    rates = []
    tasks = []

    send_channel = asyncio.Queue()

    async def controller():
        failures = 0
        while True:
            rate = await send_channel.get()
            
            if rate:
                rates.append(rate)
            else:
                failures += 1

            if len(rates) >= 2 or len(rates) == 1 and failures >= 2:
                for t in tasks:
                    t.cancel()
                break
            if failures == len(exchange_rate_providers):
                for t in tasks:
                    t.cancel()
                break

    async def fetch_price(provider: Provider):
        url = provider.api_url.format(**replacements)
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=1.0)
                r.raise_for_status()
                data = r.json()
                logger.info(f"- Got data from {provider.name}")
                rate = float(provider.getter(data, replacements))
                await send_channel.put(rate)
        except (
            TypeError,  # CoinMate returns HTTPStatus 200 but no data when a currency pair is not found
            KeyError,  # Kraken's response dictionary doesn't include keys we look up for
            httpx.ConnectTimeout,
            httpx.ConnectError,
            httpx.ReadTimeout,
            httpx.HTTPStatusError,  # Some providers throw a 404 when a currency pair is not found
        ):
            await send_channel.put(None)

    asyncio.create_task(controller())
    for _, provider in exchange_rate_providers.items():
        tasks.append(asyncio.create_task(fetch_price(provider)))

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass

    if not rates:
        return 9999999999
    elif len(rates) == 1:
        logger.info("Warning could only fetch one XRP price.")

    return sum([rate for rate in rates]) / len(rates)

async def dropsToXrp(drops:int) -> float:
    return (drops / 1000000)

async def dropsToXrp(xrp:float) -> int:
    return int(xrp * 1000000)



# async def get_fiat_rate_satoshis(currency: str) -> float:
#     return float(100_000_000 / (await xrp_price(currency)))


# async def fiat_amount_as_satoshis(amount: float, currency: str) -> int:
#     return int(amount * (await get_fiat_rate_satoshis(currency)))


# async def satoshis_amount_as_fiat(amount: float, currency: str) -> float:
#     return float(amount / (await get_fiat_rate_satoshis(currency)))

# def get_fiat_rate_pos(currency: str, rate: float, price: float):
#     if currency != 'SAT':
#         # allow some fluctuation (as the fiat price may have changed between the calls)
#         min = int(math.ceil(rate * price))
#         max = int(math.ceil(rate * price))
#     else:
#         min = int(math.ceil(price))
#         max = int(math.ceil(price))

#     return (min, max)

# def get_fiat_rate_min_max(currency: str, rate: float, price: float):
#     if currency != 'SAT':
#         # allow some fluctuation (as the fiat price may have changed between the calls)
#         min = int(math.ceil(rate * price)* 1000)
#         max = int(math.ceil(rate * price)* 1000)
#     else:
#         min = int(math.ceil(price)* 1000)
#         max = int(math.ceil(price)* 1000)

#     return (min, max)
