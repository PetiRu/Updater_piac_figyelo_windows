def get_usa_reszvenyek():
    """USA Részvény Csomag - Amerikai részvények"""
    usa_stocks = [
        # Technology - Mega Cap
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AVGO',
        'ORCL', 'CRM', 'ADBE', 'CSCO', 'TXN', 'ACN', 'IBM', 'QCOM',
        'AMD', 'INTC', 'INTU', 'NOW', 'AMAT', 'UBER', 'SNPS', 'ADP',
        'CRWD', 'PANW', 'MSI', 'FTNT', 'CDNS', 'KLAC', 'MRVL', 'ANET',
        'LRCX', 'TEL', 'MPWR', 'NXPI', 'APH', 'GLW', 'HPQ', 'JBL',
        
        # Technology - Software & Services
        'ADSK', 'CTSH', 'FIS', 'FISV', 'GPN', 'JKHY', 'MA', 'MCHP',
        'MU', 'NET', 'PAYX', 'PYPL', 'SQ', 'TER', 'TSM', 'TYL',
        'V', 'VRSN', 'WDAY', 'ZI', 'ZM', 'DOCU', 'MDB', 'DDOG',
        'TEAM', 'OKTA', 'SPLK', 'ESTC', 'MSTR', 'CFLT', 'SNOW', 'PLTR',
        
        # Healthcare - Pharmaceuticals & Biotech
        'JNJ', 'PFE', 'ABBV', 'MRK', 'TMO', 'LLY', 'AMGN', 'GILD',
        'BMY', 'VRTX', 'REGN', 'BIIB', 'CVS', 'CI', 'HUM', 'ELV',
        'UNH', 'DHR', 'BDX', 'ISRG', 'SYK', 'ZTS', 'IDXX', 'EW',
        'DXCM', 'TFX', 'RMD', 'HCA', 'UHS', 'LH', 'DGX', 'COO',
        
        # Financial Services - Banks & Insurance
        'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'SCHW', 'BLK',
        'AXP', 'V', 'MA', 'PYPL', 'SPGI', 'MCO', 'ICE', 'NDAQ',
        'CME', 'FIS', 'FISV', 'AJG', 'MMC', 'AON', 'WRB', 'TRV',
        'ALL', 'CB', 'AIG', 'MET', 'PRU', 'L', 'AFL', 'PFG',
        
        # Consumer Discretionary - Retail & Automotive
        'TSLA', 'F', 'GM', 'NIO', 'RIVN', 'LCID', 'AMZN', 'HD',
        'LOW', 'TGT', 'WMT', 'COST', 'TJX', 'ROST', 'BURL', 'DLTR',
        'DG', 'BBY', 'BKE', 'ANF', 'URBN', 'DKS', 'TSCO', 'AZO',
        'ORLY', 'KMX', 'LAD', 'PAG', 'ABG', 'CVNA', 'M', 'KSS',
        
        # Consumer Staples - Food & Beverage
        'PG', 'KO', 'PEP', 'CL', 'KMB', 'MO', 'PM', 'STZ',
        'TAP', 'BUD', 'SAM', 'COKE', 'FIZZ', 'MNST', 'KDP', 'CELH',
        'CAG', 'GIS', 'K', 'MKC', 'SJM', 'HSY', 'LW', 'TSN',
        'CPB', 'HRL', 'SYY', 'ADM', 'BG', 'INGR', 'LANC', 'CVGW',
        
        # Industrial - Manufacturing & Defense
        'BA', 'LMT', 'RTX', 'NOC', 'GD', 'HII', 'LHX', 'CW',
        'TDG', 'HEI', 'COL', 'TXT', 'DE', 'CAT', 'CNHI', 'AGCO',
        'CMI', 'PCAR', 'ALSN', 'WAB', 'GE', 'HON', 'EMR', 'DOV',
        'ITW', 'ETN', 'ROK', 'SWK', 'SNA', 'GGG', 'MIDD', 'AME',
        
        # Energy - Oil & Gas
        'XOM', 'CVX', 'COP', 'EOG', 'MPC', 'PSX', 'VLO', 'DVN',
        'OXY', 'HES', 'FANG', 'PXD', 'MRO', 'CTRA', 'EQT', 'RRC',
        'APA', 'CHK', 'MTDR', 'SWN', 'AR', 'OVV', 'TPL', 'WDS',
        'SHEL', 'BP', 'TTE', 'EQNR', 'PBR', 'VIST', 'LNG', 'KMI',
        
        # Healthcare - Medical Devices & Services
        'ABT', 'BSX', 'BDX', 'DXCM', 'EW', 'IDXX', 'ISRG', 'MDT',
        'RMD', 'SYK', 'TMO', 'ZBH', 'ALC', 'BAX', 'CNC', 'HUM',
        'IQV', 'MCK', 'WST', 'XRAY', 'CHE', 'DVA', 'EHC', 'UHS',
        
        # Real Estate - REITs
        'AMT', 'CCI', 'DLR', 'EQIX', 'EXR', 'IRM', 'PSA', 'O',
        'SPG', 'VTR', 'WELL', 'WPC', 'AVB', 'EQR', 'MAA', 'UDR',
        'ARE', 'BXP', 'DEI', 'FRT', 'KIM', 'REG', 'SLG', 'VNO',
        
        # Utilities - Electric & Gas
        'NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL', 'WEC',
        'ES', 'PEG', 'ED', 'EIX', 'FE', 'AES', 'AWK', 'CNP',
        'SRE', 'LNT', 'DTE', 'CMS', 'ATO', 'NI', 'BKH', 'OGS',
        
        # Communication Services - Telecom & Media
        'T', 'VZ', 'TMUS', 'CMCSA', 'DIS', 'NFLX', 'WBD', 'PARA',
        'FOX', 'LSXMK', 'CHTR', 'LBRDK', 'TTWO', 'EA', 'ATVI', 'ROKU',
        'TTD', 'PINS', 'SNAP', 'MTCH', 'BIDU', 'JD', 'PDD', 'BABA',
        
        # Materials - Chemicals & Mining
        'LIN', 'APD', 'SHW', 'ECL', 'PPG', 'ALB', 'FCX', 'NEM',
        'GOLD', 'AU', 'AA', 'CLF', 'STLD', 'NUE', 'RS', 'VMC',
        'MLM', 'VALE', 'SCCO', 'MOS', 'CF', 'NTR', 'IP', 'WRK',
        
        # Transportation & Logistics
        'UPS', 'FDX', 'EXPD', 'CHRW', 'XPO', 'ODFL', 'SAIA', 'JBHT',
        'LSTR', 'HUBG', 'KNX', 'WERN', 'ARCB', 'PTSI', 'YELL', 'UAL',
        'DAL', 'AAL', 'LUV', 'JBLU', 'ALK', 'HA', 'SKYW', 'UHAL',
        
        # Specialty - Business Services
        'GWW', 'FAST', 'MSM', 'NDSN', 'PNR', 'IT', 'JKHY', 'PAYC',
        'EFX', 'TRU', 'CBOE', 'CINF', 'RLI', 'RNR', 'AFG', 'BRO',
        
        # Emerging Growth & Innovation
        'RIVN', 'LCID', 'NIO', 'XPEV', 'LI', 'BYDDY', 'PLUG', 'FCEL',
        'BLDP', 'BE', 'CHPT', 'EVGO', 'QS', 'ENPH', 'SEDG', 'FSLR',
        'RUN', 'NOVA', 'ARRY', 'SHOP', 'CRSP', 'EDIT', 'NTLA', 'BEAM',
        
        # Small & Mid Cap Leaders
        'ANET', 'MRNA', 'BNTX', 'ZS', 'CRWD', 'DDOG', 'NET', 'ASAN',
        'UPST', 'COIN', 'HOOD', 'SOFI', 'AFRM', 'PATH', 'U', 'SNOW',
        'DASH', 'ABNB', 'EXFY', 'APP', 'DBX', 'TWLO', 'FVRR', 'PINS'
    ]
    return usa_stocks

