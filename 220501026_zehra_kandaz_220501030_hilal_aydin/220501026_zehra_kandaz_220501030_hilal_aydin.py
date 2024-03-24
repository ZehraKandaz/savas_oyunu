from tkinter import *

# Savasci Sinifi
class Savasci:
    def __init__(self, kaynak, can, menzil_yatay, menzil_dikey, menzil_capraz):
        self.kaynak = kaynak
        self.can = can
        self.menzil_yatay = menzil_yatay
        self.menzil_dikey = menzil_dikey
        self.menzil_capraz = menzil_capraz

# Muhafiz Sinifi
class Muhafiz(Savasci):
    def __init__(self):
        super().__init__(kaynak=10, can=80, menzil_dikey=1, menzil_yatay=1, menzil_capraz=1)

    def hasar_ver(self, dusman):
        if abs(dusman.menzil_dikey - self.menzil_dikey) <= self.menzil_dikey \
                and abs(dusman.menzil_yatay - self.menzil_yatay) <= self.menzil_yatay \
                and abs(dusman.menzil_capraz - self.menzil_capraz) <= self.menzil_capraz:
            dusman.can -= 20

# Okcu Sinifi
class Okcu(Savasci):
    def __init__(self):
        super().__init__(kaynak=20, can=30, menzil_yatay=2, menzil_dikey=2, menzil_capraz=2)

    def hasar_ver(self, dusman):
        if abs(dusman.menzil_dikey - self.menzil_dikey) <= self.menzil_dikey \
                and abs(dusman.menzil_yatay - self.menzil_yatay) <= self.menzil_yatay \
                and abs(dusman.menzil_capraz - self.menzil_capraz) <= self.menzil_capraz:
            dusman.can -= dusman.can * 0.6

# Topcu Sinifi
class Topcu(Savasci):
    def __init__(self):
        super().__init__(kaynak=50, can=30, menzil_dikey=2, menzil_yatay=2, menzil_capraz=0)

    def hasar_ver(self, dusman):
        if abs(dusman.menzil_dikey - self.menzil_dikey) <= self.menzil_dikey \
                    and abs(dusman.menzil_yatay - self.menzil_yatay) <= self.menzil_yatay \
                    and abs(dusman.menzil_capraz - self.menzil_capraz) <= self.menzil_capraz:
            dusman.can = 0

# Atli Sinifi
class Atli(Savasci):
    def __init__(self):
        super().__init__(kaynak=30, can=40, menzil_yatay=0, menzil_dikey=0, menzil_capraz=3)

    def hasar_ver(self, dusman):
        if abs(dusman.menzil_dikey - self.menzil_dikey) <= self.menzil_dikey \
                and abs(dusman.menzil_yatay - self.menzil_yatay) <= self.menzil_yatay \
                and abs(dusman.menzil_capraz - self.menzil_capraz) <= self.menzil_capraz:
            dusman.can -= 30

# Saglikci Sinifi
class Saglikci(Savasci):
    def __init__(self):
        super().__init__(kaynak=10, can=100, menzil_yatay=2, menzil_dikey=2, menzil_capraz=2)

    def iyilestir(self, dostlar):
        for dost in dostlar:
            if abs(dost.menzil_dikey - self.menzil_dikey) <= self.menzil_dikey \
                    and abs(dost.menzil_yatay - self.menzil_yatay) <= self.menzil_yatay \
                    and abs(dost.menzil_capraz - self.menzil_capraz) <= self.menzil_capraz:
                dost.can += dost.can * 0.5

class Hazine:
    def __init__(self, kaynak):
        self.kaynak = kaynak

