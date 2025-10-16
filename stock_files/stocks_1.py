def get_eu_reszvenyek():
    """EU Részvény Csomag - Európai részvények"""
    eu_stocks = [
        # German DAX stocks
        'ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BMW.DE', 'CON.DE', 
        '1COV.DE', 'DAI.DE', 'DBK.DE', 'DB1.DE', 'DHL.DE', 'DTE.DE',
        'EOAN.DE', 'FRE.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE', 'MBG.DE',
        'MRK.DE', 'MTX.DE', 'MUV2.DE', 'RWE.DE', 'SAP.DE', 'SIE.DE',
        'VOW3.DE',
        
        # French CAC 40 stocks
        'AC.PA', 'AI.PA', 'AIR.PA', 'ALO.PA', 'BNP.PA', 'EN.PA',
        'CS.PA', 'CAP.PA', 'CA.PA', 'ACA.PA', 'BN.PA', 'DSY.PA',
        'EDF.PA', 'FTI.PA', 'EL.PA', 'RF.PA', 'ERF.PA', 'ENGI.PA',
        'KER.PA', 'OR.PA', 'LR.PA', 'MC.PA', 'ML.PA', 'ORA.PA',
        'RI.PA', 'PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA',
        'SU.PA', 'GLE.PA', 'STLA.PA', 'TEP.PA', 'HO.PA', 'FP.PA',
        'URW.PA', 'VIE.PA', 'DG.PA', 'VIV.PA',
        
        # UK FTSE 100 stocks
        'AAL.L', 'ABF.L', 'ADM.L', 'AHT.L', 'ANTO.L', 'AUTO.L',
        'AV.L', 'AZN.L', 'BA.L', 'BARC.L', 'BATS.L', 'BLT.L',
        'BP.L', 'CCH.L', 'CNA.L', 'CPG.L', 'CRH.L', 'DGE.L',
        'EXPN.L', 'FLTR.L', 'GLEN.L', 'GSK.L', 'HLMA.L', 'HSBA.L',
        'IMB.L', 'III.L', 'ITRK.L', 'LLOY.L', 'LSEG.L', 'MNG.L',
        'MRO.L', 'NG.L', 'NXT.L', 'OCDO.L', 'PRU.L', 'PSON.L',
        'RB.L', 'REL.L', 'RIO.L', 'RR.L', 'RTO.L', 'SGE.L',
        'SGRO.L', 'SMT.L', 'SN.L', 'SPX.L', 'SSE.L', 'STAN.L',
        'TSCO.L', 'ULVR.L', 'VOD.L', 'WEIR.L', 'WPP.L',
        
        # Swiss stocks
        'ABBN.SW', 'ADEN.SW', 'CSGN.SW', 'GIVN.SW', 'LONN.SW',
        'NESN.SW', 'NOVN.SW', 'ROG.SW', 'SGSN.SW', 'UBSG.SW',
        'ZURN.SW',
        
        # Dutch stocks
        'AD.AS', 'AGN.AS', 'AKZA.AS', 'ASML.AS', 'DSM.AS',
        'HEIA.AS', 'INGA.AS', 'KPN.AS', 'NN.AS', 'PHIA.AS',
        'RAND.AS', 'UNA.AS', 'WKL.AS',
        
        # Italian stocks
        'AZM.MI', 'CPR.MI', 'ENEL.MI', 'ENI.MI', 'G.MI',
        'ISP.MI', 'LDO.MI', 'MB.MI', 'MONC.MI', 'PST.MI',
        'RACE.MI', 'SPM.MI', 'SRG.MI', 'STLA.MI', 'TIT.MI',
        'UCG.MI',
        
        # Spanish stocks
        'ANA.MC', 'BBVA.MC', 'CABK.MC', 'ELE.MC', 'ENG.MC',
        'FER.MC', 'GRF.MC', 'IAG.MC', 'IBE.MC', 'ITX.MC',
        'MAP.MC', 'MTS.MC', 'REP.MC', 'SAN.MC', 'TEF.MC',
        'VIS.MC',
        
        # Swedish stocks
        'ALFA.ST', 'ASSA-B.ST', 'ATCO-A.ST', 'ELUX-B.ST',
        'ERIC-B.ST', 'GETI-B.ST', 'HM-B.ST', 'INVE-B.ST',
        'SAND.ST', 'SCA-B.ST', 'SEB-A.ST', 'SHB-A.ST',
        'SWED-A.ST', 'TEL2-B.ST', 'VOLV-B.ST',
        
        # Other European markets
        'ELI.BR', 'SOLB.BR', 'UMI.BR', 'COLO-B.CO', 'DANSKE.CO',
        'NOVO-B.CO', 'ORSTED.CO', 'YAR.OL', 'DNB.OL', 'TEL.OL',
        'EQNR.OL', 'NHY.OL', 'SAMPO.HE', 'UPM.HE', 'NESTE.HE',
        'ORNBV.HE'
    ]
    return eu_stocks

