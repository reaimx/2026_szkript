
import socket
import psutil


def vzs_meret_formazas(bajtok):
    if bajtok >= 1024 ** 3:
        return f"{bajtok / 1024 ** 3:.2f} GB"
    if bajtok >= 1024 ** 2:
        return f"{bajtok / 1024 ** 2:.2f} MB"
    if bajtok >= 1024:
        return f"{bajtok / 1024:.2f} KB"
    return f"{bajtok} B"


class VZSHalozat:
    def __init__(self):
        self.adapterek = {}
        self.statisztikak = {}
        self.forgalom = {}

    def frissites(self):
        self.adapterek = psutil.net_if_addrs()
        self.statisztikak = psutil.net_if_stats()
        self.forgalom = psutil.net_io_counters(pernic=True)

    def aktiv_adapterek(self):
        self.frissites()
        eredmeny = []

        for nev, stat in self.statisztikak.items():
            if not stat.isup:
                continue

            for cim in self.adapterek.get(nev, []):
                if cim.family == socket.AF_INET:
                    if not cim.address.startswith("127."):
                        eredmeny.append({
                            "nev": nev,
                            "ip": cim.address
                        })
                    break

        return eredmeny

    def adatok_lekerese(self, nev):
        self.frissites()

        stat = self.statisztikak.get(nev)

        if stat is None or not stat.isup:
            return None

        ip_cim = None

        for cim in self.adapterek.get(nev, []):
            if cim.family == socket.AF_INET:
                ip_cim = cim.address
                break

        if ip_cim is None:
            return None

        forgalom = self.forgalom.get(nev)

        return {
            "adapter": nev,
            "ip": ip_cim,
            "allapot": "Aktív",
            "sebesseg": stat.speed,
            "kuldott": forgalom.bytes_sent if forgalom else 0,
            "fogadott": forgalom.bytes_recv if forgalom else 0
        }