class Tahta:
    def __init__(self, boyut):
        self.boyut = boyut
        self.tahta_window = None
        self.suanki_savasci = None
        self.siradaki_oyuncu = 1
        self.oyuncu_renkleri = ["pink", "lightblue", "lightgreen", "#ffff80"]
        self.hazineler = [Hazine(200) for _ in range(4)]
        self.savasci_sayisi = {1: 0, 2: 0, 3: 0, 4: 0}
        self.max_savasci_sayisi = 2

    def tahta_ciz(self):
        self.tahta_window = Tk()
        self.tahta_window.title("Lords Of The Polywarphism")
        for satir in range(self.boyut):
            for sutun in range(self.boyut):
                renk = "#f2f2f2" if (satir + sutun) % 2 == 0 else "#d9d9d9"
                label = Label(self.tahta_window, bg=renk, width=5, height=2)
                label.grid(row=satir, column=sutun)
                label.bind("<Button-1>", lambda event, row=satir, column=sutun: self.yerlestir(event, row, column))

        # Köselere muhafiz yerlestirme
        muhafizlar = [(0, 0), (0, self.boyut - 1), (self.boyut - 1, 0), (self.boyut - 1, self.boyut - 1)]
        for oyuncu, pozisyon in enumerate(muhafizlar, start=1):
            muhafiz = Muhafiz()
            self.savasci_sayisi[oyuncu] += 1
            label = Label(self.tahta_window, text=f"{muhafiz.__class__.__name__}\nCan: {muhafiz.can}",
                          bg=self.oyuncu_renkleri[oyuncu - 1], width=5, height=2)
            label.grid(row=pozisyon[0], column=pozisyon[1])

        self.siradaki_oyuncu_label = Label(self.tahta_window, text=f"Siradaki Oyuncu: Oyuncu {self.siradaki_oyuncu}",
                                           font=("Arial", 12))
        self.siradaki_oyuncu_label.grid(row=self.boyut, column=0, columnspan=self.boyut, pady=5)
        self.hazine_label = Label(self.tahta_window,
                                  text=f"Oyuncu {self.siradaki_oyuncu} Hazinesi: {self.hazineler[self.siradaki_oyuncu - 1].kaynak} Kaynak",
                                  font=("Arial", 12))
        self.hazine_label.grid(row=self.boyut + 1, column=0, columnspan=self.boyut, pady=5)
        pas_gec_button = Button(self.tahta_window, text="Pas Gec", command=self.pas_gec)
        pas_gec_button.grid(row=self.boyut + 2, column=0, columnspan=self.boyut, pady=5)

        muhafizlar = [(0, 0), (0, self.boyut - 1), (self.boyut - 1, 0), (self.boyut - 1, self.boyut - 1)]
        for oyuncu, pozisyon in enumerate(muhafizlar, start=1):
            label = Label(self.tahta_window, text="Muhafiz", bg=self.oyuncu_renkleri[oyuncu - 1], width=5, height=2)
            label.grid(row=pozisyon[0], column=pozisyon[1])
            label.bind("<Button-1>", lambda event, savasci=Muhafiz: savasci_bilgileri_goster(savasci()))

            # Savascilarin cevresindeki kareleri boyama islemi
            for i in range(max(pozisyon[0] - 1, 0), min(pozisyon[0] + 2, self.boyut)):
                for j in range(max(pozisyon[1] - 1, 0), min(pozisyon[1] + 2, self.boyut)):
                    if not (i == pozisyon[0] and j == pozisyon[1]):
                        surrounding_label = self.tahta_window.grid_slaves(row=i, column=j)[0]
                        surrounding_label.configure(bg=self.oyuncu_renkleri[oyuncu - 1])

        self.gec_button = Button(self.tahta_window, text="Gec", command=self.gec)
        self.gec_button.grid(row=self.boyut + 3, column=0, columnspan=self.boyut, pady=5)

        self.tahta_window.mainloop()

    def yerlestir(self, event, row, column):
        oyuncu = self.siradaki_oyuncu
        if self.savasci_sayisi[oyuncu] < self.max_savasci_sayisi:
            if self.suanki_savasci:
                # Secilen karenin etrafindaki kareleri kontrol et
                surrounding = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
                oyuncu_rengi = self.oyuncu_renkleri[self.siradaki_oyuncu - 1]

                # Secilen karenin rengini kontrol et
                selected_label = self.tahta_window.grid_slaves(row=row, column=column)[0]
                selected_color = selected_label.cget('bg')

                # Secilen karenin rengi mevcut oyuncunun rengine esitse devam et
                if selected_color == oyuncu_rengi:
                    # Eger secilen kare uygunsa savasciyi yerlestir
                    label = Label(self.tahta_window, text=self.suanki_savasci.__class__.__name__,
                                  bg=oyuncu_rengi, width=5, height=2)
                    label.grid(row=row, column=column)

                    # Savasci etiketine tiklama olayini bagla
                    label.bind("<Button-1>",
                               lambda event, savasci=self.suanki_savasci: savasci_bilgileri_goster(savasci))

                    # Cevredeki uygun kareleri boyama islemi
                    for r, c in surrounding:
                        if 0 <= r < self.boyut and 0 <= c < self.boyut:
                            surrounding_label = self.tahta_window.grid_slaves(row=r, column=c)[0]
                            surrounding_label.configure(bg=oyuncu_rengi)

                    # Capraz kareleri boyama islemi
                    cross_labels = [(row - 1, column - 1), (row - 1, column + 1), (row + 1, column - 1),
                                    (row + 1, column + 1)]
                    for r, c in cross_labels:
                        if 0 <= r < self.boyut and 0 <= c < self.boyut:
                            cross_label = self.tahta_window.grid_slaves(row=r, column=c)[0]
                            cross_label.configure(bg=oyuncu_rengi)

                    # Diger islemleri gerceklestir
                    print(f"{self.suanki_savasci.__class__.__name__} {row}-{column} konumuna yerleştirildi.")
                    self.hazineler[self.siradaki_oyuncu - 1].kaynak -= self.suanki_savasci.kaynak
                    self.hazine_label.config(
                        text=f"Oyuncu {self.siradaki_oyuncu} Hazinesi: {self.hazineler[self.siradaki_oyuncu - 1].kaynak} Kaynak")
                    self.suanki_savasci = None
                    self.savasci_sayisi[oyuncu] += 1
                    if self.savasci_sayisi[oyuncu] >= self.max_savasci_sayisi:
                        self.gec_button.config(state="normal")
                else:
                    print("Savasciyi koyabilmek icin kendi rengine boyali bir kare secmelisiniz.")
            else:
                print("Lütfen bir savasci secin.")
        else:
            print("Bu oyuncu daha fazla savasci yerlestiremez.")

    def savasci_sec(self, savasci):
        self.suanki_savasci = savasci()

    def pas_gec(self):
        self.gec_button.config(state="normal")
        self.siradaki_oyuncu = (self.siradaki_oyuncu % 4) + 1
        self.siradaki_oyuncu_label.config(text=f"Siradaki Oyuncu: Oyuncu {self.siradaki_oyuncu}")
        self.hazine_label.config(
            text=f"Oyuncu {self.siradaki_oyuncu} Hazinesi: {self.hazineler[self.siradaki_oyuncu - 1].kaynak} Kaynak")
        self.savasci_sayisi = {1: 0, 2: 0, 3: 0, 4: 0}

    def gec(self):
        self.gec_button.config(state="normal")
        self.siradaki_oyuncu = (self.siradaki_oyuncu % 4) + 1
        self.siradaki_oyuncu_label.config(text=f"Siradaki Oyuncu: Oyuncu {self.siradaki_oyuncu}")
        self.hazine_label.config(
            text=f"Oyuncu {self.siradaki_oyuncu} Hazinesi: {self.hazineler[self.siradaki_oyuncu - 1].kaynak} Kaynak")
        self.savasci_sayisi = {1: 0, 2: 0, 3: 0, 4: 0}

