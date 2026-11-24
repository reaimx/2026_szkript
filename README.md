Hálózatfigyelő
Készítette: Vitárius Zsolt
A program leírása
A Hálózatfigyelő egy Python nyelven készült, grafikus alkalmazás, amely a számítógép hálózati adatforgalmát figyeli.
A felhasználó kiválaszthatja a hálózati adaptert, majd a Start gombbal elindíthatja a mérést. A program másodpercenként megjeleníti az aktuális letöltési és feltöltési sebességet, valamint az összesített adatforgalmat. A mérés a Stop gombbal leállítható.
A program felépítése
	•	main.py – A program indítása, grafikus felület és eseménykezelés.
	•	vzs_halozat.py – Saját modul, a hálózati adatok lekérdezése és feldolgozása.
	•	README.md – A program dokumentációja.
Felhasznált modulok és függvények
tkinter, tkinter.ttk – grafikus felület
A program ablakának, gombjainak, feliratainak és legördülő listájának létrehozása. Eseménykezelés és automatikus frissítés.
psutil – bemutatandó modul
	•	net_if_addrs() – Hálózati adapterek IP-címeinek lekérdezése.
	•	net_if_stats() – Hálózati adapterek állapotának lekérdezése.
	•	net_io_counters() – Küldött és fogadott adatmennyiség lekérdezése.
socket – beépített modul
	•	AF_INET – IPv4-címek azonosítása.
time – beépített modul
	•	monotonic() – A mérések között eltelt idő meghatározása.
vzs_halozat – saját modul
	•	vzs_meret_formazas() – Az adatmennyiség átalakítása olvasható mértékegységekre.
Osztályok és metódusok
VZSHalozat – A hálózati adatok kezelése.
	•	aktiv_adapterek() – Aktív adapterek lekérdezése.
	•	adatok_lekerese() – Adatforgalom és sebesség kiszámítása.
	•	meres_nullazasa() – A mérés alaphelyzetbe állítása.
VZSHalozatApp – A grafikus felület kezelése.
	•	felulet_letrehozasa() – Grafikus elemek létrehozása.
	•	meres_inditasa() – Mérés indítása.
	•	meres_leallitasa() – Mérés leállítása.
	•	automatikus_frissites() – Adatok rendszeres frissítése.
Szükséges modulok és indítás
A programhoz Python 3 és a psutil csomag szükséges. A többi felhasznált modul a Python része.
Telepítés:
python -m pip install psutil
Indítás:
python main.py
