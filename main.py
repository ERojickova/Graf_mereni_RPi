from tkinter import *
import random

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading
import datetime

cas_start = -1
vypocet_bezi = False

def app():

    delka_kroku = 1 #s


    def readTemp():
        return datetime.datetime.now(), random.random()*10+10

    def mojeVypocty(temp, k):
        return 0.95*k + 0.05*temp

    def plotter():
        global cas_start

        #nacti data
        been = False
        nejaky_koef = 15 # init
        df = pd.DataFrame(columns=['teplota', 'koef'])
        # df.index = pd.to_datetime(df.index)


        while vypocet_bezi:
            pockej_do_casu = datetime.datetime.now()+datetime.timedelta(seconds=delka_kroku)
            cas_full, teplota = readTemp()
            nejaky_koef = mojeVypocty(teplota, nejaky_koef)


            if been:
                cas_diff = cas_full - cas_start
                cas_diff = cas_diff.total_seconds()
            else:
                #prvni - nakreslim jen bod, zadnou caru
                cas_diff = 0
                cas_old_diff = 0
                teplota_old = teplota
                nejaky_koef_old = nejaky_koef
                been = True
                xx_prev = 0

            ax1.plot([cas_old_diff, cas_diff], [teplota_old, teplota], marker='o', color='orange', lw=1)
            ax2.plot([cas_old_diff, cas_diff], [nejaky_koef_old, nejaky_koef], marker='x', color='forestgreen', lw=1)

            # pro pristi kresleni
            cas_old_diff = cas_diff
            teplota_old = teplota
            nejaky_koef_old = nejaky_koef

            graph.draw()

            stitek.config(text=f'muj koeficient={round(nejaky_koef,2)}C')
            xx = (datetime.datetime.now() - cas_start)
            xx = xx.total_seconds()
            print (xx-xx_prev)
            xx_prev = xx

            while datetime.datetime.now() < pockej_do_casu:
                time.sleep(0.001)
            #time.sleep(delka_kroku)

    def zaciname():

        # spust vlakno, ktere meri teploty a kresli
        global cas_start
        global vypocet_bezi

        if vypocet_bezi:
            vypocet_bezi = False
            tlacitko.config(text='start')

        else:
            cas_start = datetime.datetime.now() #skutecny cas, kdy zacinam kreslit
            tlacitko.config(text = 'stop')
            vypocet_bezi = True
            ax1.cla()
            ax2.cla()

            ax1.set_xlabel("cas (s)")
            ax1.set_ylabel("teplota")
            ax1.grid()

            ax2.set_xlabel("cas (s)")
            ax2.set_ylabel("koef")
            ax2.grid()

            threading.Thread(target=plotter).start()


        return

    # vytvor okno
    root = Tk()
    root.config(background='white')
    root.geometry("1000x700")

    lab = Label(root, text="slozite vypocty", bg='white').pack()

    fig = Figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_xlabel("cas (s)")
    ax1.set_ylabel("teplota")
    ax1.grid()

    ax2.set_xlabel("cas (s)")
    ax2.set_ylabel("koef")
    ax2.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    # textove okno
    stitek=Label(root, text=u"xxx", font="Arial 12")
    stitek.pack(padx=20, pady=10)

    # tlacitko
    tlacitko = Button(root, text ="start", command = zaciname)
    tlacitko.pack(side="right", padx=20, pady=10)


    root.mainloop()


app()



