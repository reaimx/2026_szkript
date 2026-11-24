
import tkinter as tk
from tkinter import ttk

from vzs_halozat import VZSHalozat, vzs_meret_formazas


class VZSHalozatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hálózatfigyelő")
        self.root.geometry("400x220")
        self.root.resizable(False, False)

        self.halozat = VZSHalozat()
        self.adapterek = []
        self.meres_aktiv = False
        self.idozito = None

        self.adapter_valasztas = tk.StringVar()
        self.allapot = tk.StringVar(value="Nincs kapcsolat")
        self.ip = tk.StringVar(value="IP-cím: -")
        self.letoltes = tk.StringVar(value="0.00 MB/s")
        self.feltoltes = tk.StringVar(value="0.00 MB/s")
        self.fogadott = tk.StringVar(value="Összesen: -")
        self.kuldott = tk.StringVar(value="Összesen: -")

        self.felulet_letrehozasa()
        self.adapterek_frissitese()
        self.stop_gomb.config(state="disabled")
        self.allapot.set("Mérés leállítva")

    def felulet_letrehozasa(self):
        keret = ttk.Frame(self.root, padding=10)
        keret.pack(fill="both", expand=True)

        ttk.Label(
            keret,
            text="Válassz hálózati adaptert:"
        ).pack(anchor="w", pady=(0, 4))

        self.adapter_lista = ttk.Combobox(
            keret,
            textvariable=self.adapter_valasztas,
            state="readonly"
        )
        self.adapter_lista.pack(fill="x", pady=(0, 7))
        self.adapter_lista.bind(
            "<<ComboboxSelected>>",
            self.adapter_kivalasztva
        )

        info = ttk.Frame(keret)
        info.pack(fill="x", pady=(0, 7))

        ttk.Label(
            info,
            textvariable=self.ip
        ).pack(side="left")

        ttk.Label(
            info,
            textvariable=self.allapot
        ).pack(side="right")

        sebesseg_keret = ttk.Frame(keret)
        sebesseg_keret.pack(fill="x")

        sebesseg_keret.columnconfigure(
            0, weight=1, uniform="kartya"
        )
        sebesseg_keret.columnconfigure(
            1, weight=1, uniform="kartya"
        )

        le_keret = ttk.LabelFrame(
            sebesseg_keret,
            text="Letöltés",
            padding=8
        )
        le_keret.grid(
            row=0, column=0, sticky="nsew", padx=(0, 4)
        )

        fel_keret = ttk.LabelFrame(
            sebesseg_keret,
            text="Feltöltés",
            padding=8
        )
        fel_keret.grid(
            row=0, column=1, sticky="nsew", padx=(4, 0)
        )

        ttk.Label(
            le_keret,
            textvariable=self.fogadott,
            font=("Arial", 9)
        ).pack(anchor="w")

        ttk.Label(
            le_keret,
            textvariable=self.letoltes,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(5, 0))

        ttk.Label(
            fel_keret,
            textvariable=self.kuldott,
            font=("Arial", 9)
        ).pack(anchor="w")

        ttk.Label(
            fel_keret,
            textvariable=self.feltoltes,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(5, 0))

        gombok = ttk.Frame(keret)
        gombok.pack(side="bottom", fill="x", pady=(6, 0))

        for i in range(4):
            gombok.columnconfigure(i, weight=1, uniform="gomb")

        self.start_gomb = ttk.Button(
            gombok,
            text="Start",
            command=self.meres_inditasa
        )
        self.start_gomb.grid(
            row=0, column=0, sticky="ew", padx=(0, 3)
        )

        self.stop_gomb = ttk.Button(
            gombok,
            text="Stop",
            command=self.meres_leallitasa
        )
        self.stop_gomb.grid(
            row=0, column=1, sticky="ew", padx=3
        )

        ttk.Button(
            gombok,
            text="Bezárás",
            command=self.root.destroy
        ).grid(
            row=0, column=3, sticky="ew", padx=(3, 0)
        )

    def adapterek_frissitese(self):
        try:
            self.adapterek = self.halozat.aktiv_adapterek()
        except (OSError, RuntimeError):
            self.adapterek = []

        nevek = [
            f"{adapter['nev']} - {adapter['ip']}"
            for adapter in self.adapterek
        ]
        self.adapter_lista["values"] = nevek

        if self.adapterek:
            self.adapter_lista.current(0)
        else:
            self.adapter_valasztas.set("")
            self.adatok_torlese()

    def adapter_kivalasztva(self, event):
        self.halozat.meres_nullazasa()
        if self.meres_aktiv:
            self.adatok_frissitese()

    def adatok_frissitese(self):
        index = self.adapter_lista.current()

        if not 0 <= index < len(self.adapterek):
            self.adatok_torlese()
            return

        nev = self.adapterek[index]["nev"]

        try:
            adatok = self.halozat.adatok_lekerese(nev)
        except (OSError, RuntimeError):
            adatok = None
            self.halozat.meres_nullazasa()

        if adatok is None:
            self.adatok_torlese()
            return

        self.ip.set(f"IP-cím: {adatok['ip']}")
        self.allapot.set("Mérés aktív")
        self.letoltes.set(f"{adatok['letoltes']:.2f} MB/s")
        self.feltoltes.set(f"{adatok['feltoltes']:.2f} MB/s")
        self.fogadott.set(
            f"Összesen: {vzs_meret_formazas(adatok['fogadott'])}"
        )
        self.kuldott.set(
            f"Összesen: {vzs_meret_formazas(adatok['kuldott'])}"
        )

    def adatok_torlese(self):
        self.ip.set("IP-cím: -")
        self.allapot.set("Nincs kapcsolat")
        self.letoltes.set("0.00 MB/s")
        self.feltoltes.set("0.00 MB/s")
        self.fogadott.set("Összesen: -")
        self.kuldott.set("Összesen: -")

    def meres_inditasa(self):
        if self.meres_aktiv:
            return

        self.meres_aktiv = True
        self.halozat.meres_nullazasa()
        self.start_gomb.config(state="disabled")
        self.stop_gomb.config(state="normal")
        self.adatok_frissitese()
        self.idozito = self.root.after(
            1000, self.automatikus_frissites
        )

    def meres_leallitasa(self):
        if not self.meres_aktiv:
            return

        self.meres_aktiv = False

        if self.idozito is not None:
            self.root.after_cancel(self.idozito)
            self.idozito = None

        self.start_gomb.config(state="normal")
        self.stop_gomb.config(state="disabled")
        self.allapot.set("Mérés leállítva")

    def automatikus_frissites(self):
        self.idozito = None

        if not self.meres_aktiv:
            return

        self.adatok_frissitese()
        self.idozito = self.root.after(
            1000, self.automatikus_frissites
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = VZSHalozatApp(root)
    root.mainloop()