def get_cegnevek_szotara():
    """Cégnév szótár EU részvényekhez"""
    cegnevek = {
        # German DAX stocks
        'ADS.DE': 'Adidas', 'ALV.DE': 'Allianz', 'BAS.DE': 'BASF',
        'BAYN.DE': 'Bayer', 'BMW.DE': 'BMW', 'CON.DE': 'Continental',
        '1COV.DE': 'Covestro', 'DAI.DE': 'Daimler Truck', 'DBK.DE': 'Deutsche Bank',
        'DB1.DE': 'Deutsche Börse', 'DHL.DE': 'DHL', 'DTE.DE': 'Deutsche Telekom',
        'EOAN.DE': 'E.ON', 'FRE.DE': 'Fresenius', 'HEI.DE': 'HeidelbergCement',
        'HEN3.DE': 'Henkel', 'IFX.DE': 'Infineon Technologies', 'MBG.DE': 'Mercedes-Benz Group',
        'MRK.DE': 'Merck', 'MTX.DE': 'MTU Aero Engines', 'MUV2.DE': 'Munich Re',
        'RWE.DE': 'RWE', 'SAP.DE': 'SAP', 'SIE.DE': 'Siemens', 'VOW3.DE': 'Volkswagen',
        
        # French CAC 40 stocks
        'AC.PA': 'Accor', 'AI.PA': 'Air Liquide', 'AIR.PA': 'Airbus',
        'ALO.PA': 'Alstom', 'BNP.PA': 'BNP Paribas', 'EN.PA': 'Bouygues',
        'CS.PA': 'AXA', 'CAP.PA': 'Capgemini', 'CA.PA': 'Carrefour',
        'ACA.PA': 'Crédit Agricole', 'BN.PA': 'Danone', 'DSY.PA': 'Dassault Systèmes',
        'EDF.PA': 'EDF', 'FTI.PA': 'TechnipFMC', 'EL.PA': 'EssilorLuxottica',
        'RF.PA': 'Eurazeo', 'ERF.PA': 'Eurofins Scientific', 'ENGI.PA': 'Engie',
        'KER.PA': 'Kering', 'OR.PA': 'L\'Oréal', 'LR.PA': 'Legrand',
        'MC.PA': 'LVMH', 'ML.PA': 'Michelin', 'ORA.PA': 'Orange',
        'RI.PA': 'Pernod Ricard', 'PUB.PA': 'Publicis Groupe', 'RNO.PA': 'Renault',
        'SAF.PA': 'Safran', 'SGO.PA': 'Saint-Gobain', 'SAN.PA': 'Sanofi',
        'SU.PA': 'Schneider Electric', 'GLE.PA': 'Société Générale', 'STLA.PA': 'Stellantis',
        'TEP.PA': 'Teleperformance', 'HO.PA': 'Thales', 'FP.PA': 'TotalEnergies',
        'URW.PA': 'Unibail-Rodamco-Westfield', 'VIE.PA': 'Veolia', 'DG.PA': 'Vinci',
        'VIV.PA': 'Vivendi',
        
        # UK FTSE 100 stocks
        'AAL.L': 'Anglo American', 'ABF.L': 'Associated British Foods', 'ADM.L': 'Admiral Group',
        'AHT.L': 'Ashtead Group', 'ANTO.L': 'Antofagasta', 'AUTO.L': 'Auto Trader Group',
        'AV.L': 'Aviva', 'AZN.L': 'AstraZeneca', 'BA.L': 'BAE Systems',
        'BARC.L': 'Barclays', 'BATS.L': 'British American Tobacco', 'BLT.L': 'BHP Group',
        'BP.L': 'BP', 'CCH.L': 'Coca-Cola HBC', 'CNA.L': 'Centrica',
        'CPG.L': 'Compass Group', 'CRH.L': 'CRH', 'DGE.L': 'Diageo',
        'EXPN.L': 'Experian', 'FLTR.L': 'Flutter Entertainment', 'GLEN.L': 'Glencore',
        'GSK.L': 'GSK', 'HLMA.L': 'Halma', 'HSBA.L': 'HSBC Holdings',
        'IMB.L': 'Imperial Brands', 'III.L': '3i Group', 'ITRK.L': 'Intertek Group',
        'LLOY.L': 'Lloyds Banking Group', 'LSEG.L': 'London Stock Exchange Group', 'MNG.L': 'M&G',
        'MRO.L': 'Marathon Oil', 'NG.L': 'National Grid', 'NXT.L': 'Next',
        'OCDO.L': 'Ocado Group', 'PRU.L': 'Prudential', 'PSON.L': 'Pearson',
        'RB.L': 'Reckitt Benckiser', 'REL.L': 'RELX', 'RIO.L': 'Rio Tinto',
        'RR.L': 'Rolls-Royce Holdings', 'RTO.L': 'Rentokil Initial', 'SGE.L': 'Sage Group',
        'SGRO.L': 'Segro', 'SMT.L': 'Scottish Mortgage Investment Trust', 'SN.L': 'Smith & Nephew',
        'SPX.L': 'Spirax-Sarco Engineering', 'SSE.L': 'SSE', 'STAN.L': 'Standard Chartered',
        'TSCO.L': 'Tesco', 'ULVR.L': 'Unilever', 'VOD.L': 'Vodafone Group',
        'WEIR.L': 'Weir Group', 'WPP.L': 'WPP',
        
        # Swiss stocks
        'ABBN.SW': 'ABB', 'ADEN.SW': 'Adecco Group', 'CSGN.SW': 'Credit Suisse Group',
        'GIVN.SW': 'Givaudan', 'LONN.SW': 'Lonza Group', 'NESN.SW': 'Nestlé',
        'NOVN.SW': 'Novartis', 'ROG.SW': 'Roche Holding', 'SGSN.SW': 'SGS',
        'UBSG.SW': 'UBS Group', 'ZURN.SW': 'Zurich Insurance Group',
        
        # Dutch stocks
        'AD.AS': 'Ahold Delhaize', 'AGN.AS': 'Aegon', 'AKZA.AS': 'Akzo Nobel',
        'ASML.AS': 'ASML Holding', 'DSM.AS': 'DSM', 'HEIA.AS': 'Heineken',
        'INGA.AS': 'ING Groep', 'KPN.AS': 'KPN', 'NN.AS': 'NN Group',
        'PHIA.AS': 'Philips', 'RAND.AS': 'Randstad', 'UNA.AS': 'Unilever',
        'WKL.AS': 'Wolters Kluwer',
        
        # Italian stocks
        'AZM.MI': 'Azimut Holding', 'CPR.MI': 'Davide Campari', 'ENEL.MI': 'Enel',
        'ENI.MI': 'Eni', 'G.MI': 'Assicurazioni Generali', 'ISP.MI': 'Intesa Sanpaolo',
        'LDO.MI': 'Leonardo', 'MB.MI': 'Mediobanca', 'MONC.MI': 'Moncler',
        'PST.MI': 'Poste Italiane', 'RACE.MI': 'Ferrari', 'SPM.MI': 'Saipem',
        'SRG.MI': 'Snam', 'STLA.MI': 'Stellantis', 'TIT.MI': 'Telecom Italia',
        'UCG.MI': 'UniCredit',
        
        # Spanish stocks
        'ANA.MC': 'Acciona', 'BBVA.MC': 'BBVA', 'CABK.MC': 'CaixaBank',
        'ELE.MC': 'Endesa', 'ENG.MC': 'Enagás', 'FER.MC': 'Ferrovial',
        'GRF.MC': 'Grifols', 'IAG.MC': 'International Airlines Group', 'IBE.MC': 'Iberdrola',
        'ITX.MC': 'Inditex', 'MAP.MC': 'Mapfre', 'MTS.MC': 'ArcelorMittal',
        'REP.MC': 'Repsol', 'SAN.MC': 'Santander', 'TEF.MC': 'Telefónica',
        'VIS.MC': 'Viscofan',
        
        # Swedish stocks
        'ALFA.ST': 'Alfa Laval', 'ASSA-B.ST': 'Assa Abloy', 'ATCO-A.ST': 'Atlas Copco',
        'ELUX-B.ST': 'Electrolux', 'ERIC-B.ST': 'Ericsson', 'GETI-B.ST': 'Getinge',
        'HM-B.ST': 'H&M', 'INVE-B.ST': 'Investor', 'SAND.ST': 'Sandvik',
        'SCA-B.ST': 'Svenska Cellulosa', 'SEB-A.ST': 'Skandinaviska Enskilda Banken',
        'SHB-A.ST': 'Svenska Handelsbanken', 'SWED-A.ST': 'Swedbank', 'TEL2-B.ST': 'Tele2',
        'VOLV-B.ST': 'Volvo',
        
        # Other European markets
        'ELI.BR': 'Elia Group', 'SOLB.BR': 'Solvay', 'UMI.BR': 'Umicore',
        'COLO-B.CO': 'Coloplast', 'DANSKE.CO': 'Danske Bank', 'NOVO-B.CO': 'Novo Nordisk',
        'ORSTED.CO': 'Ørsted', 'YAR.OL': 'Yara International', 'DNB.OL': 'DNB',
        'TEL.OL': 'Telenor', 'EQNR.OL': 'Equinor', 'NHY.OL': 'Norsk Hydro',
        'SAMPO.HE': 'Sampo', 'UPM.HE': 'UPM', 'NESTE.HE': 'Neste', 'ORNBV.HE': 'Orion'
    }
    return cegnevek

def get_cegnev(szimbólum):
    cegnevek = get_cegnevek_szotara()
    return cegnevek.get(szimbólum, "Ismeretlen cég")

def get_reszveny_szamlalo():
    return len(get_eu_reszvenyek())