def get_usa_cegnevek_szotara():
    """Cégnév szótár USA részvényekhez"""
    cegnevek = {
        # Technology - Mega Cap
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc. (Google)',
        'AMZN': 'Amazon.com Inc.',
        'NVDA': 'NVIDIA Corporation',
        'META': 'Meta Platforms Inc.',
        'TSLA': 'Tesla Inc.',
        'AVGO': 'Broadcom Inc.',
        'ORCL': 'Oracle Corporation',
        'CRM': 'Salesforce Inc.',
        'ADBE': 'Adobe Inc.',
        'CSCO': 'Cisco Systems Inc.',
        'TXN': 'Texas Instruments',
        'ACN': 'Accenture plc',
        'IBM': 'International Business Machines',
        'QCOM': 'Qualcomm Inc.',
        'AMD': 'Advanced Micro Devices',
        'INTC': 'Intel Corporation',
        'INTU': 'Intuit Inc.',
        'NOW': 'ServiceNow Inc.',
        
        # Healthcare
        'JNJ': 'Johnson & Johnson',
        'PFE': 'Pfizer Inc.',
        'ABBV': 'AbbVie Inc.',
        'MRK': 'Merck & Co.',
        'TMO': 'Thermo Fisher Scientific',
        'LLY': 'Eli Lilly and Company',
        'AMGN': 'Amgen Inc.',
        'GILD': 'Gilead Sciences',
        'BMY': 'Bristol-Myers Squibb',
        'UNH': 'UnitedHealth Group',
        
        # Financial Services
        'JPM': 'JPMorgan Chase & Co.',
        'BAC': 'Bank of America',
        'WFC': 'Wells Fargo & Company',
        'C': 'Citigroup Inc.',
        'GS': 'Goldman Sachs Group',
        'MS': 'Morgan Stanley',
        'V': 'Visa Inc.',
        'MA': 'Mastercard Inc.',
        
        # Consumer
        'PG': 'Procter & Gamble',
        'KO': 'Coca-Cola Company',
        'PEP': 'PepsiCo Inc.',
        'WMT': 'Walmart Inc.',
        'COST': 'Costco Wholesale',
        'HD': 'Home Depot',
        'LOW': "Lowe's Companies",
        'TGT': 'Target Corporation',
        
        # Industrial
        'BA': 'Boeing Company',
        'CAT': 'Caterpillar Inc.',
        'DE': 'Deere & Company',
        'GE': 'General Electric',
        'HON': 'Honeywell International',
        
        # Energy
        'XOM': 'Exxon Mobil Corporation',
        'CVX': 'Chevron Corporation',
        'COP': 'ConocoPhillips',
        'SLB': 'Schlumberger NV',
        
        # Communication Services
        'T': 'AT&T Inc.',
        'VZ': 'Verizon Communications',
        'DIS': 'Walt Disney Company',
        'NFLX': 'Netflix Inc.',
        'CMCSA': 'Comcast Corporation',
        
        # Real Estate
        'AMT': 'American Tower Corporation',
        'PLD': 'Prologis Inc.',
        'CCI': 'Crown Castle International',
        'EQIX': 'Equinix Inc.',
        
        # Utilities
        'NEE': 'NextEra Energy',
        'DUK': 'Duke Energy',
        'SO': 'Southern Company',
        'D': 'Dominion Energy',
        
        # Materials
        'LIN': 'Linde plc',
        'APD': 'Air Products & Chemicals',
        'SHW': 'Sherwin-Williams',
        
        # Transportation
        'UPS': 'United Parcel Service',
        'FDX': 'FedEx Corporation',
        
        # Additional major companies
        'ABT': 'Abbott Laboratories',
        'ADP': 'Automatic Data Processing',
        'BDX': 'Becton Dickinson',
        'BLK': 'BlackRock Inc.',
        'CB': 'Chubb Limited',
        'CL': 'Colgate-Palmolive',
        'CMG': 'Chipotle Mexican Grill',
        'COF': 'Capital One Financial',
        'DHR': 'Danaher Corporation',
        'EL': 'Estée Lauder Companies',
        'EMR': 'Emerson Electric',
        'F': 'Ford Motor Company',
        'FDX': 'FedEx Corporation',
        'GD': 'General Dynamics',
        'GM': 'General Motors',
        'GSK': 'GlaxoSmithKline',
        'HCA': 'HCA Healthcare',
        'ICE': 'Intercontinental Exchange',
        'ISRG': 'Intuitive Surgical',
        'ITW': 'Illinois Tool Works',
        'LMT': 'Lockheed Martin',
        'LRCX': 'Lam Research',
        'MMM': '3M Company',
        'MO': 'Altria Group',
        'MRVL': 'Marvell Technology',
        'NEE': 'NextEra Energy',
        'NKE': 'Nike Inc.',
        'NOC': 'Northrop Grumman',
        'NSC': 'Norfolk Southern',
        'NUE': 'Nucor Corporation',
        'PM': 'Philip Morris International',
        'PNC': 'PNC Financial Services',
        'RTX': 'Raytheon Technologies',
        'SBUX': 'Starbucks Corporation',
        'SYK': 'Stryker Corporation',
        'TFC': 'Truist Financial',
        'TJX': 'TJX Companies',
        'TMO': 'Thermo Fisher Scientific',
        'TXN': 'Texas Instruments',
        'UNP': 'Union Pacific',
        'USB': 'U.S. Bancorp',
        'VZ': 'Verizon Communications',
        'WBA': 'Walgreens Boots Alliance',
        'WFC': 'Wells Fargo',
        'WMT': 'Walmart',
        'ZTS': 'Zoetis Inc.',
        
        # Emerging Technology
        'SNOW': 'Snowflake Inc.',
        'DDOG': 'Datadog Inc.',
        'NET': 'Cloudflare Inc.',
        'CRWD': 'CrowdStrike Holdings',
        'ZS': 'Zscaler Inc.',
        'MDB': 'MongoDB Inc.',
        'PLTR': 'Palantir Technologies',
        'SHOP': 'Shopify Inc.',
        'SQ': 'Block Inc. (Square)',
        'PYPL': 'PayPal Holdings',
        'UBER': 'Uber Technologies',
        'LYFT': 'Lyft Inc.',
        'DASH': 'DoorDash Inc.',
        'ABNB': 'Airbnb Inc.',
        'ROKU': 'Roku Inc.',
        'SPOT': 'Spotify Technology',
        'SNAP': 'Snap Inc.',
        'TWTR': 'Twitter Inc.',
        'PINS': 'Pinterest Inc.',
        'MTCH': 'Match Group',
        'ZM': 'Zoom Video Communications',
        'DOCU': 'DocuSign Inc.',
        'TEAM': 'Atlassian Corporation',
        'OKTA': 'Okta Inc.',
        'SPLK': 'Splunk Inc.',
        'ESTC': 'Elastic NV',
        'MSTR': 'MicroStrategy',
        'CFLT': 'Confluent Inc.',
        'ASAN': 'Asana Inc.',
        'UPST': 'Upstart Holdings',
        'COIN': 'Coinbase Global',
        'HOOD': 'Robinhood Markets',
        'SOFI': 'SoFi Technologies',
        'AFRM': 'Affirm Holdings',
        'PATH': 'UiPath Inc.',
        'U': 'Unity Software',
        'RIVN': 'Rivian Automotive',
        'LCID': 'Lucid Group',
        'NIO': 'NIO Inc.',
        'XPEV': 'XPeng Inc.',
        'LI': 'Li Auto Inc.',
        'PLUG': 'Plug Power',
        'FCEL': 'FuelCell Energy',
        'ENPH': 'Enphase Energy',
        'SEDG': 'SolarEdge Technologies',
        'FSLR': 'First Solar',
        'RUN': 'Sunrun Inc.'
    }
    return cegnevek

def get_usa_cegnev(szimbólum):
    """Visszaadja a szimbólumhoz tartozó cégnevet"""
    cegnevek = get_usa_cegnevek_szotara()
    return cegnevek.get(szimbólum, "Ismeretlen cég")

def get_usa_reszveny_szamlalo():
    """Visszaadja a megfigyelt USA részvények számát"""
    return len(get_usa_reszvenyek())
