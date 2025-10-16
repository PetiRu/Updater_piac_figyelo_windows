def get_world_reszvenyek():
    """World Részvény Csomag - Világ részvényei"""
    world_stocks = [
        # USA Stocks (200 legnagyobb)
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
        'UNH', 'JNJ', 'XOM', 'JPM', 'V', 'PG', 'MA', 'CVX',
        'HD', 'LLY', 'AVGO', 'MRK', 'ABBV', 'KO', 'PEP', 'WMT',
        'TMO', 'COST', 'DIS', 'PFE', 'ABT', 'NFLX', 'CRM', 'ACN',
        'DHR', 'ADBE', 'NKE', 'TXN', 'CMCSA', 'RTX', 'UPS', 'ORCL',
        'PM', 'LIN', 'LOW', 'UNP', 'IBM', 'SPGI', 'CAT', 'AXP',
        'AMGN', 'DE', 'GS', 'PLD', 'SBUX', 'ISRG', 'VZ', 'T',
        'LMT', 'NEE', 'BKNG', 'MDT', 'SYK', 'COP', 'NOC', 'CI',
        'ELV', 'GE', 'C', 'HON', 'LRCX', 'ETN', 'PGR', 'BLK',
        'ADI', 'AMAT', 'TJX', 'DELL', 'BSX', 'MMC', 'SCHW', 'GILD',
        'CVS', 'INTU', 'PYPL', 'MO', 'SO', 'DUK', 'BDX', 'APD',
        'CL', 'EOG', 'F', 'GM', 'ITW', 'MCD', 'NSC', 'PNC',
        'TGT', 'USB', 'WM', 'AON', 'CSX', 'GD', 'ICE', 'JCI',
        'KMB', 'MCO', 'MET', 'MS', 'NEM', 'PXD', 'SRE', 'TFC',
        'TRV', 'VLO', 'WFC', 'WMB', 'ZTS', 'AEP', 'AIG', 'ALL',
        'BA', 'CARR', 'CB', 'CME', 'CNC', 'COF', 'CTAS', 'CTVA',
        'D', 'DHI', 'DOW', 'DTE', 'EA', 'ECL', 'EMR', 'EXC',
        'FIS', 'FISV', 'FLT', 'FDX', 'GLW', 'HCA', 'HUM', 'IDXX',
        'ILMN', 'IT', 'J', 'KDP', 'KHC', 'KMI', 'LEN', 'LHX',
        'LLY', 'MAR', 'MCHP', 'MCK', 'MDLZ', 'MPC', 'MRVL', 'NUE',
        'ODFL', 'OKE', 'PCAR', 'PEG', 'PH', 'PSA', 'PSX', 'QCOM',
        'REG', 'RJF', 'ROP', 'RSG', 'SLB', 'SNPS', 'SPG', 'SWK',
        'TEL', 'TT', 'TXN', 'VRSK', 'WAB', 'WEC', 'WELL', 'WST',
        'XEL', 'ZBH',

        # European Stocks (150 legnagyobb)
        # German DAX
        'ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BMW.DE', 'CON.DE',
        '1COV.DE', 'DAI.DE', 'DBK.DE', 'DB1.DE', 'DHL.DE', 'DTE.DE',
        'EOAN.DE', 'FRE.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE', 'MBG.DE',
        'MRK.DE', 'MTX.DE', 'MUV2.DE', 'RWE.DE', 'SAP.DE', 'SIE.DE',
        'VOW3.DE',
        # French CAC 40
        'AC.PA', 'AI.PA', 'AIR.PA', 'ALO.PA', 'BNP.PA', 'EN.PA',
        'CS.PA', 'CAP.PA', 'CA.PA', 'ACA.PA', 'BN.PA', 'DSY.PA',
        'EDF.PA', 'FTI.PA', 'EL.PA', 'RF.PA', 'ERF.PA', 'ENGI.PA',
        'KER.PA', 'OR.PA', 'LR.PA', 'MC.PA', 'ML.PA', 'ORA.PA',
        'RI.PA', 'PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA',
        'SU.PA', 'GLE.PA', 'STLA.PA', 'TEP.PA', 'HO.PA', 'FP.PA',
        'URW.PA', 'VIE.PA', 'DG.PA', 'VIV.PA',
        # UK FTSE 100
        'AAL.L', 'ABF.L', 'ADM.L', 'AHT.L', 'ANTO.L', 'AUTO.L',
        'AV.L', 'AZN.L', 'BA.L', 'BARC.L', 'BATS.L', 'BLT.L',
        'BP.L', 'CCH.L', 'CNA.L', 'CPG.L', 'CRH.L', 'DGE.L',
        'EXPN.L', 'FLTR.L', 'GLEN.L', 'GSK.L', 'HLMA.L', 'HSBA.L',
        'IMB.L', 'III.L', 'ITRK.L', 'LLOY.L', 'LSEG.L', 'MNG.L',
        'NG.L', 'NXT.L', 'OCDO.L', 'PRU.L', 'PSON.L', 'RB.L',
        'REL.L', 'RIO.L', 'RR.L', 'RTO.L', 'SGE.L', 'SGRO.L',
        'SMT.L', 'SN.L', 'SPX.L', 'SSE.L', 'STAN.L', 'TSCO.L',
        'ULVR.L', 'VOD.L', 'WEIR.L', 'WPP.L',
        # Swiss
        'ABBN.SW', 'ADEN.SW', 'CSGN.SW', 'GIVN.SW', 'LONN.SW',
        'NESN.SW', 'NOVN.SW', 'ROG.SW', 'SGSN.SW', 'UBSG.SW',
        'ZURN.SW',
        # Dutch
        'AD.AS', 'AGN.AS', 'AKZA.AS', 'ASML.AS', 'DSM.AS',
        'HEIA.AS', 'INGA.AS', 'KPN.AS', 'NN.AS', 'PHIA.AS',
        'RAND.AS', 'UNA.AS', 'WKL.AS',
        # Italian
        'AZM.MI', 'CPR.MI', 'ENEL.MI', 'ENI.MI', 'G.MI',
        'ISP.MI', 'LDO.MI', 'MB.MI', 'MONC.MI', 'PST.MI',
        'RACE.MI', 'SPM.MI', 'SRG.MI', 'STLA.MI', 'TIT.MI',
        'UCG.MI',
        # Spanish
        'ANA.MC', 'BBVA.MC', 'CABK.MC', 'ELE.MC', 'ENG.MC',
        'FER.MC', 'GRF.MC', 'IAG.MC', 'IBE.MC', 'ITX.MC',
        'MAP.MC', 'MTS.MC', 'REP.MC', 'SAN.MC', 'TEF.MC',
        'VIS.MC',

        # Canadian Stocks (50 legnagyobb)
        'RY.TO', 'TD.TO', 'ENB.TO', 'CNR.TO', 'BNS.TO',
        'BMO.TO', 'TRP.TO', 'MFC.TO', 'SU.TO', 'CP.TO',
        'ATD.TO', 'GIB-A.TO', 'WCN.TO', 'CSU.TO', 'TRI.TO',
        'L.TO', 'NTR.TO', 'ABX.TO', 'SHOP.TO', 'BAM-A.TO',
        'POW.TO', 'SLF.TO', 'AQN.TO', 'CM.TO', 'CTC-A.TO',
        'DOL.TO', 'MRU.TO', 'RCI-B.TO', 'TFII.TO', 'WPM.TO',
        'CCL-B.TO', 'FTS.TO', 'K.TO', 'MG.TO', 'NVEI.TO',
        'OTEX.TO', 'QSR.TO', 'SAP.TO', 'T.TO', 'X.TO',
        'AC.TO', 'BB.TO', 'CAR-UN.TO', 'CCO.TO', 'CNQ.TO',
        'CU.TO', 'DOO.TO', 'EMP-A.TO', 'FFH.TO', 'IMO.TO',

        # Chinese Stocks (100 legnagyobb)
        # US-listed Chinese stocks
        'BABA', 'PDD', 'JD', 'BIDU', 'NIO', 'TCEHY',
        'BILI', 'IQ', 'TCOM', 'VIPS', 'ZH', 'YUMC',
        'EDU', 'TME', 'WB', 'MOMO', 'NTES', 'DAO',
        'XPEV', 'LI', 'BZUN', 'HUYA', 'DOYU', 'FINV',
        'HTHT', 'JMIA', 'KC', 'MKD', 'QFIN', 'RERE',
        'TIGR', 'YALA', 'ZTO', 'DADA', 'GDS', 'BEKE',
        # Hong Kong listed
        '0700.HK', '0939.HK', '1398.HK', '0388.HK', '0941.HK',
        '0005.HK', '1299.HK', '2318.HK', '3988.HK', '2628.HK',
        '0883.HK', '1088.HK', '0762.HK', '0016.HK', '0011.HK',
        '2388.HK', '3328.HK', '3968.HK', '1810.HK', '1024.HK',
        '9618.HK', '3690.HK', '9988.HK', '2688.HK', '2015.HK',
        '2269.HK', '1876.HK', '6060.HK', '1951.HK', '9961.HK',
        # Shanghai/Shenzhen A-shares (selected)
        '601318.SS', '600036.SS', '000858.SZ', '600519.SS',
        '000333.SZ', '002415.SZ', '600276.SS', '000001.SZ',
        '601888.SS', '300750.SZ', '601398.SS', '601328.SS',
        '601288.SS', '601166.SS', '600900.SS', '601919.SS',
        '601668.SS', '601390.SS', '601766.SS', '601186.SS',
        '600048.SS', '600028.SS', '600104.SS', '600309.SS',
        '600887.SS', '600585.SS', '601818.SS', '601088.SS',
        '601857.SS', '601628.SS'
    ]
    return world_stocks

