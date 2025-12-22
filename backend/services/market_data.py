import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

class MarketDataService:
    def __init__(self):
        # Global Indices
        self.indices = {
            "S&P 500": "^GSPC",
            "Nasdaq 100": "^NDX",
            "Dow Jones": "^DJI",
            "IBEX 35": "^IBEX",
            "DAX 40": "^GDAXI",
            "CAC 40": "^FCHI",
            "FTSE 100": "^FTSE",
            "EURO STOXX 50": "^STOXX50E",
            "Nikkei 225": "^N225"
        }

    # ... (other methods same) ...

    def get_indices_summary(self) -> List[Dict]:
        """Obtiene un resumen actual de los principales índices."""
        summary = []
        for name, ticker in self.indices.items():
            try:
                ticker_obj = yf.Ticker(ticker)
                # Obtenemos info rápida
                info = ticker_obj.info
                # O usamos history para datos más recientes si info falla o es lenta
                hist = ticker_obj.history(period="5d")
                
                if not hist.empty:
                    last_close = hist['Close'].iloc[-1]
                    
                    # Intentar obtener previousClose de info si está disponible
                    previous_close = info.get('previousClose')
                    
                    # Si no esta en info, usamos el cierre del día anterior en el historial
                    if previous_close is None and len(hist) > 1:
                        previous_close = hist['Close'].iloc[-2]
                    elif previous_close is None:
                         # Fallback si no hay suficientes datos históricos
                         previous_close = hist['Open'].iloc[-1]
                    
                    change = last_close - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    summary.append({
                        "name": name,
                        "ticker": ticker,
                        "price": round(last_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "currency": "EUR" # Asumimos EUR/GBP según corresponda pero hardcodeamos para demo
                    })
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                
        return summary

    def get_historical_data(self, ticker: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """Obtiene datos históricos para un ticker específico."""
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching history for {ticker}: {e}")
            return None

    def get_stock_info(self, ticker: str) -> Dict:
        """Obtiene información fundamental del ticker."""
        try:
            t = yf.Ticker(ticker)
            info = t.info
            
            # Extract safe values with defaults
            return {
                "longName": info.get("longName", ticker),
                "description": info.get("longBusinessSummary", "No description available."),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "marketCap": info.get("marketCap", None),
                "trailingPE": info.get("trailingPE", None),
                "forwardPE": info.get("forwardPE", None),
                "dividendYield": info.get("dividendYield", None),
                "beta": info.get("beta", None),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", None),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", None),
                "returnOnEquity": info.get("returnOnEquity", None),
                "profitMargins": info.get("profitMargins", None),
                "operatingMargins": info.get("operatingMargins", None),
                "totalRevenue": info.get("totalRevenue", None),
                "revenueGrowth": info.get("revenueGrowth", None),
                "currency": info.get("currency", "EUR")
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return {}

    def get_index_constituents(self, index_ticker: str) -> List[Dict]:
        """
        Devuelve una lista de los principales componentes para un índice dado.
        Expanded list for major indices.
        """
        constituents_map = {
            "^GSPC": [ # S&P 500 (Top ~20)
                {"ticker": "MSFT", "name": "Microsoft"}, {"ticker": "AAPL", "name": "Apple"},
                {"ticker": "NVDA", "name": "Nvidia"}, {"ticker": "AMZN", "name": "Amazon"},
                {"ticker": "GOOGL", "name": "Alphabet A"}, {"ticker": "META", "name": "Meta"},
                {"ticker": "TSLA", "name": "Tesla"}, {"ticker": "BRK-B", "name": "Berkshire Hathaway"},
                {"ticker": "LLY", "name": "Eli Lilly"}, {"ticker": "AVGO", "name": "Broadcom"},
                {"ticker": "JPM", "name": "JPMorgan Chase"}, {"ticker": "XOM", "name": "Exxon Mobil"},
                {"ticker": "UNH", "name": "UnitedHealth"}, {"ticker": "V", "name": "Visa"},
                {"ticker": "PG", "name": "Procter & Gamble"}, {"ticker": "MA", "name": "Mastercard"},
                {"ticker": "COST", "name": "Costco"}, {"ticker": "JNJ", "name": "Johnson & Johnson"},
                {"ticker": "HD", "name": "Home Depot"}, {"ticker": "MRK", "name": "Merck"}
            ],
            "^NDX": [ # Nasdaq 100 (Top Tech ~15)
                {"ticker": "MSFT", "name": "Microsoft"}, {"ticker": "AAPL", "name": "Apple"},
                {"ticker": "NVDA", "name": "Nvidia"}, {"ticker": "AMZN", "name": "Amazon"},
                {"ticker": "AVGO", "name": "Broadcom"}, {"ticker": "META", "name": "Meta"},
                {"ticker": "TSLA", "name": "Tesla"}, {"ticker": "COST", "name": "Costco"},
                {"ticker": "GOOGL", "name": "Alphabet"}, {"ticker": "NFLX", "name": "Netflix"},
                {"ticker": "AMD", "name": "AMD"}, {"ticker": "ADBE", "name": "Adobe"},
                {"ticker": "PEP", "name": "PepsiCo"}, {"ticker": "LIN", "name": "Linde"},
                {"ticker": "CSCO", "name": "Cisco"}
            ],
            "^DJI": [ # Dow Jones (All 30)
                {"ticker": "MMM", "name": "3M"}, {"ticker": "AXP", "name": "American Express"},
                {"ticker": "AMGN", "name": "Amgen"}, {"ticker": "AAPL", "name": "Apple"},
                {"ticker": "BA", "name": "Boeing"}, {"ticker": "CAT", "name": "Caterpillar"},
                {"ticker": "CVX", "name": "Chevron"}, {"ticker": "CSCO", "name": "Cisco"},
                {"ticker": "KO", "name": "Coca-Cola"}, {"ticker": "DIS", "name": "Disney"},
                {"ticker": "DOW", "name": "Dow"}, {"ticker": "GS", "name": "Goldman Sachs"},
                {"ticker": "HD", "name": "Home Depot"}, {"ticker": "HON", "name": "Honeywell"},
                {"ticker": "IBM", "name": "IBM"}, {"ticker": "INTC", "name": "Intel"},
                {"ticker": "JNJ", "name": "Johnson & Johnson"}, {"ticker": "JPM", "name": "JPMorgan"},
                {"ticker": "MCD", "name": "McDonald's"}, {"ticker": "MRK", "name": "Merck"},
                {"ticker": "MSFT", "name": "Microsoft"}, {"ticker": "NKE", "name": "Nike"},
                {"ticker": "PG", "name": "Procter & Gamble"}, {"ticker": "CRM", "name": "Salesforce"},
                {"ticker": "TRV", "name": "Travelers"}, {"ticker": "UNH", "name": "UnitedHealth"},
                {"ticker": "VZ", "name": "Verizon"}, {"ticker": "V", "name": "Visa"},
                {"ticker": "WMT", "name": "Walmart"}, {"ticker": "AMZN", "name": "Amazon"}
            ],
            "^IBEX": [ # IBEX 35 (Full)
                {"ticker": "ITX.MC", "name": "Inditex"}, {"ticker": "IBE.MC", "name": "Iberdrola"},
                {"ticker": "SAN.MC", "name": "Santander"}, {"ticker": "BBVA.MC", "name": "BBVA"},
                {"ticker": "CABK.MC", "name": "CaixaBank"}, {"ticker": "AMS.MC", "name": "Amadeus"},
                {"ticker": "TEF.MC", "name": "Telefónica"}, {"ticker": "REP.MC", "name": "Repsol"},
                {"ticker": "FER.MC", "name": "Ferrovial"}, {"ticker": "AENA.MC", "name": "Aena"},
                {"ticker": "NTGY.MC", "name": "Naturgy"}, {"ticker": "EDR.MC", "name": "Endesa"},
                {"ticker": "ACS.MC", "name": "ACS"}, {"ticker": "GRF.MC", "name": "Grifols"},
                {"ticker": "ENG.MC", "name": "Enagás"}, {"ticker": "RED.MC", "name": "Red Eléctrica"},
                {"ticker": "MAP.MC", "name": "Mapfre"}, {"ticker": "SAB.MC", "name": "Sabadell"},
                {"ticker": "BKT.MC", "name": "Bankinter"}, {"ticker": "ANA.MC", "name": "Acciona"},
                {"ticker": "MRL.MC", "name": "Merlin Properties"}, {"ticker": "CLNX.MC", "name": "Cellnex"},
                {"ticker": "ACG.MC", "name": "Acerinox"}, {"ticker": "FDR.MC", "name": "Fluidra"},
                {"ticker": "COL.MC", "name": "Colonial"}, {"ticker": "IAG.MC", "name": "IAG"},
                {"ticker": "LOG.MC", "name": "Logista"}, {"ticker": "ROVI.MC", "name": "Rovi"},
                {"ticker": "UNI.MC", "name": "Unicaja"}, {"ticker": "SACY.MC", "name": "Sacyr"},
                {"ticker": "SOL.MC", "name": "Solaria"}, {"ticker": "MEL.MC", "name": "Meliá Hotels"},
                {"ticker": "IDR.MC", "name": "Indra"}, {"ticker": "ANE.MC", "name": "Acciona Energía"}
            ],
            "^GDAXI": [ # DAX 40 (Major)
                {"ticker": "SAP.DE", "name": "SAP"}, {"ticker": "SIE.DE", "name": "Siemens"},
                {"ticker": "ALV.DE", "name": "Allianz"}, {"ticker": "AIR.DE", "name": "Airbus"},
                {"ticker": "DTE.DE", "name": "Deutsche Telekom"}, {"ticker": "MBG.DE", "name": "Mercedes-Benz"},
                {"ticker": "VOW3.DE", "name": "Volkswagen"}, {"ticker": "BMW.DE", "name": "BMW"},
                {"ticker": "DHL.DE", "name": "DHL Group"}, {"ticker": "BAS.DE", "name": "BASF"},
                {"ticker": "IFX.DE", "name": "Infineon"}, {"ticker": "MUV2.DE", "name": "Munich Re"},
                {"ticker": "DB1.DE", "name": "Deutsche Boerse"}, {"ticker": "BEI.DE", "name": "Beiersdorf"},
                {"ticker": "EOAN.DE", "name": "E.ON"}, {"ticker": "RWE.DE", "name": "RWE"},
                {"ticker": "DTG.DE", "name": "Daimler Truck"}, {"ticker": "ADS.DE", "name": "Adidas"},
                {"ticker": "VNA.DE", "name": "Vonovia"}, {"ticker": "HNR1.DE", "name": "Hannover Rueck"},
                {"ticker": "BAYN.DE", "name": "Bayer"}, {"ticker": "CON.DE", "name": "Continental"},
                {"ticker": "COK.DE", "name": "Commerzbank"}, {"ticker": "DBK.DE", "name": "Deutsche Bank"},
                {"ticker": "HEI.DE", "name": "Heidelberg Materials"}, {"ticker": "HEN3.DE", "name": "Henkel"},
                {"ticker": "MTX.DE", "name": "MTU Aero Engines"}, {"ticker": "PUM.DE", "name": "Puma"},
                {"ticker": "QIA.DE", "name": "Qiagen"}, {"ticker": "RHM.DE", "name": "Rheinmetall"},
                {"ticker": "SHL.DE", "name": "Siemens Healthineers"}, {"ticker": "SY1.DE", "name": "Symrise"},
                {"ticker": "ZAL.DE", "name": "Zalando"}
            ],
            "^FCHI": [ # CAC 40 (Major)
                {"ticker": "MC.PA", "name": "LVMH"}, {"ticker": "OR.PA", "name": "L'Oréal"},
                {"ticker": "RMS.PA", "name": "Hermès"}, {"ticker": "TTE.PA", "name": "TotalEnergies"},
                {"ticker": "SAN.PA", "name": "Sanofi"}, {"ticker": "AIR.PA", "name": "Airbus"},
                {"ticker": "SU.PA", "name": "Schneider Electric"}, {"ticker": "AI.PA", "name": "Air Liquide"},
                {"ticker": "EL.PA", "name": "EssilorLuxottica"}, {"ticker": "BNP.PA", "name": "BNP Paribas"},
                {"ticker": "CS.PA", "name": "AXA"}, {"ticker": "DG.PA", "name": "Vinci"},
                {"ticker": "SAF.PA", "name": "Safran"}, {"ticker": "KER.PA", "name": "Kering"},
                {"ticker": "ORA.PA", "name": "Orange"}, {"ticker": "CAP.PA", "name": "Capgemini"},
                {"ticker": "CA.PA", "name": "Carrefour"}, {"ticker": "ACA.PA", "name": "Crédit Agricole"},
                {"ticker": "BN.PA", "name": "Danone"}, {"ticker": "ENGI.PA", "name": "Engie"},
                {"ticker": "LR.PA", "name": "Legrand"}, {"ticker": "ML.PA", "name": "Michelin"},
                {"ticker": "PUB.PA", "name": "Publicis"}, {"ticker": "RNO.PA", "name": "Renault"},
                {"ticker": "SGO.PA", "name": "Saint-Gobain"}, {"ticker": "GLE.PA", "name": "Société Générale"},
                {"ticker": "STLAP.PA", "name": "Stellantis"}, {"ticker": "STM.PA", "name": "STMicroelectronics"},
                {"ticker": "TEP.PA", "name": "Teleperformance"}, {"ticker": "HO.PA", "name": "Thales"},
                {"ticker": "VIE.PA", "name": "Veolia"}
            ],
            "^FTSE": [ # FTSE 100 (Major)
                {"ticker": "AZN.L", "name": "AstraZeneca"}, {"ticker": "SHEL.L", "name": "Shell"},
                {"ticker": "HSBA.L", "name": "HSBC"}, {"ticker": "ULVR.L", "name": "Unilever"},
                {"ticker": "BP.L", "name": "BP"}, {"ticker": "RIO.L", "name": "Rio Tinto"},
                {"ticker": "DGE.L", "name": "Diageo"}, {"ticker": "GSK.L", "name": "GSK"},
                {"ticker": "REL.L", "name": "RELX"}, {"ticker": "GLEN.L", "name": "Glencore"},
                {"ticker": "BATS.L", "name": "British American Tobacco"}, {"ticker": "LSEG.L", "name": "LSEG"},
                {"ticker": "NG.L", "name": "National Grid"}, {"ticker": "AAL.L", "name": "Anglo American"},
                {"ticker": "LLOY.L", "name": "Lloyds Banking Group"}, {"ticker": "BARC.L", "name": "Barclays"},
                {"ticker": "VOD.L", "name": "Vodafone"}, {"ticker": "TSCO.L", "name": "Tesco"},
                {"ticker": "RR.L", "name": "Rolls-Royce"}, {"ticker": "PRU.L", "name": "Prudential"},
                {"ticker": "NWG.L", "name": "NatWest"}, {"ticker": "BA.L", "name": "BAE Systems"},
                {"ticker": "CPG.L", "name": "Compass Group"}, {"ticker": "EXPN.L", "name": "Experian"},
                {"ticker": "HLN.L", "name": "Haleon"}, {"ticker": "SGE.L", "name": "Sage Group"}
            ],
            "^STOXX50E": [ # EURO STOXX 50 (Major)
                {"ticker": "ASML.AS", "name": "ASML"}, {"ticker": "MC.PA", "name": "LVMH"},
                {"ticker": "SAP.DE", "name": "SAP"}, {"ticker": "TTE.PA", "name": "TotalEnergies"},
                {"ticker": "SIE.DE", "name": "Siemens"}, {"ticker": "SAN.PA", "name": "Sanofi"},
                {"ticker": "ALV.DE", "name": "Allianz"}, {"ticker": "OR.PA", "name": "L'Oréal"},
                {"ticker": "SU.PA", "name": "Schneider Electric"}, {"ticker": "AIR.PA", "name": "Airbus"},
                {"ticker": "IBE.MC", "name": "Iberdrola"}, {"ticker": "RMS.PA", "name": "Hermès"},
                {"ticker": "BNP.PA", "name": "BNP Paribas"}, {"ticker": "AI.PA", "name": "Air Liquide"},
                {"ticker": "CS.PA", "name": "AXA"}, {"ticker": "ITX.MC", "name": "Inditex"},
                {"ticker": "MBG.DE", "name": "Mercedes-Benz"}, {"ticker": "DTE.DE", "name": "Deutsche Telekom"},
                {"ticker": "BBVA.MC", "name": "BBVA"}, {"ticker": "EL.PA", "name": "EssilorLuxottica"},
                {"ticker": "MUV2.DE", "name": "Munich Re"}, {"ticker": "BAS.DE", "name": "BASF"},
                {"ticker": "ABI.BR", "name": "AB InBev"}, {"ticker": "SAF.PA", "name": "Safran"},
                {"ticker": "SAN.MC", "name": "Santander"}, {"ticker": "DG.PA", "name": "Vinci"},
                {"ticker": "BMW.DE", "name": "BMW"}, {"ticker": "INGA.AS", "name": "ING"},
                {"ticker": "STLAP.PA", "name": "Stellantis"}, {"ticker": "ENEL.MI", "name": "Enel"},
                {"ticker": "ISP.MI", "name": "Intesa Sanpaolo"}, {"ticker": "UNI.MI", "name": "Unicredit"},
                {"ticker": "CRH.L", "name": "CRH"}, {"ticker": "AD.AS", "name": "Ahold Delhaize"}
            ],
            "^N225": [ # Nikkei 225
                {"ticker": "7203.T", "name": "Toyota"}, {"ticker": "6758.T", "name": "Sony"},
                {"ticker": "9984.T", "name": "SoftBank"}, {"ticker": "8035.T", "name": "Tokyo Electron"},
                {"ticker": "6861.T", "name": "Keyence"}, {"ticker": "9983.T", "name": "Fast Retailing"},
                {"ticker": "7974.T", "name": "Nintendo"}, {"ticker": "8058.T", "name": "Mitsubishi"},
                {"ticker": "6098.T", "name": "Recruit Holdings"}, {"ticker": "9432.T", "name": "NTT"}
            ]
        }

        base_list = constituents_map.get(index_ticker, [])
        
        # Optimization: Fetch basic info only or skip price for full list if it's too slow.
        # For now, to support "All companies" request without timeouts, 
        # let's try to batch fetch or just return the list if price fetch fails.
        # Reduced history fetch to 1d for speed.
        
        results = []
        # Limit to top 50 to avoid timeout on simple loop
        for item in base_list[:50]: 
            try:
                t = yf.Ticker(item["ticker"])
                # history(period='1d') is usually fast
                hist = t.history(period="2d") 
                if not hist.empty:
                    last = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[-1]
                    change = last - prev
                    change_pct = (change / prev) * 100
                    
                    results.append({
                        **item,
                        "price": round(last, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_pct, 2)
                    })
                else:
                    results.append({**item, "price": None, "change": None, "change_percent": None})
            except:
                results.append({**item, "price": None, "change": None, "change_percent": None})
                
        return results