def savasci_bilgileri_goster(savasci):
    bilgi_penceresi = Tk()
    bilgi_penceresi.title("Savasci Bilgileri")
    bilgi_penceresi.geometry("300x200")

    # Savasci türüne göre özelliklerini, adlarini ve degerlerini bir listede sakla.
    if isinstance(savasci, Muhafiz):
        bilgiler = [("Tür:", "Muhafiz"), ("Kaynak:", savasci.kaynak), ("Can:", savasci.can),
                     ("Menzil Yatay:", savasci.menzil_yatay), ("Menzil Dikey:", savasci.menzil_dikey),
                     ("Menzil Çapraz:", savasci.menzil_capraz)]
    elif isinstance(savasci, Okcu):
        bilgiler = [("Tür:", "Okcu"), ("Kaynak:", savasci.kaynak), ("Can:", savasci.can),
                     ("Menzil Yatay:", savasci.menzil_yatay), ("Menzil Dikey:", savasci.menzil_dikey),
                     ("Menzil Çapraz:", savasci.menzil_capraz)]
    elif isinstance(savasci, Topcu):
        bilgiler = [("Tür:", "Topçu"), ("Kaynak:", savasci.kaynak), ("Can:", savasci.can),
                     ("Menzil Yatay:", savasci.menzil_yatay), ("Menzil Dikey:", savasci.menzil_dikey),
                     ("Menzil Çapraz:", savasci.menzil_capraz)]
    elif isinstance(savasci, Atli):
        bilgiler = [("Tür:", "Atli"), ("Kaynak:", savasci.kaynak), ("Can:", savasci.can),
                     ("Menzil Yatay:", savasci.menzil_yatay), ("Menzil Dikey:", savasci.menzil_dikey),
                     ("Menzil Çapraz:", savasci.menzil_capraz)]
    elif isinstance(savasci, Saglikci):
        bilgiler = [("Tür:", "Saglikci"), ("Kaynak:", savasci.kaynak), ("Can:", savasci.can),
                     ("Menzil Yatay:", savasci.menzil_yatay), ("Menzil Dikey:", savasci.menzil_dikey),
                     ("Menzil Çapraz:", savasci.menzil_capraz)]
    else:
        bilgiler = []

    # Özelliklerin etiketlerini ve degerlerini pencereye ekle.
    for i, (etiket, deger) in enumerate(bilgiler):
        label = Label(bilgi_penceresi, text=f"{etiket}: {deger}", font=("Arial", 12))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    bilgi_penceresi.mainloop()

