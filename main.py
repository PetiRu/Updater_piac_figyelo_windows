import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import logging
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import sys
import os
import queue
import json
import random
from stocks import get_eu_reszvenyek, get_cegnev
from update_handler import FrissitoKezelo

class RészvényFigyelő:
    def __init__(self, root):
        self.root = root
        self.root.title("EU Részvény Figyelő - Stochastic Szkanner v2.1.0")
        self.root.geometry("1600x900")
        self.root.minsize(1400, 700)
        
        self._logolas_beallitasa()
        self._komponensek_beallitasa()
        self._gui_beallitasa()
        self.megfigyeles_inditasa()
        self._frissitesek_ellenorzese_inditaskor()

    def _logolas_beallitasa(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/stock_monitor.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('RészvényFigyelő')
        self.logger.info("Alkalmazás elindult")

    def _komponensek_beallitasa(self):
        self.eu_reszvenyek = get_eu_reszvenyek()
        self.figyelt_reszvenyek = []
        self.stochastic_kuszob = 20
        self.ellenorzes_intervallum = 300
        
        self.k_periodus = 14
        self.k_simitas = 1
        self.d_simitas = 3
        
        self.jelzes_tipusok = {
            "Alatta": "alatta",
            "Keresztezés (±3)": "keresztezes", 
            "Keresztezés fel": "keresztezes_fel",
            "Keresztezés le": "keresztezes_le"
        }
        self.aktualis_jelzes_tipus = "alatta"
        
        self.use_k_line = True
        self.use_d_line = False
        
        self.timeframe_opciok = {
            "1 Perc": "1m",
            "5 Perc": "5m", 
            "15 Perc": "15m",
            "1 Óra": "1h",
            "4 Óra": "4h",
            "1 Nap": "1d"
        }
        self.aktualis_timeframe = "1h"
        self.aktualis_timeframe_nev = "1 Óra"
        
        self.megfigyeles_aktiv = False
        self.megfigyeles_szal = None
        self.uzenet_verem = queue.Queue()
        
        self.frissito_kezelo = FrissitoKezelo()
        
        self.utolso_ellenorzes_ido = None
        self.ellenorzes_szamlalo = 0
        self.jelzesek_szamlalo = 0
        
        self.reszveny_gyorsitotar = {}
        self.gyorsitotar_tartam = timedelta(minutes=5)
        
        self.elozo_ertekek = {}
        
        # Piaci áttekintő változók
        self.piaci_frissites_idozito = None

    def _gui_beallitasa(self):
        self._stilusok_beallitasa()
        
        fos_keret = ttk.Frame(self.root, padding="10")
        fos_keret.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        fos_keret.columnconfigure(1, weight=1)
        fos_keret.columnconfigure(2, weight=0)  # Piaci panel súlya kevesebb
        fos_keret.rowconfigure(1, weight=1)
        
        cim_cimke = ttk.Label(fos_keret, text="EU Részvény Figyelő - Stochastic Szkanner v2.1.0", 
                             font=('Arial', 16, 'bold'))
        cim_cimke.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        self._allapotsor_beallitasa(fos_keret)
        self._vezerlok_beallitasa(fos_keret)
        self._eredmenyek_keret_beallitasa(fos_keret)
        self._piaci_attekinto_panel_beallitasa(fos_keret)  # ÚJ PANEL
        self._terminal_keret_beallitasa(fos_keret)
        
        fos_keret.rowconfigure(1, weight=1)
        fos_keret.rowconfigure(3, weight=0)
        fos_keret.columnconfigure(1, weight=1)
        
        self._uzenetek_feldolgozasa()

    def _stilusok_beallitasa(self):
        stilus = ttk.Style()
        stilus.configure('Green.TButton', foreground='green')
        stilus.configure('Red.TButton', foreground='red')
        stilus.configure('Orange.TButton', foreground='orange')

    def _allapotsor_beallitasa(self, szulo):
        allapot_keret = ttk.Frame(szulo)
        allapot_keret.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.allapot_valtozo = tk.StringVar(value="Inicializálás...")
        allapot_cimke = ttk.Label(allapot_keret, textvariable=self.allapot_valtozo, font=('Arial', 10, 'bold'))
        allapot_cimke.grid(row=0, column=0, sticky=tk.W)
        
        self.allapot_canvas = tk.Canvas(allapot_keret, width=20, height=20, bg="orange", highlightthickness=1)
        self.allapot_canvas.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.timeframe_info_valtozo = tk.StringVar(value="Időkeret: 1 Óra")
        timeframe_cimke = ttk.Label(allapot_keret, textvariable=self.timeframe_info_valtozo, font=('Arial', 9))
        timeframe_cimke.grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        self.jelzes_info_valtozo = tk.StringVar(value="Jelzés: Alatta")
        jelzes_cimke = ttk.Label(allapot_keret, textvariable=self.jelzes_info_valtozo, font=('Arial', 9))
        jelzes_cimke.grid(row=0, column=3, sticky=tk.W, padx=(20, 0))
        
        self.ellenorzes_info_valtozo = tk.StringVar(value="Szkennelések: 0 | Jelzések: 0")
        ellenorzes_cimke = ttk.Label(allapot_keret, textvariable=self.ellenorzes_info_valtozo, font=('Arial', 9))
        ellenorzes_cimke.grid(row=0, column=4, sticky=tk.E, padx=(0, 10))
        
        allapot_keret.columnconfigure(4, weight=1)

    def _vezerlok_beallitasa(self, szulo):
        vezerlo_keret = ttk.LabelFrame(szulo, text="Vezérlők", padding="10")
        vezerlo_keret.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Első sor
        elso_sor_keret = ttk.Frame(vezerlo_keret)
        elso_sor_keret.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        kuszob_keret = ttk.Frame(elso_sor_keret)
        kuszob_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(kuszob_keret, text="Stochastic Küszöb:").grid(row=0, column=0, sticky=tk.W)
        self.kuszob_valtozo = tk.StringVar(value=str(self.stochastic_kuszob))
        kuszob_bevitel = ttk.Entry(kuszob_keret, textvariable=self.kuszob_valtozo, width=5)
        kuszob_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Button(kuszob_keret, text="Frissítés", command=self._kuszob_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        timeframe_keret = ttk.Frame(elso_sor_keret)
        timeframe_keret.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(timeframe_keret, text="Időkeret:").grid(row=0, column=0, sticky=tk.W)
        self.timeframe_valtozo = tk.StringVar(value=self.aktualis_timeframe_nev)
        timeframe_combobox = ttk.Combobox(timeframe_keret, textvariable=self.timeframe_valtozo,
                                         values=list(self.timeframe_opciok.keys()), state="readonly", width=10)
        timeframe_combobox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        timeframe_combobox.bind('<<ComboboxSelected>>', self._timeframe_valtas)
        
        intervallum_keret = ttk.Frame(elso_sor_keret)
        intervallum_keret.grid(row=0, column=2, sticky=tk.W)
        ttk.Label(intervallum_keret, text="Szkennelési Intervallum (perc):").grid(row=0, column=0, sticky=tk.W)
        self.intervallum_valtozo = tk.StringVar(value=str(self.ellenorzes_intervallum // 60))
        intervallum_bevitel = ttk.Entry(intervallum_keret, textvariable=self.intervallum_valtozo, width=5)
        intervallum_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Button(intervallum_keret, text="Frissítés", command=self._intervallum_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Második sor - Stochastic paraméterek
        masodik_sor_keret = ttk.LabelFrame(vezerlo_keret, text="Stochastic Paraméterek", padding="5")
        masodik_sor_keret.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        k_hossz_keret = ttk.Frame(masodik_sor_keret)
        k_hossz_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Label(k_hossz_keret, text="%K Hossz:").grid(row=0, column=0, sticky=tk.W)
        self.k_hossz_valtozo = tk.StringVar(value=str(self.k_periodus))
        k_hossz_bevitel = ttk.Entry(k_hossz_keret, textvariable=self.k_hossz_valtozo, width=5)
        k_hossz_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Button(k_hossz_keret, text="Frissítés", command=self._k_hossz_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        k_simitas_keret = ttk.Frame(masodik_sor_keret)
        k_simitas_keret.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        ttk.Label(k_simitas_keret, text="%K Simítás:").grid(row=0, column=0, sticky=tk.W)
        self.k_simitas_valtozo = tk.StringVar(value=str(self.k_simitas))
        k_simitas_bevitel = ttk.Entry(k_simitas_keret, textvariable=self.k_simitas_valtozo, width=5)
        k_simitas_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Button(k_simitas_keret, text="Frissítés", command=self._k_simitas_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        d_simitas_keret = ttk.Frame(masodik_sor_keret)
        d_simitas_keret.grid(row=0, column=2, sticky=tk.W)
        ttk.Label(d_simitas_keret, text="%D Simítás:").grid(row=0, column=0, sticky=tk.W)
        self.d_simitas_valtozo = tk.StringVar(value=str(self.d_simitas))
        d_simitas_bevitel = ttk.Entry(d_simitas_keret, textvariable=self.d_simitas_valtozo, width=5)
        d_simitas_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Button(d_simitas_keret, text="Frissítés", command=self._d_simitas_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Harmadik sor - Jelzés beállítások
        harmadik_sor_keret = ttk.LabelFrame(vezerlo_keret, text="Jelzés Beállítások", padding="5")
        harmadik_sor_keret.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        jelzes_tipus_keret = ttk.Frame(harmadik_sor_keret)
        jelzes_tipus_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(jelzes_tipus_keret, text="Jelzés Típusa:").grid(row=0, column=0, sticky=tk.W)
        self.jelzes_tipus_valtozo = tk.StringVar(value="Alatta")
        jelzes_tipus_combobox = ttk.Combobox(jelzes_tipus_keret, textvariable=self.jelzes_tipus_valtozo,
                                           values=list(self.jelzes_tipusok.keys()), state="readonly", width=15)
        jelzes_tipus_combobox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        jelzes_tipus_combobox.bind('<<ComboboxSelected>>', self._jelzes_tipus_valtas)
        
        vonalak_keret = ttk.Frame(harmadik_sor_keret)
        vonalak_keret.grid(row=0, column=1, sticky=tk.W)
        self.use_k_valtozo = tk.BooleanVar(value=self.use_k_line)
        k_check = ttk.Checkbutton(vonalak_keret, text="%K vonal", variable=self.use_k_valtozo, command=self._vonalak_frissitese)
        k_check.grid(row=0, column=0, sticky=tk.W)
        self.use_d_valtozo = tk.BooleanVar(value=self.use_d_line)
        d_check = ttk.Checkbutton(vonalak_keret, text="%D vonal", variable=self.use_d_valtozo, command=self._vonalak_frissitese)
        d_check.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Negyedik sor - Vezérlő gombok
        gomb_keret = ttk.Frame(vezerlo_keret)
        gomb_keret.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        self.inditas_gomb = ttk.Button(gomb_keret, text="Megfigyelés Indítása", command=self.megfigyeles_inditasa)
        self.inditas_gomb.grid(row=0, column=0, padx=(0, 5))
        self.leallas_gomb = ttk.Button(gomb_keret, text="Megfigyelés Leállítása", command=self.megfigyeles_leallitasa, state='disabled')
        self.leallas_gomb.grid(row=0, column=1, padx=(0, 5))
        ttk.Button(gomb_keret, text="Frissítések Ellenőrzése", command=self._frissitesek_ellenorzese_manualis).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(gomb_keret, text="Kényszer Szkennelés", command=self._kenyszer_ellenorzes).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(gomb_keret, text="Paraméterek Mentése", command=self._parameterek_mentese).grid(row=0, column=4, padx=(0, 5))
        
        # Ötödik sor - Statisztika
        stat_keret = ttk.Frame(vezerlo_keret)
        stat_keret.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(stat_keret, text="Statisztikák:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.stat_valtozo = tk.StringVar(value="Részvények: 0 | Utolsó szkennelés: Soha")
        stat_cimke = ttk.Label(stat_keret, textvariable=self.stat_valtozo, font=('Arial', 8))
        stat_cimke.grid(row=1, column=0, sticky=tk.W)
        
        self._statisztikak_frissitese()

    def _eredmenyek_keret_beallitasa(self, szulo):
        cim = f"Stochastic Jelzések ({self.aktualis_jelzes_tipus}) - {self.aktualis_timeframe_nev}"
        eredmeny_keret = ttk.LabelFrame(szulo, text=cim, padding="5")
        eredmeny_keret.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        eredmeny_keret.columnconfigure(0, weight=1)
        eredmeny_keret.rowconfigure(0, weight=1)
        
        self.eredmeny_szoveg = scrolledtext.ScrolledText(eredmeny_keret, width=80, height=15, font=('Courier', 9), wrap=tk.NONE)
        self.eredmeny_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        v_gorgeto = ttk.Scrollbar(eredmeny_keret, orient=tk.VERTICAL, command=self.eredmeny_szoveg.yview)
        v_gorgeto.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.eredmeny_szoveg.configure(yscrollcommand=v_gorgeto.set)
        
        h_gorgeto = ttk.Scrollbar(eredmeny_keret, orient=tk.HORIZONTAL, command=self.eredmeny_szoveg.xview)
        h_gorgeto.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.eredmeny_szoveg.configure(xscrollcommand=h_gorgeto.set)

    def _piaci_attekinto_panel_beallitasa(self, szulo):
        """
        🌍 Piaci Áttekintő Panel létrehozása
        """
        piaci_keret = ttk.LabelFrame(szulo, text="🌍 Piaci Áttekintő", padding="10")
        piaci_keret.grid(row=2, column=2, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 10))
        
        # Fő indexek megjelenítése
        index_keret = ttk.LabelFrame(piaci_keret, text="Fő Indexek", padding="5")
        index_keret.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.index_szoveg = scrolledtext.ScrolledText(index_keret, width=25, height=8, font=('Courier', 9))
        self.index_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Piaci hangulat
        hangulat_keret = ttk.LabelFrame(piaci_keret, text="Piaci Hangulat", padding="5")
        hangulat_keret.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        self.hangulat_szoveg = scrolledtext.ScrolledText(hangulat_keret, width=25, height=6, font=('Courier', 9))
        self.hangulat_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frissítés gomb
        frissites_keret = ttk.Frame(piaci_keret)
        frissites_keret.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Button(frissites_keret, text="Piaci Adatok Frissítése", 
                  command=self._piaci_adatok_frissitese).grid(row=0, column=0)
        
        piaci_keret.columnconfigure(0, weight=1)
        piaci_keret.rowconfigure(0, weight=1)
        piaci_keret.rowconfigure(1, weight=1)
        piaci_keret.rowconfigure(2, weight=0)
        index_keret.columnconfigure(0, weight=1)
        index_keret.rowconfigure(0, weight=1)
        hangulat_keret.columnconfigure(0, weight=1)
        hangulat_keret.rowconfigure(0, weight=1)

    def _terminal_keret_beallitasa(self, szulo):
        terminal_keret = ttk.LabelFrame(szulo, text="Terminál Kimenet", padding="5")
        terminal_keret.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        terminal_keret.columnconfigure(0, weight=1)
        terminal_keret.rowconfigure(0, weight=1)
        
        self.terminal_szoveg = scrolledtext.ScrolledText(terminal_keret, width=120, height=12, font=('Courier', 8), wrap=tk.WORD)
        self.terminal_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.terminal_szoveg.tag_config("red", foreground="red")
        self.terminal_szoveg.tag_config("orange", foreground="orange")
        self.terminal_szoveg.tag_config("green", foreground="green")
        self.terminal_szoveg.tag_config("blue", foreground="blue")
        self.terminal_szoveg.tag_config("signal", foreground="green", background="#f0fff0")

    def _fő_indexek_frissitese(self):
        """
        Fő európai tőzsdeindexek adatainak frissítése
        """
        indexek = {
            '^GDAXI': 'Német DAX',
            '^FCHI': 'Francia CAC 40', 
            '^FTSE': 'Angol FTSE 100',
            '^STOXX50E': 'Euro Stoxx 50',
            '^IBEX': 'Spanyol IBEX 35',
            'FTSEMIB.MI': 'Olasz FTSE MIB'
        }
        
        index_adatok = []
        
        for szimbolum, nev in indexek.items():
            try:
                ticker = yf.Ticker(szimbolum)
                adat = ticker.history(period='2d', interval='1d')
                
                if len(adat) >= 2:
                    zaras = adat['Close'].iloc[-1]
                    elozo_zaras = adat['Close'].iloc[-2]
                    valtozas = ((zaras - elozo_zaras) / elozo_zaras) * 100
                    valtozas_elojel = "+" if valtozas >= 0 else ""
                    
                    index_adatok.append(
                        f"{nev:<15} {zaras:8.0f} {valtozas_elojel}{valtozas:6.2f}%"
                    )
                else:
                    index_adatok.append(f"{nev:<15} N/A")
                    
            except Exception as e:
                index_adatok.append(f"{nev:<15} Hiba")
                self.logger.error(f"Hiba {szimbolum} index lekérésénél: {e}")
        
        return index_adatok

    def _piaci_hangulat_elemzese(self):
        """
        Piaci hangulat elemzése - hány részvény emelkedik/esesik
        """
        try:
            emelkedo = 0
            eseso = 0
            valtozatlan = 0
            osszes = len(self.eu_reszvenyek)
            
            # Véletlenszerűen választunk 30 részvényt a gyorsabb ellenőrzéshez
            mintareszvenyek = random.sample(self.eu_reszvenyek, min(30, len(self.eu_reszvenyek)))
            
            for szimbolum in mintareszvenyek:
                try:
                    ticker = yf.Ticker(szimbolum)
                    adat = ticker.history(period='2d', interval='1d')
                    
                    if len(adat) >= 2:
                        mai_zaras = adat['Close'].iloc[-1]
                        tegnapi_zaras = adat['Close'].iloc[-2]
                        
                        if mai_zaras > tegnapi_zaras:
                            emelkedo += 1
                        elif mai_zaras < tegnapi_zaras:
                            eseso += 1
                        else:
                            valtozatlan += 1
                            
                except Exception:
                    continue
            
            # Statisztikák számítása
            if len(mintareszvenyek) > 0:
                emelkedo_szazalek = (emelkedo / len(mintareszvenyek)) * 100
                eseso_szazalek = (eseso / len(mintareszvenyek)) * 100
                valtozatlan_szazalek = (valtozatlan / len(mintareszvenyek)) * 100
                
                hangulat_adatok = [
                    f"Összes: {osszes} részvény",
                    f"Minta: {len(mintareszvenyek)} db",
                    "",
                    f"📈 Emelkedő: {emelkedo} ({emelkedo_szazalek:.1f}%)",
                    f"📉 Eső: {eseso} ({eseso_szazalek:.1f}%)", 
                    f"➡️ Változatlan: {valtozatlan} ({valtozatlan_szazalek:.1f}%)",
                    "",
                    f"🧭 Hangulat: {self._hangulat_ertekeles(emelkedo_szazalek)}"
                ]
            else:
                hangulat_adatok = ["Nem sikerült adatot gyűjteni"]
                
            return hangulat_adatok
            
        except Exception as e:
            self.logger.error(f"Hiba piaci hangulat elemzésénél: {e}")
            return ["Hiba a piaci adatok gyűjtésében"]

    def _hangulat_ertekeles(self, emelkedo_szazalek):
        """
        Piaci hangulat szöveges értékelése
        """
        if emelkedo_szazalek >= 70:
            return "🚀 ERŐS BULL"
        elif emelkedo_szazalek >= 60:
            return "📈 Mérsékelt BULL" 
        elif emelkedo_szazalek >= 40:
            return "⚖️ SEMLEGES"
        elif emelkedo_szazalek >= 30:
            return "📉 Mérsékelt BEAR"
        else:
            return "🐻 ERŐS BEAR"

    def _piaci_adatok_frissitese(self):
        """
        Piaci adatok frissítése és megjelenítése
        """
        try:
            # Fő indexek frissítése
            index_adatok = self._fő_indexek_frissitese()
            self.index_szoveg.delete(1.0, tk.END)
            self.index_szoveg.insert(tk.END, "Index         Érték   Változás\n")
            self.index_szoveg.insert(tk.END, "-" * 35 + "\n")
            for sor in index_adatok:
                # Színezés a változás alapján
                if "+" in sor:
                    self.index_szoveg.insert(tk.END, sor + "\n", "green")
                elif "-" in sor:
                    self.index_szoveg.insert(tk.END, sor + "\n", "red")
                else:
                    self.index_szoveg.insert(tk.END, sor + "\n")
            
            # Piaci hangulat frissítése
            hangulat_adatok = self._piaci_hangulat_elemzese()
            self.hangulat_szoveg.delete(1.0, tk.END)
            for sor in hangulat_adatok:
                self.hangulat_szoveg.insert(tk.END, sor + "\n")
                
            self._terminal_naplozas("Piaci adatok frissítve", "INFO")
            
        except Exception as e:
            self.logger.error(f"Hiba piaci adatok frissítésénél: {e}")
            self._terminal_naplozas(f"Piaci adatok frissítési hiba: {e}", "ERROR")

    def _piaci_frissites_inditasa(self):
        """
        Piaci adatok automatikus frissítésének indítása
        """
        def idozitett_frissites():
            if self.megfigyeles_aktiv:
                self._piaci_adatok_frissitese()
                # 5 percenként frissít
                self.piaci_frissites_idozito = self.root.after(300000, idozitett_frissites)
        
        # Azonnali frissítés
        self._piaci_adatok_frissitese()
        # Időzítő beállítása
        self.piaci_frissites_idozito = self.root.after(300000, idozitett_frissites)

    def _piaci_frissites_leallitasa(self):
        """
        Piaci adatok automatikus frissítésének leállítása
        """
        if self.piaci_frissites_idozito:
            self.root.after_cancel(self.piaci_frissites_idozito)
            self.piaci_frissites_idozito = None

    # ... (a többi metódus változatlan marad, csak a megfigyelés indításánál és leállításánál kell módosítani)

    def megfigyeles_inditasa(self):
        if not self.megfigyeles_aktiv:
            self._parameterek_betoltese()
            self.megfigyeles_aktiv = True
            self.megfigyeles_szal = threading.Thread(target=self._reszvenyek_figyelese, daemon=True)
            self.megfigyeles_szal.start()
            self.inditas_gomb.config(state='disabled')
            self.leallas_gomb.config(state='normal')
            self._piaci_frissites_inditasa()  # ÚJ: Piaci frissítés indítása
            self._terminal_naplozas("Megfigyelés elindítva", "INFO")
            self.logger.info("Megfigyelés felhasználó által elindítva")

    def megfigyeles_leallitasa(self):
        self.megfigyeles_aktiv = False
        self._allapot_frissitese("orange", "Megfigyelés leállítva")
        self.inditas_gomb.config(state='normal')
        self.leallas_gomb.config(state='disabled')
        self._piaci_frissites_leallitasa()  # ÚJ: Piaci frissítés leállítása
        self._terminal_naplozas("Megfigyelés leállítva", "INFO")
        self.logger.info("Megfigyelés felhasználó által leállítva")

    # ... (a többi metódus változatlan marad)

    def _timeframe_valtas(self, event=None):
        uj_timeframe_nev = self.timeframe_valtozo.get()
        if uj_timeframe_nev in self.timeframe_opciok:
            regi_timeframe = self.aktualis_timeframe_nev
            self.aktualis_timeframe_nev = uj_timeframe_nev
            self.aktualis_timeframe = self.timeframe_opciok[uj_timeframe_nev]
            self.reszveny_gyorsitotar.clear()
            self.elozo_ertekek.clear()
            self._terminal_naplozas(f"Időkeret váltás: {regi_timeframe} -> {uj_timeframe_nev}", "INFO")
            self.timeframe_info_valtozo.set(f"Időkeret: {uj_timeframe_nev}")
            self._eredmenyek_cim_frissitese()
            self.logger.info(f"Időkeret váltva erre: {uj_timeframe_nev}")

    def _jelzes_tipus_valtas(self, event=None):
        uj_jelzes_tipus_nev = self.jelzes_tipus_valtozo.get()
        if uj_jelzes_tipus_nev in self.jelzes_tipusok:
            regi_jelzes_tipus = self.aktualis_jelzes_tipus
            self.aktualis_jelzes_tipus = self.jelzes_tipusok[uj_jelzes_tipus_nev]
            self.elozo_ertekek.clear()
            self._terminal_naplozas(f"Jelzés típus váltás: {regi_jelzes_tipus} -> {uj_jelzes_tipus_nev}", "INFO")
            self.jelzes_info_valtozo.set(f"Jelzés: {uj_jelzes_tipus_nev}")
            self._eredmenyek_cim_frissitese()
            self.logger.info(f"Jelzés típus váltva erre: {uj_jelzes_tipus_nev}")

    def _vonalak_frissitese(self):
        self.use_k_line = self.use_k_valtozo.get()
        self.use_d_line = self.use_d_valtozo.get()
        vonalak = []
        if self.use_k_line:
            vonalak.append("%K")
        if self.use_d_line:
            vonalak.append("%D")
        self._terminal_naplozas(f"Használt vonalak frissítve: {', '.join(vonalak) if vonalak else 'Nincs'}", "INFO")
        self.logger.info(f"Használt vonalak: {vonalak}")

    def _eredmenyek_cim_frissitese(self):
        cim = f"Stochastic Jelzések ({self.jelzes_tipus_valtozo.get()}) - {self.aktualis_timeframe_nev}"
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and "Stochastic Jelzések" in widget.cget("text"):
                widget.config(text=cim)
                break

    def _kuszob_frissitese(self):
        try:
            uj_kuszob = float(self.kuszob_valtozo.get())
            if 0 < uj_kuszob <= 100:
                regi_kuszob = self.stochastic_kuszob
                self.stochastic_kuszob = uj_kuszob
                self._terminal_naplozas(f"Küszöb frissítve: {regi_kuszob} -> {uj_kuszob}", "INFO")
                self.logger.info(f"Stochastic küszöb frissítve erre: {uj_kuszob}")
            else:
                self._terminal_naplozas("A küszöb értéke 1 és 100 között kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen küszöb érték", "ERROR")

    def _k_hossz_frissitese(self):
        try:
            uj_hossz = int(self.k_hossz_valtozo.get())
            if uj_hossz >= 1:
                regi_hossz = self.k_periodus
                self.k_periodus = uj_hossz
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                self._terminal_naplozas(f"%K hossz frissítve: {regi_hossz} -> {uj_hossz}", "INFO")
                self.logger.info(f"%K hossz frissítve erre: {uj_hossz}")
            else:
                self._terminal_naplozas("A %K hossz legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %K hossz érték", "ERROR")

    def _k_simitas_frissitese(self):
        try:
            uj_simitas = int(self.k_simitas_valtozo.get())
            if uj_simitas >= 1:
                regi_simitas = self.k_simitas
                self.k_simitas = uj_simitas
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                self._terminal_naplozas(f"%K simítás frissítve: {regi_simitas} -> {uj_simitas}", "INFO")
                self.logger.info(f"%K simítás frissítve erre: {uj_simitas}")
            else:
                self._terminal_naplozas("A %K simítás legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %K simítás érték", "ERROR")

    def _d_simitas_frissitese(self):
        try:
            uj_simitas = int(self.d_simitas_valtozo.get())
            if uj_simitas >= 1:
                regi_simitas = self.d_simitas
                self.d_simitas = uj_simitas
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                self._terminal_naplozas(f"%D simítás frissítve: {regi_simitas} -> {uj_simitas}", "INFO")
                self.logger.info(f"%D simítás frissítve erre: {uj_simitas}")
            else:
                self._terminal_naplozas("A %D simítás legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %D simítás érték", "ERROR")

    def _intervallum_frissitese(self):
        try:
            uj_intervallum = int(self.intervallum_valtozo.get())
            if uj_intervallum >= 1:
                regi_intervallum = self.ellenorzes_intervallum // 60
                self.ellenorzes_intervallum = uj_intervallum * 60
                self._terminal_naplozas(f"Szkennelési intervallum frissítve: {regi_intervallum}perc -> {uj_intervallum}perc", "INFO")
                self.logger.info(f"Szkennelési intervallum frissítve erre: {uj_intervallum} perc")
            else:
                self._terminal_naplozas("Az intervallum legalább 1 perc kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen intervallum érték", "ERROR")

    def _parameterek_mentese(self):
        try:
            config = {
                "verzio": "2.1.0",
                "stochastic_kuszob": self.stochastic_kuszob,
                "k_periodus": self.k_periodus,
                "k_simitas": self.k_simitas,
                "d_simitas": self.d_simitas,
                "jelzes_tipus": self.aktualis_jelzes_tipus,
                "use_k_line": self.use_k_line,
                "use_d_line": self.use_d_line,
                "timeframe": self.aktualis_timeframe,
                "ellenorzes_intervallum": self.ellenorzes_intervallum
            }
            with open("parameters.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self._terminal_naplozas("Paraméterek sikeresen elmentve", "INFO")
            self.logger.info("Paraméterek mentése sikeres")
        except Exception as e:
            self._terminal_naplozas(f"Paraméterek mentése sikertelen: {e}", "ERROR")
            self.logger.error(f"Paraméterek mentése sikertelen: {e}")

    def _parameterek_betoltese(self):
        try:
            if os.path.exists("parameters.json"):
                with open("parameters.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.stochastic_kuszob = config.get("stochastic_kuszob", 20)
                self.k_periodus = config.get("k_periodus", 14)
                self.k_simitas = config.get("k_simitas", 1)
                self.d_simitas = config.get("d_simitas", 3)
                self.aktualis_jelzes_tipus = config.get("jelzes_tipus", "alatta")
                self.use_k_line = config.get("use_k_line", True)
                self.use_d_line = config.get("use_d_line", False)
                self.aktualis_timeframe = config.get("timeframe", "1h")
                self.ellenorzes_intervallum = config.get("ellenorzes_intervallum", 300)
                self.kuszob_valtozo.set(str(self.stochastic_kuszob))
                self.k_hossz_valtozo.set(str(self.k_periodus))
                self.k_simitas_valtozo.set(str(self.k_simitas))
                self.d_simitas_valtozo.set(str(self.d_simitas))
                self.use_k_valtozo.set(self.use_k_line)
                self.use_d_valtozo.set(self.use_d_line)
                self.intervallum_valtozo.set(str(self.ellenorzes_intervallum // 60))
                for nev, ertek in self.jelzes_tipusok.items():
                    if ertek == self.aktualis_jelzes_tipus:
                        self.jelzes_tipus_valtozo.set(nev)
                        break
                for nev, ertek in self.timeframe_opciok.items():
                    if ertek == self.aktualis_timeframe:
                        self.timeframe_valtozo.set(nev)
                        self.aktualis_timeframe_nev = nev
                        break
                self._terminal_naplozas("Paraméterek sikeresen betöltve", "INFO")
                self.logger.info("Paraméterek betöltése sikeres")
        except Exception as e:
            self._terminal_naplozas(f"Paraméterek betöltése sikertelen: {e}", "ERROR")
            self.logger.error(f"Paraméterek betöltése sikertelen: {e}")

    def _statisztikak_frissitese(self):
        stat_szoveg = f"Részvények: {len(self.eu_reszvenyek)} | Utolsó szkennelés: {self.utolso_ellenorzes_ido or 'Soha'}"
        self.stat_valtozo.set(stat_szoveg)
        self.ellenorzes_info_valtozo.set(f"Szkennelések: {self.ellenorzes_szamlalo} | Jelzések: {self.jelzesek_szamlalo}")

    def _get_period_for_timeframe(self):
        timeframe_period_map = {
            "1m": "7d", "5m": "60d", "15m": "60d", "1h": "730d", "4h": "730d", "1d": "730d"
        }
        return timeframe_period_map.get(self.aktualis_timeframe, "60d")

    def _stochastic_szamitas(self, szimbolum):
        gyorsitotar_kulcs = f"{szimbolum}_{self.aktualis_timeframe}_{self.k_periodus}_{self.k_simitas}_{self.d_simitas}"
        if gyorsitotar_kulcs in self.reszveny_gyorsitotar:
            gyorsitotar_ido, gyorsitotartott_ertek = self.reszveny_gyorsitotar[gyorsitotar_kulcs]
            if datetime.now() - gyorsitotar_ido < self.gyorsitotar_tartam:
                return gyorsitotartott_ertek
        try:
            reszveny = yf.Ticker(szimbolum)
            period = self._get_period_for_timeframe()
            elozmeny = reszveny.history(period=period, interval=self.aktualis_timeframe)
            if len(elozmeny) < self.k_periodus + max(self.k_simitas, self.d_simitas):
                self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (None, None))
                return (None, None)
            also_min = elozmeny['Low'].rolling(window=self.k_periodus).min()
            felso_max = elozmeny['High'].rolling(window=self.k_periodus).max()
            nevezo = (felso_max - also_min)
            nevezo = nevezo.replace(0, 0.001)
            raw_k = 100 * (elozmeny['Close'] - also_min) / nevezo
            if self.k_simitas > 1:
                k_ertek = raw_k.rolling(window=self.k_simitas).mean()
            else:
                k_ertek = raw_k
            if self.d_simitas > 1:
                d_ertek = k_ertek.rolling(window=self.d_simitas).mean()
            else:
                d_ertek = k_ertek
            k_final = k_ertek.iloc[-1] if not pd.isna(k_ertek.iloc[-1]) else None
            d_final = d_ertek.iloc[-1] if not pd.isna(d_ertek.iloc[-1]) else None
            self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (k_final, d_final))
            return (k_final, d_final)
        except Exception as e:
            self._terminal_naplozas(f"Hiba stochastic számításakor {szimbolum}: {e}", "ERROR")
            self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (None, None))
            return (None, None)

    def _jelzes_ellenorzes(self, szimbolum, k_ertek, d_ertek):
        kulcs = f"{szimbolum}_{self.aktualis_timeframe}"
        elozo_k, elozo_d = self.elozo_ertekek.get(kulcs, (None, None))
        self.elozo_ertekek[kulcs] = (k_ertek, d_ertek)
        if k_ertek is None or (self.use_d_line and d_ertek is None):
            return False
        hasznalt_ertek = None
        if self.use_k_line and not self.use_d_line:
            hasznalt_ertek = k_ertek
        elif not self.use_k_line and self.use_d_line:
            hasznalt_ertek = d_ertek
        elif self.use_k_line and self.use_d_line:
            hasznalt_ertek = k_ertek
        if hasznalt_ertek is None:
            return False
        if self.aktualis_jelzes_tipus == "alatta":
            return hasznalt_ertek < self.stochastic_kuszob
        elif self.aktualis_jelzes_tipus == "keresztezes":
            if elozo_k is None:
                return False
            return ((elozo_k < self.stochastic_kuszob - 3 and k_ertek >= self.stochastic_kuszob - 3) or
                   (elozo_k >= self.stochastic_kuszob + 3 and k_ertek < self.stochastic_kuszob + 3))
        elif self.aktualis_jelzes_tipus == "keresztezes_fel":
            if elozo_k is None:
                return False
            return elozo_k < self.stochastic_kuszob and k_ertek >= self.stochastic_kuszob
        elif self.aktualis_jelzes_tipus == "keresztezes_le":
            if elozo_k is None:
                return False
            return elozo_k >= self.stochastic_kuszob and k_ertek < self.stochastic_kuszob
        return False

    def _reszvenyek_figyelese(self):
        self.megfigyeles_aktiv = True
        self._allapot_frissitese("green", "Megfigyelés aktív")
        self._terminal_naplozas(f"Részvény megfigyelés elindítva - Időkeret: {self.aktualis_timeframe_nev}, Jelzés: {self.jelzes_tipus_valtozo.get()}", "INFO")
        self.logger.info(f"Részvény megfigyelési szál elindítva")
        while self.megfigyeles_aktiv:
            try:
                jelzesek = []
                osszes_reszveny = len(self.eu_reszvenyek)
                feldolgozott_reszvenyek = 0
                hibak = 0
                self._terminal_naplozas(f"{osszes_reszveny} részvény szkennelésének indítása ({self.aktualis_timeframe_nev}, {self.jelzes_tipus_valtozo.get()})...", "INFO")
                for i, szimbolum in enumerate(self.eu_reszvenyek):
                    if not self.megfigyeles_aktiv:
                        break
                    if i % 10 == 0:
                        haladás = (i + 1) / osszes_reszveny * 100
                        self._allapot_frissitese("green", f"Szkennelés... {haladás:.1f}% ({self.aktualis_timeframe_nev})")
                    k_ertek, d_ertek = self._stochastic_szamitas(szimbolum)
                    feldolgozott_reszvenyek += 1
                    if k_ertek is None:
                        hibak += 1
                        continue
                    if self._jelzes_ellenorzes(szimbolum, k_ertek, d_ertek):
                        vonal_info = []
                        if self.use_k_line:
                            vonal_info.append(f"K%: {k_ertek:.2f}")
                        if self.use_d_line:
                            vonal_info.append(f"D%: {d_ertek:.2f}")
                        cegnev = get_cegnev(szimbolum)
                        jelzes = {
                            'szimbolum': szimbolum,
                            'cegnev': cegnev,
                            'k_ertek': k_ertek,
                            'd_ertek': d_ertek,
                            'idobelyeg': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'timeframe': self.aktualis_timeframe_nev,
                            'jelzes_tipus': self.jelzes_tipus_valtozo.get(),
                            'vonal_info': ", ".join(vonal_info)
                        }
                        jelzesek.append(jelzes)
                        vonal_szoveg = ", ".join(vonal_info)
                        uzenet = f"JELZÉS: {szimbolum} ({cegnev}) - {vonal_szoveg} ({self.aktualis_timeframe_nev}, {self.jelzes_tipus_valtozo.get()})"
                        self._terminal_naplozas(uzenet, "signal")
                        self.logger.info(uzenet)
                self.utolso_ellenorzes_ido = datetime.now().strftime("%H:%M:%S")
                self.ellenorzes_szamlalo += 1
                self.jelzesek_szamlalo += len(jelzesek)
                self.uzenet_verem.put(('eredmenyek_frissitese', jelzesek))
                self.uzenet_verem.put(('statisztikak_frissitese', None))
                self._terminal_naplozas(f"Szkennelés befejezve ({self.aktualis_timeframe_nev}, {self.jelzes_tipus_valtozo.get()}): {feldolgozott_reszvenyek} feldolgozva, {len(jelzesek)} jelzés, {hibak} hiba", "INFO" if hibak == 0 else "WARNING")
                self._terminal_naplozas(f"Következő szkennelés {self.ellenorzes_intervallum//60} perc múlva...", "INFO")
                for i in range(self.ellenorzes_intervallum):
                    if not self.megfigyeles_aktiv:
                        break
                    time.sleep(1)
            except Exception as e:
                self._allapot_frissitese("red", f"Megfigyelési hiba: {e}")
                self._terminal_naplozas(f"Megfigyelési hiba ({self.aktualis_timeframe_nev}): {e}", "ERROR")
                self.logger.error(f"Megfigyelési hiba ({self.aktualis_timeframe_nev}): {e}")
                for i in range(60):
                    if not self.megfigyeles_aktiv:
                        break
                    time.sleep(1)

    def _eredmenyek_frissitese(self, jelzesek):
        self.eredmeny_szoveg.delete(1.0, tk.END)
        if not jelzesek:
            self.eredmeny_szoveg.insert(tk.END, f"Nem található részvény {self.jelzes_tipus_valtozo.get()} jelzéssel ({self.aktualis_timeframe_nev})")
            return
        fejlec = f"{'Szimbólum':<12} {'Cégnév':<25} {'K%':<8} {'D%':<8} {'Jelzés':<15} {'Időkeret':<10} {'Idő':<20}\n"
        self.eredmeny_szoveg.insert(tk.END, fejlec)
        self.eredmeny_szoveg.insert(tk.END, "-" * 110 + "\n")
        for jelzes in sorted(jelzesek, key=lambda x: x['k_ertek']):
            k_ertek = f"{jelzes['k_ertek']:.2f}" if jelzes['k_ertek'] is not None else "N/A"
            d_ertek = f"{jelzes['d_ertek']:.2f}" if jelzes['d_ertek'] is not None else "N/A"
            cegnev = jelzes['cegnev']
            if len(cegnev) > 24:
                cegnev = cegnev[:22] + ".."
            sor = f"{jelzes['szimbolum']:<12} {cegnev:<25} {k_ertek:<8} {d_ertek:<8} {jelzes['jelzes_tipus']:<15} {jelzes['timeframe']:<10} {jelzes['idobelyeg']:<20}\n"
            self.eredmeny_szoveg.insert(tk.END, sor)

    def _terminal_naplozas(self, uzenet, szint="INFO"):
        self.uzenet_verem.put(('naplo', (uzenet, szint)))

    def _allapot_frissitese(self, szin, uzenet):
        self.uzenet_verem.put(('allapot', (szin, uzenet)))

    def _uzenetek_feldolgozasa(self):
        try:
            while True:
                try:
                    msg_type, data = self.uzenet_verem.get_nowait()
                    if msg_type == 'naplo':
                        message, level = data
                        self._terminal_naplozas_ui(message, level)
                    elif msg_type == 'allapot':
                        color, message = data
                        self._allapot_frissitese_ui(color, message)
                    elif msg_type == 'eredmenyek_frissitese':
                        self._eredmenyek_frissitese(data)
                    elif msg_type == 'statisztikak_frissitese':
                        self._statisztikak_frissitese()
                except queue.Empty:
                    break
        except Exception as e:
            self.logger.error(f"Hiba üzenetek feldolgozásakor: {e}")
        self.root.after(100, self._uzenetek_feldolgozasa)

    def _terminal_naplozas_ui(self, uzenet, szint):
        idobelyeg = datetime.now().strftime('%H:%M:%S')
        self.terminal_szoveg.insert(tk.END, f"{idobelyeg} - ")
        if szint == "ERROR":
            self.terminal_szoveg.insert(tk.END, f"HIBA: {uzenet}\n", "red")
        elif szint == "WARNING":
            self.terminal_szoveg.insert(tk.END, f"FIGYELMEZTETÉS: {uzenet}\n", "orange")
        elif szint == "signal":
            self.terminal_szoveg.insert(tk.END, f"🚨 {uzenet}\n", "signal")
        elif szint == "INFO":
            self.terminal_szoveg.insert(tk.END, f"{uzenet}\n", "blue")
        else:
            self.terminal_szoveg.insert(tk.END, f"{uzenet}\n")
        self.terminal_szoveg.see(tk.END)
        self.terminal_szoveg.update()

    def _allapot_frissitese_ui(self, szin, uzenet):
        self.allapot_canvas.configure(bg=szin)
        self.allapot_valtozo.set(uzenet)

    def _kenyszer_ellenorzes(self):
        if self.megfigyeles_aktiv:
            self._terminal_naplozas("Szkennelés már folyamatban van", "INFO")
        else:
            self._terminal_naplozas("Kézi szkennelés kérés...", "INFO")
            self._terminal_naplozas("Kézi szkennelés funkció implementálásra vár", "INFO")

    def _frissitesek_ellenorzese_inditaskor(self):
        def frissites_ellenorzes():
            siker, uzenet, ujrainditas_szukseges = self.frissito_kezelo.frissites_vegrehajtasa()
            if ujrainditas_szukseges:
                self._terminal_naplozas(uzenet, "WARNING")
                messagebox.showwarning("Frissítés Kész", f"{uzenet}\n\nKérjük indítsa újra az alkalmazást.")
            elif not siker:
                self._terminal_naplozas(uzenet, "WARNING")
            else:
                self._terminal_naplozas(uzenet, "INFO")
        threading.Thread(target=frissites_ellenorzes, daemon=True).start()

    def _frissitesek_ellenorzese_manualis(self):
        self._terminal_naplozas("Frissítések ellenőrzése...", "INFO")
        def frissites_ellenorzes():
            siker, uzenet, ujrainditas_szukseges = self.frissito_kezelo.frissites_vegrehajtasa()
            self.root.after(0, lambda: self._frissites_ellenorzes_befejezese(siker, uzenet, ujrainditas_szukseges))
        threading.Thread(target=frissites_ellenorzes, daemon=True).start()

    def _frissites_ellenorzes_befejezese(self, siker, uzenet, ujrainditas_szukseges):
        if ujrainditas_szukseges:
            self._terminal_naplozas(uzenet, "WARNING")
            if messagebox.askyesno("Frissítés Kész", f"{uzenet}\n\nSzeretné most újraindítani az alkalmazást?"):
                self._alkalmazas_ujrainditasa()
        elif siker:
            self._terminal_naplozas(uzenet, "INFO")
            if "frissítve" in uzenet.lower():
                messagebox.showinfo("Frissítés Ellenőrzés", uzenet)
        else:
            self._terminal_naplozas(uzenet, "ERROR")
            messagebox.showerror("Frissítési Hiba", uzenet)

    def _alkalmazas_ujrainditasa(self):
        self.logger.info("Alkalmazás újraindítása...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def _bezaras_kezelese(self):
        self.megfigyeles_leallitasa()
        self.logger.info("Alkalmazás bezárása")
        self.root.destroy()

def main():
    os.makedirs('logs', exist_ok=True)
    root = tk.Tk()
    app = RészvényFigyelő(root)
    root.protocol("WM_DELETE_WINDOW", app._bezaras_kezelese)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app._bezaras_kezelese()
    except Exception as e:
        logging.error(f"Alkalmazás hiba: {e}")
        messagebox.showerror("Hiba", f"Alkalmazás hiba: {e}")

if __name__ == "__main__":
    main()