def get_world_cegnevek_szotara():
    """Cégnév szótár világ részvényeihez"""
    cegnevek = {
        # USA Stocks
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc. (Google)',
        'AMZN': 'Amazon.com Inc.',
        'NVDA': 'NVIDIA Corporation',
        'META': 'Meta Platforms Inc.',
        'TSLA': 'Tesla Inc.',
        'BRK-B': 'Berkshire Hathaway',
        'UNH': 'UnitedHealth Group',
        'JNJ': 'Johnson & Johnson',
        'XOM': 'Exxon Mobil',
        'JPM': 'JPMorgan Chase',
        'V': 'Visa Inc.',
        'PG': 'Procter & Gamble',
        'MA': 'Mastercard',
        'CVX': 'Chevron Corporation',
        'HD': 'Home Depot',
        'LLY': 'Eli Lilly',
        'AVGO': 'Broadcom',
        'MRK': 'Merck & Co.',

        # European Stocks
        # German
        'ADS.DE': 'Adidas',
        'ALV.DE': 'Allianz',
        'BAS.DE': 'BASF',
        'BAYN.DE': 'Bayer',
        'BMW.DE': 'BMW',
        'SAP.DE': 'SAP',
        'SIE.DE': 'Siemens',
        'VOW3.DE': 'Volkswagen',
        # French
        'AIR.PA': 'Airbus',
        'MC.PA': 'LVMH',
        'OR.PA': "L'Oreal",
        'SAN.PA': 'Sanofi',
        'TTE.PA': 'TotalEnergies',
        # UK
        'AZN.L': 'AstraZeneca',
        'HSBA.L': 'HSBC',
        'BP.L': 'BP',
        'GLEN.L': 'Glencore',
        'ULVR.L': 'Unilever',
        # Swiss
        'NESN.SW': 'Nestle',
        'NOVN.SW': 'Novartis',
        'ROG.SW': 'Roche',
        # Dutch
        'ASML.AS': 'ASML',
        'UNA.AS': 'Unilever',
        # Italian
        'ENEL.MI': 'Enel',
        'ENI.MI': 'Eni',
        # Spanish
        'SAN.MC': 'Santander',
        'TEF.MC': 'Telefonica',

        # Canadian Stocks
        'RY.TO': 'Royal Bank of Canada',
        'TD.TO': 'Toronto-Dominion Bank',
        'ENB.TO': 'Enbridge',
        'CNR.TO': 'Canadian National Railway',
        'BNS.TO': 'Bank of Nova Scotia',
        'BMO.TO': 'Bank of Montreal',
        'TRP.TO': 'TC Energy',
        'SHOP.TO': 'Shopify',
        'SU.TO': 'Suncor Energy',
        'CP.TO': 'Canadian Pacific Railway',
        'GIB-A.TO': 'CGI Inc.',
        'WCN.TO': 'Waste Connections',
        'CSU.TO': 'Constellation Software',
        'TRI.TO': 'Thomson Reuters',
        'L.TO': 'Loblaw Companies',
        'NTR.TO': 'Nutrien',
        'ABX.TO': 'Barrick Gold',
        'BAM-A.TO': 'Brookfield Asset Management',
        'SLF.TO': 'Sun Life Financial',
        'AQN.TO': 'Algonquin Power & Utilities',

        # Chinese Stocks
        # US-listed
        'BABA': 'Alibaba Group',
        'PDD': 'Pinduoduo',
        'JD': 'JD.com',
        'BIDU': 'Baidu',
        'NIO': 'NIO Inc.',
        'TCEHY': 'Tencent Holdings',
        'XPEV': 'XPeng Inc.',
        'LI': 'Li Auto',
        'BILI': 'Bilibili',
        'IQ': 'iQiyi',
        'TCOM': 'Trip.com',
        'EDU': 'New Oriental Education',
        'TME': 'Tencent Music',
        'ZTO': 'ZTO Express',
        'BEKE': 'KE Holdings',
        # Hong Kong
        '0700.HK': 'Tencent Holdings',
        '0939.HK': 'China Construction Bank',
        '1398.HK': 'Industrial and Commercial Bank of China',
        '0388.HK': 'Hong Kong Exchanges and Clearing',
        '0941.HK': 'China Mobile',
        '0005.HK': 'HSBC Holdings',
        '1299.HK': 'AIA Group',
        '2318.HK': 'Ping An Insurance',
        '2628.HK': 'China Life Insurance',
        '0883.HK': 'CNOOC',
        '1024.HK': 'Kuaishou Technology',
        '9618.HK': 'JD.com',
        '3690.HK': 'Meituan',
        '9988.HK': 'Alibaba Group',
        # A-shares
        '601318.SS': 'Ping An Insurance',
        '600036.SS': 'China Merchants Bank',
        '000858.SZ': 'Wuliangye Yibin',
        '600519.SS': 'Kweichow Moutai',
        '000333.SZ': 'Midea Group',
        '002415.SZ': 'Hikvision',
        '600276.SS': 'Jiangsu Hengrui Medicine',
        '000001.SZ': 'Ping An Bank',
        '601888.SS': 'China Tourism Group Duty Free',
        '300750.SZ': 'Contemporary Amperex Technology (CATL)',
        '601398.SS': 'ICBC',
        '601328.SS': 'Bank of Communications',
        '601288.SS': 'Agricultural Bank of China',
        '601166.SS': 'Industrial Bank',
        '600900.SS': 'China Yangtze Power',
        '601919.SS': 'COSCO Shipping',
        '601668.SS': 'China State Construction Engineering',
        '601390.SS': 'China Railway Group',
        '601766.SS': 'CRRC Corporation',
        '601186.SS': 'China Railway Construction',
        '600048.SS': 'Poly Real Estate',
        '600028.SS': 'Sinopec',
        '600104.SS': 'SAIC Motor',
        '600309.SS': 'Wanhua Chemical',
        '600887.SS': 'Inner Mongolia Yili Industrial',
        '600585.SS': 'Anhui Conch Cement',
        '601818.SS': 'China Everbright Bank',
        '601088.SS': 'China Shenhua Energy',
        '601857.SS': 'PetroChina',
        '601628.SS': 'China Life Insurance'
    }
    return cegnevek

def get_world_cegnev(szimbólum):
    """Visszaadja a szimbólumhoz tartozó cégnevet"""
    cegnevek = get_world_cegnevek_szotara()
    return cegnevek.get(szimbólum, "Ismeretlen cég")

def get_world_reszveny_szamlalo():
    """Visszaadja a világ részvényeinek számát"""
    return len(get_world_reszvenyek())

def get_regional_breakdown():
    """Visszaadja a régiók szerinti felosztást"""
    stocks = get_world_reszvenyek()
    usa_count = len([s for s in stocks if '.' not in s or '.HK' not in s and '.SS' not in s and '.SZ' not in s])
    europe_count = len([s for s in stocks if any(ext in s for ext in ['.DE', '.PA', '.L', '.SW', '.AS', '.MI', '.MC'])])
    canada_count = len([s for s in stocks if '.TO' in s])
    china_count = len([s for s in stocks if any(ext in s for ext in ['.HK', '.SS', '.SZ']) or s in ['BABA', 'PDD', 'JD', 'BIDU', 'NIO']])
    
    return {
        'USA': usa_count,
        'Europe': europe_count,
        'Canada': canada_count,
        'China': china_count,
        'Total': len(stocks)
    }
