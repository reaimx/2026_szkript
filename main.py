
from vzs_halozat import VZSHalozat, vzs_meret_formazas


def main():
    app = VZSHalozat()
    adapterek = app.aktiv_adapterek()

    print("HÁLÓZATFIGYELŐ")
    print("-" * 40)

    if not adapterek:
        print("Nem található aktív hálózati adapter.")
        return

    print("Elérhető hálózati adapterek:\n")

    for index, adapter in enumerate(adapterek, start=1):
        print(f"{index}. {adapter['nev']} - {adapter['ip']}")

    print()

    try:
        valasztas = int(input("Válassz adaptert (sorszám): "))
    except ValueError:
        print("Hibás választás.")
        return

    if not 1 <= valasztas <= len(adapterek):
        print("Érvénytelen sorszám.")
        return

    nev = adapterek[valasztas - 1]["nev"]
    adatok = app.adatok_lekerese(nev)

    if adatok is None:
        print("A kiválasztott adapter nem elérhető.")
        return

    print("\nHÁLÓZATI INFORMÁCIÓK")
    print("-" * 40)
    print(f"Adapter: {adatok['adapter']}")
    print(f"IP-cím: {adatok['ip']}")
    print(f"Állapot: {adatok['allapot']}")

    if adatok["sebesseg"] > 0:
        print(f"Kapcsolati sebesség: {adatok['sebesseg']} Mbps")
    else:
        print("Kapcsolati sebesség: Nem elérhető")

    print(f"Összes küldött adat: {vzs_meret_formazas(adatok['kuldott'])}")
    print(f"Összes fogadott adat: {vzs_meret_formazas(adatok['fogadott'])}")


if __name__ == "__main__":
    main()
