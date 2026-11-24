
import socket
import time
import psutil


def vzs_meret_formazas(bajtok):
    if bajtok >= 1000 ** 3:
        return f"{bajtok / 1000 ** 3:.2f} GB"
    if bajtok >= 1000 ** 2:
        return f"{bajtok / 1000 ** 2:.2f} MB"
    if bajtok >= 1000:
        return f"{bajtok / 1000:.2f} KB"
    return f"{bajtok} B"


class VZSHalozat:
    def __init__(self):
        self.elozo_nev = None
        self.elozo_ido = None
        self.elozo_kuldott = 0
        self.elozo_fogadott = 0

    def meres_nullazasa(self):
        self.elozo_nev = None
        self.elozo_ido = None
        self.elozo_kuldott = 0
        self.elozo_fogadott = 0

    def aktiv_adapterek(self):
        cimek = psutil.net_if_addrs()
        allapotok = psutil.net_if_stats()
        eredmeny = []

        for nev, stat in allapotok.items():
            if not stat.isup:
                continue

            for cim in cimek.get(nev, []):
                if cim.family == socket.AF_INET:
                    if not cim.address.startswith("127."):
                        eredmeny.append({
                            "nev": nev,
                            "ip": cim.address
                        })
                        break

        return eredmeny

    def adatok_lekerese(self, nev):
        cimek = psutil.net_if_addrs()
        allapotok = psutil.net_if_stats()
        forgalom = psutil.net_io_counters(pernic=True)

        stat = allapotok.get(nev)
        adatok = forgalom.get(nev)

        if stat is None or not stat.isup or adatok is None:
            self.meres_nullazasa()
            return None

        ip = None

        for cim in cimek.get(nev, []):
            if cim.family == socket.AF_INET:
                if not cim.address.startswith("127."):
                    ip = cim.address
                    break

        if ip is None:
            self.meres_nullazasa()
            return None

        most = time.monotonic()
        kuldott = adatok.bytes_sent
        fogadott = adatok.bytes_recv
        letoltes = 0.0
        feltoltes = 0.0

        if self.elozo_nev == nev and self.elozo_ido is not None:
            eltelt = most - self.elozo_ido
            le_kulonbseg = fogadott - self.elozo_fogadott
            fel_kulonbseg = kuldott - self.elozo_kuldott

            if eltelt > 0 and le_kulonbseg >= 0 and fel_kulonbseg >= 0:
                letoltes = le_kulonbseg / eltelt / 1000000
                feltoltes = fel_kulonbseg / eltelt / 1000000

        self.elozo_nev = nev
        self.elozo_ido = most
        self.elozo_kuldott = kuldott
        self.elozo_fogadott = fogadott

        return {
            "adapter": nev,
            "ip": ip,
            "letoltes": letoltes,
            "feltoltes": feltoltes,
            "fogadott": fogadott,
            "kuldott": kuldott
        }
