
import tkinter as tk
from tkinter import ttk, messagebox

from vzs_halozat import VZSHalozat, vzs_meret_formazas


class VZSHalozatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hálózatfigyelő")
        self.root.geometry("480x460")
        self.root.resizable(False, False)

        self.halozat = VZSHalozat()
        self.adapterek = []

        self.adapter_valasztas = tk.StringVar()
        self.ip = tk.StringVar(value="-")
        self.allapot = tk.StringVar(value="-")
        self.sebesseg = tk.StringVar(value="-")
        self.kuldott = tk.StringVar(value="-")
        self.fogadott = tk.StringVar(value="-")

        self.felulet_letrehozasa()
        self.adapterek_frissitese()

    def felulet_letrehozasa(self):
        keret = ttk.Frame(self.root, padding=20)
        keret.pack(fill="both", expand=True)

        ttk.Label(
            keret,
            text="Hálózatfigyelő",
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            keret,
            text="Hálózati adapterek és adatforgalom"
        ).pack(anchor="w", pady=(0, 20))

        ttk.Label(
            keret,
            text="Hálózati adapter:"
        ).pack(anchor="w")

        self.adapter_lista = ttk.Combobox(
            keret,
            textvariable=self.adapter_valasztas,
            state="readonly"
        )
        self.adapter_lista.pack(fill="x", pady=(5, 15))
        self.adapter_lista.bind(
            "<<ComboboxSelected>>",
            self.adapter_kivalasztva
        )

        adatok_keret = ttk.LabelFrame(
            keret,
            text="Hálózati információk",
            padding=15
        )
        adatok_keret.pack(fill="x")

        mezok = [
            ("IP-cím:", self.ip),
            ("Állapot:", self.allapot),
            ("Kapcsolati sebesség:", self.sebesseg),
            ("Összes küldött adat:", self.kuldott),
            ("Összes fogadott adat:", self.fogadott)
        ]

        for sor, (felirat, valtozo) in enumerate(mezok):
            ttk.Label(
                adatok_keret,
                text=felirat
            ).grid(row=sor, column=0, sticky="w", pady=6)

            ttk.Label(
                adatok_keret,
                textvariable=valtozo
            ).grid(row=sor, column=1, sticky="e", padx=(15, 0), pady=6)

        adatok_keret.columnconfigure(1, weight=1)

        ttk.Button(
            keret,
            text="Frissítés",
            command=self.adapterek_frissitese
        ).pack(pady=20)

    def adapterek_frissitese(self):
        elozo_nev = None
        index = self.adapter_lista.current()

        if 0 <= index < len(self.adapterek):
            elozo_nev = self.adapterek[index]["nev"]

        try:
            self.adapterek = self.halozat.aktiv_adapterek()
        except (OSError, RuntimeError) as hiba:
            messagebox.showerror("Hiba", str(hiba))
            return

        nevek = [
            f"{adapter['nev']} - {adapter['ip']}"
            for adapter in self.adapterek
        ]

        self.adapter_lista["values"] = nevek

        if not self.adapterek:
            self.adapter_valasztas.set("")
            self.adatok_torlese()
            return

        uj_index = 0

        for i, adapter in enumerate(self.adapterek):
            if adapter["nev"] == elozo_nev:
                uj_index = i
                break

        self.adapter_lista.current(uj_index)
        self.adatok_frissitese()

    def adapter_kivalasztva(self, event):
        self.adatok_frissitese()

    def adatok_frissitese(self):
        index = self.adapter_lista.current()

        if not 0 <= index < len(self.adapterek):
            self.adatok_torlese()
            return

        nev = self.adapterek[index]["nev"]

        try:
            adatok = self.halozat.adatok_lekerese(nev)
        except (OSError, RuntimeError) as hiba:
            messagebox.showerror("Hiba", str(hiba))
            self.adatok_torlese()
            return

        if adatok is None:
            self.adatok_torlese()
            return

        self.ip.set(adatok["ip"])
        self.allapot.set(adatok["allapot"])

        if adatok["sebesseg"] > 0:
            self.sebesseg.set(f'{adatok["sebesseg"]} Mbps')
        else:
            self.sebesseg.set("Nem elérhető")

        self.kuldott.set(
            vzs_meret_formazas(adatok["kuldott"])
        )
        self.fogadott.set(
            vzs_meret_formazas(adatok["fogadott"])
        )

    def adatok_torlese(self):
        self.ip.set("-")
        self.allapot.set("-")
        self.sebesseg.set("-")
        self.kuldott.set("-")
        self.fogadott.set("-")


if __name__ == "__main__":
    root = tk.Tk()
    app = VZSHalozatApp(root)
    root.mainloop()