def secim_ekrani_goster():
    secim_window = Tk()
    secim_window.title("Savasci Secim Ekrani")
    secim_window.config(background="#B0C4DE")
    secim_window.geometry("400x400")

    def savasci_sec(savasci):
        tahta.savasci_sec(savasci)
        secim_window.destroy()

    muhafiz_button = Button(secim_window, text="Muhafiz", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=lambda: savasci_sec(Muhafiz))
    muhafiz_button.pack(pady=10)

    okcu_button = Button(secim_window, text="Okçu", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=lambda: savasci_sec(Okcu))
    okcu_button.pack(pady=10)

    topcu_button = Button(secim_window, text="Topçu", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=lambda: savasci_sec(Topcu))
    topcu_button.pack(pady=10)

    atli_button = Button(secim_window, text="Atli", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=lambda: savasci_sec(Atli))
    atli_button.pack(pady=10)

    saglikci_button = Button(secim_window, text="Saglikci", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=lambda: savasci_sec(Saglikci))
    saglikci_button.pack(pady=10)

    secim_window.mainloop()

window = Tk()
window.title("Menu")
window.config(background="#B0C4DE")
window.geometry("400x400")

boyut_label = Label(window, text="Dünya boyutunu giriniz: ", font=("Arial", 20), bg="#B0C4DE", pady=4)
boyut_label.place(x=50, y=50)

boyut_entry = Entry(window, width=20, font=("Arial", 20))
boyut_entry.place(x=50, y=100)

def tahta_olustur():
    boyut = int(boyut_entry.get())
    global tahta
    if(8<=boyut<=32):
        tahta = Tahta(boyut)
        tahta.tahta_ciz()
    else:
        print("Gecerli bir tahta boyutu giriniz.")

boyut_olustur_button = Button(window, text="Olustur", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=tahta_olustur)
boyut_olustur_button.place(x=120, y=150)

secim_button = Button(window, text="Savasci Sec", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=secim_ekrani_goster)
secim_button.place(x=120, y=200)

cikis_button = Button(window, text="Cikis", background="#5794f7", activebackground="#5794f7", width=20, height=2, command=quit)
cikis_button.place(x=120, y=250)

window.mainloop()