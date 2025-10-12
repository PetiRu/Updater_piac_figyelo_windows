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
from stocks import get_eu_reszvenyek
from update_handler import FrissitoKezelo

class RészvényFigyelő:
    def __init__(self, root):
        self.root = root
        self.root.title("EU Részvény Figyelő - Stochastic Szkanner v2.0.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Először a logolás beállítása
        self._logolas_beallitasa()
        
        # Komponensek inicializálása
        self._komponensek_beallitasa()
        
        # GUI beállítása
        self._gui_beallitasa()
        
        # Megfigyelési szál indítása
        self.megfigyeles_inditasa()
        
        # Frissítések ellenőrzése indításkor (nem blokkoló)
        self._frissitesek_ellenorzese_inditaskor()
    
    def _logolas_beallitasa(self):
        """Logolási konfiguráció beállítása"""
        # Logs könyvtár létrehozása ha nem létezik
        os.makedirs('logs', exist_ok=True)
        
        # Logolás beállítása
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
        """Alkalmazás komponensek inicializálása"""
        # Részvény adatok
        self.eu_reszvenyek = get_eu_reszvenyek()
        self.figyelt_reszvenyek = []
        
        # Stochastic alap paraméterek
        self.stochastic_kuszob = 20
        self.ellenorzes_intervallum = 300  # 5 perc teljes szkennelések között
        
        # Stochastic haladó paraméterek
        self.k_periodus = 14      # %K hossz
        self.k_simitas = 1        # %K simítás
        self.d_simitas = 3        # %D simítás
        
        # Jelzés típusa beállítások
        self.jelzes_tipusok = {
            "Alatta": "alatta",
            "Keresztezés (±3)": "keresztezes", 
            "Keresztezés fel": "keresztezes_fel",
            "Keresztezés le": "keresztezes_le"
        }
        self.aktualis_jelzes_tipus = "alatta"
        
        # Használt vonalak
        self.use_k_line = True
        self.use_d_line = False
        
        # Időkeret beállítások
        self.timeframe_opciok = {
            "1 Perc": "1m",
            "5 Perc": "5m", 
            "15 Perc": "15m",
            "1 Óra": "1h",
            "4 Óra": "4h",
            "1 Nap": "1d"
        }
        self.aktualis_timeframe = "1h"  # Alapértelmezett
        self.aktualis_timeframe_nev = "1 Óra"
        
        # Szálkezelés
        self.megfigyeles_aktiv = False
        self.megfigyeles_szal = None
        self.uzenet_verem = queue.Queue()
        
        # Frissítés kezelő
        self.frissito_kezelo = FrissitoKezelo()
        
        # Teljesítmény követés
        self.utolso_ellenorzes_ido = None
        self.ellenorzes_szamlalo = 0
        self.jelzesek_szamlalo = 0
        
        # Adat gyorsítótár redundáns API hívások elkerülésére
        self.reszveny_gyorsitotar = {}
        self.gyorsitotar_tartam = timedelta(minutes=5)
        
        # Előző értékek a keresztezésekhez
        self.elozo_ertekek = {}
    
    def _gui_beallitasa(self):
        """Grafikus felhasználói felület beállítása"""
        # Stílus beállítása
        self._stilusok_beallitasa()
        
        # Fő keret
        fos_keret = ttk.Frame(self.root, padding="10")
        fos_keret.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Rács súlyok beállítása
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        fos_keret.columnconfigure(1, weight=1)
        fos_keret.rowconfigure(1, weight=1)
        
        # Cím
        cim_cimke = ttk.Label(fos_keret, text="EU Részvény Figyelő - Stochastic Szkanner v2.0", 
                             font=('Arial', 16, 'bold'))
        cim_cimke.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Állapotsor
        self._allapotsor_beallitasa(fos_keret)
        
        # Vezérlő panel
        self._vezerlok_beallitasa(fos_keret)
        
        # Eredmények keret
        self._eredmenyek_keret_beallitasa(fos_keret)
        
        # Terminál keret
        self._terminal_keret_beallitasa(fos_keret)
        
        # Fő keret rács súlyok beállítása
        fos_keret.rowconfigure(1, weight=1)
        fos_keret.rowconfigure(3, weight=0)
        fos_keret.columnconfigure(1, weight=1)
        
        # Üzenetek feldolgozásának indítása a váróból
        self._uzenetek_feldolgozasa()
    
    def _stilusok_beallitasa(self):
        """Ttk stílusok konfigurálása"""
        stilus = ttk.Style()
        stilus.configure('Green.TButton', foreground='green')
        stilus.configure('Red.TButton', foreground='red')
        stilus.configure('Orange.TButton', foreground='orange')
    
    def _allapotsor_beallitasa(self, szulo):
        """Állapotsor beállítása indikátorokkal"""
        allapot_keret = ttk.Frame(szulo)
        allapot_keret.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Állapot indikátor
        self.allapot_valtozo = tk.StringVar(value="Inicializálás...")
        allapot_cimke = ttk.Label(allapot_keret, textvariable=self.allapot_valtozo, font=('Arial', 10, 'bold'))
        allapot_cimke.grid(row=0, column=0, sticky=tk.W)
        
        # Állapot szín indikátor
        self.allapot_canvas = tk.Canvas(allapot_keret, width=20, height=20, bg="orange", highlightthickness=1)
        self.allapot_canvas.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Időkeret információ
        self.timeframe_info_valtozo = tk.StringVar(value="Időkeret: 1 Óra")
        timeframe_cimke = ttk.Label(allapot_keret, textvariable=self.timeframe_info_valtozo, font=('Arial', 9))
        timeframe_cimke.grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Jelzés típus információ
        self.jelzes_info_valtozo = tk.StringVar(value="Jelzés: Alatta")
        jelzes_cimke = ttk.Label(allapot_keret, textvariable=self.jelzes_info_valtozo, font=('Arial', 9))
        jelzes_cimke.grid(row=0, column=3, sticky=tk.W, padx=(20, 0))
        
        # Szkennelési információk
        self.ellenorzes_info_valtozo = tk.StringVar(value="Szkennelések: 0 | Jelzések: 0")
        ellenorzes_cimke = ttk.Label(allapot_keret, textvariable=self.ellenorzes_info_valtozo, font=('Arial', 9))
        ellenorzes_cimke.grid(row=0, column=4, sticky=tk.E, padx=(0, 10))
        
        allapot_keret.columnconfigure(4, weight=1)
    
    def _vezerlok_beallitasa(self, szulo):
        """Vezérlő panel beállítása"""
        vezerlo_keret = ttk.LabelFrame(szulo, text="Vezérlők", padding="10")
        vezerlo_keret.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Első sor: Alap paraméterek
        elso_sor_keret = ttk.Frame(vezerlo_keret)
        elso_sor_keret.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Küszöb vezérlés
        kuszob_keret = ttk.Frame(elso_sor_keret)
        kuszob_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(kuszob_keret, text="Stochastic Küszöb:").grid(row=0, column=0, sticky=tk.W)
        self.kuszob_valtozo = tk.StringVar(value=str(self.stochastic_kuszob))
        kuszob_bevitel = ttk.Entry(kuszob_keret, textvariable=self.kuszob_valtozo, width=5)
        kuszob_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(kuszob_keret, text="Frissítés", 
                  command=self._kuszob_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Időkeret választás
        timeframe_keret = ttk.Frame(elso_sor_keret)
        timeframe_keret.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(timeframe_keret, text="Időkeret:").grid(row=0, column=0, sticky=tk.W)
        self.timeframe_valtozo = tk.StringVar(value=self.aktualis_timeframe_nev)
        timeframe_combobox = ttk.Combobox(timeframe_keret, 
                                         textvariable=self.timeframe_valtozo,
                                         values=list(self.timeframe_opciok.keys()),
                                         state="readonly", width=10)
        timeframe_combobox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        timeframe_combobox.bind('<<ComboboxSelected>>', self._timeframe_valtas)
        
        # Intervallum vezérlés
        intervallum_keret = ttk.Frame(elso_sor_keret)
        intervallum_keret.grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(intervallum_keret, text="Szkennelési Intervallum (perc):").grid(row=0, column=0, sticky=tk.W)
        self.intervallum_valtozo = tk.StringVar(value=str(self.ellenorzes_intervallum // 60))
        intervallum_bevitel = ttk.Entry(intervallum_keret, textvariable=self.intervallum_valtozo, width=5)
        intervallum_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(intervallum_keret, text="Frissítés", 
                  command=self._intervallum_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Második sor: Stochastic paraméterek
        masodik_sor_keret = ttk.LabelFrame(vezerlo_keret, text="Stochastic Paraméterek", padding="5")
        masodik_sor_keret.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # %K hossz
        k_hossz_keret = ttk.Frame(masodik_sor_keret)
        k_hossz_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(k_hossz_keret, text="%K Hossz:").grid(row=0, column=0, sticky=tk.W)
        self.k_hossz_valtozo = tk.StringVar(value=str(self.k_periodus))
        k_hossz_bevitel = ttk.Entry(k_hossz_keret, textvariable=self.k_hossz_valtozo, width=5)
        k_hossz_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(k_hossz_keret, text="Frissítés", 
                  command=self._k_hossz_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # %K simítás
        k_simitas_keret = ttk.Frame(masodik_sor_keret)
        k_simitas_keret.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(k_simitas_keret, text="%K Simítás:").grid(row=0, column=0, sticky=tk.W)
        self.k_simitas_valtozo = tk.StringVar(value=str(self.k_simitas))
        k_simitas_bevitel = ttk.Entry(k_simitas_keret, textvariable=self.k_simitas_valtozo, width=5)
        k_simitas_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(k_simitas_keret, text="Frissítés", 
                  command=self._k_simitas_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # %D simítás
        d_simitas_keret = ttk.Frame(masodik_sor_keret)
        d_simitas_keret.grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(d_simitas_keret, text="%D Simítás:").grid(row=0, column=0, sticky=tk.W)
        self.d_simitas_valtozo = tk.StringVar(value=str(self.d_simitas))
        d_simitas_bevitel = ttk.Entry(d_simitas_keret, textvariable=self.d_simitas_valtozo, width=5)
        d_simitas_bevitel.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Button(d_simitas_keret, text="Frissítés", 
                  command=self._d_simitas_frissitese).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Harmadik sor: Jelzés beállítások
        harmadik_sor_keret = ttk.LabelFrame(vezerlo_keret, text="Jelzés Beállítások", padding="5")
        harmadik_sor_keret.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Jelzés típusa
        jelzes_tipus_keret = ttk.Frame(harmadik_sor_keret)
        jelzes_tipus_keret.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(jelzes_tipus_keret, text="Jelzés Típusa:").grid(row=0, column=0, sticky=tk.W)
        self.jelzes_tipus_valtozo = tk.StringVar(value="Alatta")
        jelzes_tipus_combobox = ttk.Combobox(jelzes_tipus_keret, 
                                           textvariable=self.jelzes_tipus_valtozo,
                                           values=list(self.jelzes_tipusok.keys()),
                                           state="readonly", width=15)
        jelzes_tipus_combobox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        jelzes_tipus_combobox.bind('<<ComboboxSelected>>', self._jelzes_tipus_valtas)
        
        # Használt vonalak
        vonalak_keret = ttk.Frame(harmadik_sor_keret)
        vonalak_keret.grid(row=0, column=1, sticky=tk.W)
        
        self.use_k_valtozo = tk.BooleanVar(value=self.use_k_line)
        k_check = ttk.Checkbutton(vonalak_keret, text="%K vonal", variable=self.use_k_valtozo,
                                 command=self._vonalak_frissitese)
        k_check.grid(row=0, column=0, sticky=tk.W)
        
        self.use_d_valtozo = tk.BooleanVar(value=self.use_d_line)
        d_check = ttk.Checkbutton(vonalak_keret, text="%D vonal", variable=self.use_d_valtozo,
                                 command=self._vonalak_frissitese)
        d_check.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Negyedik sor: Vezérlő gombok
        gomb_keret = ttk.Frame(vezerlo_keret)
        gomb_keret.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        self.inditas_gomb = ttk.Button(gomb_keret, text="Megfigyelés Indítása", 
                                      command=self.megfigyeles_inditasa)
        self.inditas_gomb.grid(row=0, column=0, padx=(0, 5))
        
        self.leallas_gomb = ttk.Button(gomb_keret, text="Megfigyelés Leállítása", 
                                     command=self.megfigyeles_leallitasa, state='disabled')
        self.leallas_gomb.grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(gomb_keret, text="Frissítések Ellenőrzése", 
                  command=self._frissitesek_ellenorzese_manualis).grid(row=0, column=2, padx=(0, 5))
        
        ttk.Button(gomb_keret, text="Kényszer Szkennelés", 
                  command=self._kenyszer_ellenorzes).grid(row=0, column=3, padx=(0, 5))
        
        ttk.Button(gomb_keret, text="Paraméterek Mentése", 
                  command=self._parameterek_mentese).grid(row=0, column=4, padx=(0, 5))
        
        # Ötödik sor: Statisztika keret
        stat_keret = ttk.Frame(vezerlo_keret)
        stat_keret.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(stat_keret, text="Statisztikák:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        self.stat_valtozo = tk.StringVar(value="Részvények: 0 | Utolsó szkennelés: Soha")
        stat_cimke = ttk.Label(stat_keret, textvariable=self.stat_valtozo, font=('Arial', 8))
        stat_cimke.grid(row=1, column=0, sticky=tk.W)
        
        self._statisztikak_frissitese()
    
    def _eredmenyek_keret_beallitasa(self, szulo):
        """Eredmények megjelenítésének beállítása"""
        cim = f"Stochastic Jelzések ({self.aktualis_jelzes_tipus}) - {self.aktualis_timeframe_nev}"
        eredmeny_keret = ttk.LabelFrame(szulo, text=cim, padding="5")
        eredmeny_keret.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        eredmeny_keret.columnconfigure(0, weight=1)
        eredmeny_keret.rowconfigure(0, weight=1)
        
        # Eredmények szöveg terület
        self.eredmeny_szoveg = scrolledtext.ScrolledText(eredmeny_keret, width=80, height=15,
                                                        font=('Courier', 9), wrap=tk.NONE)
        self.eredmeny_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Görgetősávok hozzáadása
        v_gorgeto = ttk.Scrollbar(eredmeny_keret, orient=tk.VERTICAL, command=self.eredmeny_szoveg.yview)
        v_gorgeto.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.eredmeny_szoveg.configure(yscrollcommand=v_gorgeto.set)
        
        h_gorgeto = ttk.Scrollbar(eredmeny_keret, orient=tk.HORIZONTAL, command=self.eredmeny_szoveg.xview)
        h_gorgeto.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.eredmeny_szoveg.configure(xscrollcommand=h_gorgeto.set)
    
    def _terminal_keret_beallitasa(self, szulo):
        """Terminál kimenet beállítása"""
        terminal_keret = ttk.LabelFrame(szulo, text="Terminál Kimenet", padding="5")
        terminal_keret.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        terminal_keret.columnconfigure(0, weight=1)
        terminal_keret.rowconfigure(0, weight=1)
        
        self.terminal_szoveg = scrolledtext.ScrolledText(terminal_keret, width=120, height=12,
                                                        font=('Courier', 8), wrap=tk.WORD)
        self.terminal_szoveg.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Szöveg színek beállítása
        self.terminal_szoveg.tag_config("red", foreground="red")
        self.terminal_szoveg.tag_config("orange", foreground="orange")
        self.terminal_szoveg.tag_config("green", foreground="green")
        self.terminal_szoveg.tag_config("blue", foreground="blue")
        self.terminal_szoveg.tag_config("signal", foreground="green", background="#f0fff0")
    
    def _timeframe_valtas(self, event=None):
        """Időkeret váltás kezelése"""
        uj_timeframe_nev = self.timeframe_valtozo.get()
        if uj_timeframe_nev in self.timeframe_opciok:
            regi_timeframe = self.aktualis_timeframe_nev
            self.aktualis_timeframe_nev = uj_timeframe_nev
            self.aktualis_timeframe = self.timeframe_opciok[uj_timeframe_nev]
            
            # Gyorsítótár ürítése új időkeret miatt
            self.reszveny_gyorsitotar.clear()
            self.elozo_ertekek.clear()
            
            self._terminal_naplozas(f"Időkeret váltás: {regi_timeframe} -> {uj_timeframe_nev}", "INFO")
            self.timeframe_info_valtozo.set(f"Időkeret: {uj_timeframe_nev}")
            
            # Eredmények keret címének frissítése
            self._eredmenyek_cim_frissitese()
            
            self.logger.info(f"Időkeret váltva erre: {uj_timeframe_nev} ({self.aktualis_timeframe})")
    
    def _jelzes_tipus_valtas(self, event=None):
        """Jelzés típus váltás kezelése"""
        uj_jelzes_tipus_nev = self.jelzes_tipus_valtozo.get()
        if uj_jelzes_tipus_nev in self.jelzes_tipusok:
            regi_jelzes_tipus = self.aktualis_jelzes_tipus
            self.aktualis_jelzes_tipus = self.jelzes_tipusok[uj_jelzes_tipus_nev]
            
            # Előző értékek ürítése új jelzés típus miatt
            self.elozo_ertekek.clear()
            
            self._terminal_naplozas(f"Jelzés típus váltás: {regi_jelzes_tipus} -> {uj_jelzes_tipus_nev}", "INFO")
            self.jelzes_info_valtozo.set(f"Jelzés: {uj_jelzes_tipus_nev}")
            
            # Eredmények keret címének frissítése
            self._eredmenyek_cim_frissitese()
            
            self.logger.info(f"Jelzés típus váltva erre: {uj_jelzes_tipus_nev}")
    
    def _vonalak_frissitese(self):
        """Használt vonalak frissítése"""
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
        """Eredmények keret címének frissítése"""
        cim = f"Stochastic Jelzések ({self.jelzes_tipus_valtozo.get()}) - {self.aktualis_timeframe_nev}"
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and "Stochastic Jelzések" in widget.cget("text"):
                widget.config(text=cim)
                break
    
    def _kuszob_frissitese(self):
        """Stochastic küszöb frissítése"""
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
        """%K hossz frissítése"""
        try:
            uj_hossz = int(self.k_hossz_valtozo.get())
            if uj_hossz >= 1:
                regi_hossz = self.k_periodus
                self.k_periodus = uj_hossz
                
                # Gyorsítótár ürítése új paraméter miatt
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                
                self._terminal_naplozas(f"%K hossz frissítve: {regi_hossz} -> {uj_hossz}", "INFO")
                self.logger.info(f"%K hossz frissítve erre: {uj_hossz}")
            else:
                self._terminal_naplozas("A %K hossz legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %K hossz érték", "ERROR")
    
    def _k_simitas_frissitese(self):
        """%K simítás frissítése"""
        try:
            uj_simitas = int(self.k_simitas_valtozo.get())
            if uj_simitas >= 1:
                regi_simitas = self.k_simitas
                self.k_simitas = uj_simitas
                
                # Gyorsítótár ürítése új paraméter miatt
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                
                self._terminal_naplozas(f"%K simítás frissítve: {regi_simitas} -> {uj_simitas}", "INFO")
                self.logger.info(f"%K simítás frissítve erre: {uj_simitas}")
            else:
                self._terminal_naplozas("A %K simítás legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %K simítás érték", "ERROR")
    
    def _d_simitas_frissitese(self):
        """%D simítás frissítése"""
        try:
            uj_simitas = int(self.d_simitas_valtozo.get())
            if uj_simitas >= 1:
                regi_simitas = self.d_simitas
                self.d_simitas = uj_simitas
                
                # Gyorsítótár ürítése új paraméter miatt
                self.reszveny_gyorsitotar.clear()
                self.elozo_ertekek.clear()
                
                self._terminal_naplozas(f"%D simítás frissítve: {regi_simitas} -> {uj_simitas}", "INFO")
                self.logger.info(f"%D simítás frissítve erre: {uj_simitas}")
            else:
                self._terminal_naplozas("A %D simítás legalább 1 kell legyen", "ERROR")
        except ValueError:
            self._terminal_naplozas("Érvénytelen %D simítás érték", "ERROR")
    
    def _intervallum_frissitese(self):
        """Szkennelési intervallum frissítése"""
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
        """Paraméterek mentése konfigurációs fájlba"""
        try:
            config = {
                "verzio": "2.0.0",
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
        """Paraméterek betöltése konfigurációs fájlból"""
        try:
            if os.path.exists("parameters.json"):
                with open("parameters.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                # Paraméterek betöltése
                self.stochastic_kuszob = config.get("stochastic_kuszob", 20)
                self.k_periodus = config.get("k_periodus", 14)
                self.k_simitas = config.get("k_simitas", 1)
                self.d_simitas = config.get("d_simitas", 3)
                self.aktualis_jelzes_tipus = config.get("jelzes_tipus", "alatta")
                self.use_k_line = config.get("use_k_line", True)
                self.use_d_line = config.get("use_d_line", False)
                self.aktualis_timeframe = config.get("timeframe", "1h")
                self.ellenorzes_intervallum = config.get("ellenorzes_intervallum", 300)
                
                # GUI frissítése
                self.kuszob_valtozo.set(str(self.stochastic_kuszob))
                self.k_hossz_valtozo.set(str(self.k_periodus))
                self.k_simitas_valtozo.set(str(self.k_simitas))
                self.d_simitas_valtozo.set(str(self.d_simitas))
                self.use_k_valtozo.set(self.use_k_line)
                self.use_d_valtozo.set(self.use_d_line)
                self.intervallum_valtozo.set(str(self.ellenorzes_intervallum // 60))
                
                # Jelzés típus és időkeret
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
        """Statisztikák megjelenítésének frissítése"""
        stat_szoveg = f"Részvények: {len(self.eu_reszvenyek)} | Utolsó szkennelés: {self.utolso_ellenorzes_ido or 'Soha'}"
        self.stat_valtozo.set(stat_szoveg)
        self.ellenorzes_info_valtozo.set(f"Szkennelések: {self.ellenorzes_szamlalo} | Jelzések: {self.jelzesek_szamlalo}")
    
    def _get_period_for_timeframe(self):
        """Időkerethez tartozó időtartam meghatározása"""
        timeframe_period_map = {
            "1m": "7d",   # 1 perc - max 7 nap
            "5m": "60d",  # 5 perc - max 60 nap
            "15m": "60d", # 15 perc - max 60 nap
            "1h": "730d", # 1 óra - max 2 év
            "4h": "730d", # 4 óra - max 2 év
            "1d": "730d"  # 1 nap - max 2 év
        }
        return timeframe_period_map.get(self.aktualis_timeframe, "60d")
    
    def _stochastic_szamitas(self, szimbolum):
        """Stochastic oszcillátor számítása a három paraméterrel"""
        # Gyorsítótár kulcs az összes paraméterrel
        gyorsitotar_kulcs = f"{szimbolum}_{self.aktualis_timeframe}_{self.k_periodus}_{self.k_simitas}_{self.d_simitas}"
        
        if gyorsitotar_kulcs in self.reszveny_gyorsitotar:
            gyorsitotar_ido, gyorsitotartott_ertek = self.reszveny_gyorsitotar[gyorsitotar_kulcs]
            if datetime.now() - gyorsitotar_ido < self.gyorsitotar_tartam:
                return gyorsitotartott_ertek
        
        try:
            reszveny = yf.Ticker(szimbolum)
            period = self._get_period_for_timeframe()
            
            # Adatok letöltése a kiválasztott időkerettel
            elozmeny = reszveny.history(period=period, interval=self.aktualis_timeframe)
            
            if len(elozmeny) < self.k_periodus + max(self.k_simitas, self.d_simitas):
                self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (None, None))
                return (None, None)
            
            # Alap %K számítása
            also_min = elozmeny['Low'].rolling(window=self.k_periodus).min()
            felso_max = elozmeny['High'].rolling(window=self.k_periodus).max()
            
            # Nullával való osztás elkerülése
            nevezo = (felso_max - also_min)
            nevezo = nevezo.replace(0, 0.001)
            
            raw_k = 100 * (elozmeny['Close'] - also_min) / nevezo
            
            # %K simítás
            if self.k_simitas > 1:
                k_ertek = raw_k.rolling(window=self.k_simitas).mean()
            else:
                k_ertek = raw_k
            
            # %D simítás (%K simított értékének további simítása)
            if self.d_simitas > 1:
                d_ertek = k_ertek.rolling(window=self.d_simitas).mean()
            else:
                d_ertek = k_ertek
            
            k_final = k_ertek.iloc[-1] if not pd.isna(k_ertek.iloc[-1]) else None
            d_final = d_ertek.iloc[-1] if not pd.isna(d_ertek.iloc[-1]) else None
            
            # Gyorsítótár frissítése
            self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (k_final, d_final))
            
            return (k_final, d_final)
            
        except Exception as e:
            self._terminal_naplozas(f"Hiba stochastic számításakor {szimbolum}: {e}", "ERROR")
            self.reszveny_gyorsitotar[gyorsitotar_kulcs] = (datetime.now(), (None, None))
            return (None, None)
    
    def _jelzes_ellenorzes(self, szimbolum, k_ertek, d_ertek):
        """Jelzés ellenőrzése a kiválasztott típus szerint"""
        kulcs = f"{szimbolum}_{self.aktualis_timeframe}"
        elozo_k, elozo_d = self.elozo_ertekek.get(kulcs, (None, None))
        
        # Aktuális értékek mentése
        self.elozo_ertekek[kulcs] = (k_ertek, d_ertek)
        
        # Érvénytelen értékek ellenőrzése
        if k_ertek is None or (self.use_d_line and d_ertek is None):
            return False
        
        hasznalt_ertek = None
        if self.use_k_line and not self.use_d_line:
            hasznalt_ertek = k_ertek
        elif not self.use_k_line and self.use_d_line:
            hasznalt_ertek = d_ertek
        elif self.use_k_line and self.use_d_line:
            # Mindkét vonal használata esetén a %K-t használjuk
            hasznalt_ertek = k_ertek
        
        if hasznalt_ertek is None:
            return False
        
        # Jelzés típusok szerinti ellenőrzés
        if self.aktualis_jelzes_tipus == "alatta":
            return hasznalt_ertek < self.stochastic_kuszob
        
        elif self.aktualis_jelzes_tipus == "keresztezes":
            if elozo_k is None:
                return False
            # ±3 tolerancia melletti keresztezés
            return ((elozo_k < self.stochastic_kuszob - 3 and k_ertek >= self.stochastic_kuszob - 3) or
                   (elozo_k >= self.stochastic_kuszob + 3 and k_ertek < self.stochastic_kuszob + 3))
        
        elif self.aktualis_jelzes_tipus == "keresztezes_fel":
            if elozo_k is None:
                return False
            # Felfelé keresztezés
            return elozo_k < self.stochastic_kuszob and k_ertek >= self.stochastic_kuszob
        
        elif self.aktualis_jelzes_tipus == "keresztezes_le":
            if elozo_k is None:
                return False
            # Lefelé keresztezés
            return elozo_k >= self.stochastic_kuszob and k_ertek < self.stochastic_kuszob
        
        return False
    
    def _reszvenyek_figyelese(self):
        """Fő megfigyelési függvény"""
        self.megfigyeles_aktiv = True
        self._allapot_frissitese("green", "Megfigyelés aktív")
        self._terminal_naplozas(f"Részvény megfigyelés elindítva - Időkeret: {self.aktualis_timeframe_nev}, Jelzés: {self.jelzes_tipus_valtozo.get()}", "INFO")
        self.logger.info(f"Részvény megfigyelési szál elindítva - Időkeret: {self.aktualis_timeframe_nev}")
        
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
                    
                    # Haladás frissítése időszakosan
                    if i % 10 == 0:
                        haladás = (i + 1) / osszes_reszveny * 100
                        self._allapot_frissitese("green", f"Szkennelés... {haladás:.1f}% ({self.aktualis_timeframe_nev})")
                    
                    # Stochastic számítás
                    k_ertek, d_ertek = self._stochastic_szamitas(szimbolum)
                    feldolgozott_reszvenyek += 1
                    
                    if k_ertek is None:
                        hibak += 1
                        continue
                    
                    # Jelzés ellenőrzése
                    if self._jelzes_ellenorzes(szimbolum, k_ertek, d_ertek):
                        vonal_info = []
                        if self.use_k_line:
                            vonal_info.append(f"K%: {k_ertek:.2f}")
                        if self.use_d_line:
                            vonal_info.append(f"D%: {d_ertek:.2f}")
                        
                        jelzes = {
                            'szimbolum': szimbolum,
                            'k_ertek': k_ertek,
                            'd_ertek': d_ertek,
                            'idobelyeg': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'timeframe': self.aktualis_timeframe_nev,
                            'jelzes_tipus': self.jelzes_tipus_valtozo.get(),
                            'vonal_info': ", ".join(vonal_info)
                        }
                        jelzesek.append(jelzes)
                        
                        # Jelzés naplózása
                        vonal_szoveg = ", ".join(vonal_info)
                        uzenet = f"JELZÉS: {szimbolum} - {vonal_szoveg} ({self.aktualis_timeframe_nev}, {self.jelzes_tipus_valtozo.get()})"
                        self._terminal_naplozas(uzenet, "signal")
                        self.logger.info(uzenet)
                
                # Eredmények frissítése
                self.utolso_ellenorzes_ido = datetime.now().strftime("%H:%M:%S")
                self.ellenorzes_szamlalo += 1
                self.jelzesek_szamlalo += len(jelzesek)
                
                # UI frissítés várólistába helyezése
                self.uzenet_verem.put(('eredmenyek_frissitese', jelzesek))
                self.uzenet_verem.put(('statisztikak_frissitese', None))
                
                # Szkennelés befejezésének naplózása
                self._terminal_naplozas(
                    f"Szkennelés befejezve ({self.aktualis_timeframe_nev}, {self.jelzes_tipus_valtozo.get()}): {feldolgozott_reszvenyek} feldolgozva, {len(jelzesek)} jelzés, {hibak} hiba", 
                    "INFO" if hibak == 0 else "WARNING"
                )
                
                # Várakozás következő szkennelés előtt megszakítható alvással
                self._terminal_naplozas(f"Következő szkennelés {self.ellenorzes_intervallum//60} perc múlva...", "INFO")
                for i in range(self.ellenorzes_intervallum):
                    if not self.megfigyeles_aktiv:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self._allapot_frissitese("red", f"Megfigyelési hiba: {e}")
                self._terminal_naplozas(f"Megfigyelési hiba ({self.aktualis_timeframe_nev}): {e}", "ERROR")
                self.logger.error(f"Megfigyelési hiba ({self.aktualis_timeframe_nev}): {e}")
                
                # Újrapróbálkozás előtti várakozás
                for i in range(60):
                    if not self.megfigyeles_aktiv:
                        break
                    time.sleep(1)
    
    def _eredmenyek_frissitese(self, jelzesek):
        """Eredmények megjelenítésének frissítése a fő szálban"""
        self.eredmeny_szoveg.delete(1.0, tk.END)
        
        if not jelzesek:
            self.eredmeny_szoveg.insert(tk.END, f"Nem található részvény {self.jelzes_tipus_valtozo.get()} jelzéssel ({self.aktualis_timeframe_nev})")
            return
        
        # Fejléc
        fejlec = f"{'Szimbólum':<15} {'K%':<8} {'D%':<8} {'Jelzés':<15} {'Időkeret':<10} {'Idő':<20}\n"
        self.eredmeny_szoveg.insert(tk.END, fejlec)
        self.eredmeny_szoveg.insert(tk.END, "-" * 85 + "\n")
        
        # Jelzések rendezése K% érték szerint
        for jelzes in sorted(jelzesek, key=lambda x: x['k_ertek']):
            k_ertek = f"{jelzes['k_ertek']:.2f}" if jelzes['k_ertek'] is not None else "N/A"
            d_ertek = f"{jelzes['d_ertek']:.2f}" if jelzes['d_ertek'] is not None else "N/A"
            sor = f"{jelzes['szimbolum']:<15} {k_ertek:<8} {d_ertek:<8} {jelzes['jelzes_tipus']:<15} {jelzes['timeframe']:<10} {jelzes['idobelyeg']:<20}\n"
            self.eredmeny_szoveg.insert(tk.END, sor)
    
    def _terminal_naplozas(self, uzenet, szint="INFO"):
        """Üzenet naplózása terminálba színkódolással (szálbiztos)"""
        self.uzenet_verem.put(('naplo', (uzenet, szint)))
    
    def _allapot_frissitese(self, szin, uzenet):
        """Állapot indikátor és üzenet frissítése (szálbiztos)"""
        self.uzenet_verem.put(('allapot', (szin, uzenet)))
    
    def _uzenetek_feldolgozasa(self):
        """Üzenetek feldolgozása a váróból a fő szálban"""
        try:
            while True:
                try:
                    uzenet_tipus, adatok = self.uzenet_verem.get_nowait()
                    
                    if uzenet_tipus == 'naplo':
                        uzenet, szint = adatok
                        self._terminal_naplozas_ui(uzenet, szint)
                    elif uzenet_tipus == 'allapot':
                        szin, uzenet = adatok
                        self._allapot_frissitese_ui(szin, uzenet)
                    elif uzenet_tipus == 'eredmenyek_frissitese':
                        self._eredmenyek_frissitese(adatok)
                    elif uzenet_tipus == 'statisztikak_frissitese':
                        self._statisztikak_frissitese()
                        
                except queue.Empty:
                    break
        except Exception as e:
            self.logger.error(f"Hiba üzenetek feldolgozásakor: {e}")
        
        # Következő feldolgozás ütemezése
        self.root.after(100, self._uzenetek_feldolgozasa)
    
    def _terminal_naplozas_ui(self, uzenet, szint):
        """Terminál UI frissítése fő szálban"""
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
        """Állapot UI frissítése fő szálban"""
        self.allapot_canvas.configure(bg=szin)
        self.allapot_valtozo.set(uzenet)
    
    def megfigyeles_inditasa(self):
        """Megfigyelési szál indítása"""
        if not self.megfigyeles_aktiv:
            # Paraméterek betöltése indítás előtt
            self._parameterek_betoltese()
            
            self.megfigyeles_aktiv = True
            self.megfigyeles_szal = threading.Thread(target=self._reszvenyek_figyelese, daemon=True)
            self.megfigyeles_szal.start()
            
            self.inditas_gomb.config(state='disabled')
            self.leallas_gomb.config(state='normal')
            
            self._terminal_naplozas("Megfigyelés elindítva", "INFO")
            self.logger.info("Megfigyelés felhasználó által elindítva")
    
    def megfigyeles_leallitasa(self):
        """Megfigyelési szál leállítása"""
        self.megfigyeles_aktiv = False
        self._allapot_frissitese("orange", "Megfigyelés leállítva")
        
        self.inditas_gomb.config(state='normal')
        self.leallas_gomb.config(state='disabled')
        
        self._terminal_naplozas("Megfigyelés leállítva", "INFO")
        self.logger.info("Megfigyelés felhasználó által leállítva")
    
    def _kenyszer_ellenorzes(self):
        """Azonnali szkennelés kényszerítése"""
        if self.megfigyeles_aktiv:
            self._terminal_naplozas("Szkennelés már folyamatban van", "INFO")
        else:
            self._terminal_naplozas("Kézi szkennelés kérés...", "INFO")
            # Kézi szkennelés logika implementálása itt
            # Egyelőre csak naplózzuk, hogy a funkciót implementálni kell
            self._terminal_naplozas("Kézi szkennelés funkció implementálásra vár", "INFO")
    
    def _frissitesek_ellenorzese_inditaskor(self):
        """Frissítések ellenőrzése indításkor külön szálban"""
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
        """Kézi frissítés ellenőrzés"""
        self._terminal_naplozas("Frissítések ellenőrzése...", "INFO")
        
        def frissites_ellenorzes():
            siker, uzenet, ujrainditas_szukseges = self.frissito_kezelo.frissites_vegrehajtasa()
            self.root.after(0, lambda: self._frissites_ellenorzes_befejezese(siker, uzenet, ujrainditas_szukseges))
        
        threading.Thread(target=frissites_ellenorzes, daemon=True).start()
    
    def _frissites_ellenorzes_befejezese(self, siker, uzenet, ujrainditas_szukseges):
        """Frissítés ellenőrzés befejezésének kezelése fő szálban"""
        if ujrainditas_szukseges:
            self._terminal_naplozas(uzenet, "WARNING")
            if messagebox.askyesno("Frissítés Kész", 
                                 f"{uzenet}\n\nSzeretné most újraindítani az alkalmazást?"):
                self._alkalmazas_ujrainditasa()
        elif siker:
            self._terminal_naplozas(uzenet, "INFO")
            if "frissítve" in uzenet.lower():
                messagebox.showinfo("Frissítés Ellenőrzés", uzenet)
        else:
            self._terminal_naplozas(uzenet, "ERROR")
            messagebox.showerror("Frissítési Hiba", uzenet)
    
    def _alkalmazas_ujrainditasa(self):
        """Alkalmazás újraindítása"""
        self.logger.info("Alkalmazás újraindítása...")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    def _bezaras_kezelese(self):
        """Alkalmazás bezárásának kezelése"""
        self.megfigyeles_leallitasa()
        self.logger.info("Alkalmazás bezárása")
        self.root.destroy()

def main():
    # Logs könyvtár létrehozása
    os.makedirs('logs', exist_ok=True)
    
    # GUI indítása
    root = tk.Tk()
    app = RészvényFigyelő(root)
    
    # Ablak bezárásának kezelése
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
