from cProfile import run
import smtplib
import ssl
import time
import requests
from tkinter import *
import threading

root = Tk()
root.title("Monitoreo de paginas web")

exit_event = threading.Event()

EMAIL_ADDRESS = 'fcropalati@gmail.com'
EMAIL_PASSWORD = 'vmqkixpieudeyfoa'
port = 465
context = ssl.create_default_context()
urls = []

urlEntrada = Entry(root, width=35)
urlEntrada.pack()

botonesEstado = []
def agregarUrl():
    urls.append(urlEntrada.get())
    lblPagina = Label(root,text=urlEntrada.get())
    lblPagina.pack()
    global btnEstado
    btnEstado = Button(root,width=5,state=DISABLED,bg="grey")
    botonesEstado.append(btnEstado)
    btnEstado.pack()

hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))

lblEnMonitoreo = Label(root, text="MONITOREO EN CURSO...")

def comenzarMonitoreo():
    botonMonitorear["state"] = DISABLED
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    lblEnMonitoreo.pack()
    hiloMonitoreo.start()

def detenerMonitoreo():
    lblEnMonitoreo.pack_forget()
    botonReanudarMonitoreo["state"] = NORMAL
    botonPararMonitoreo["state"] = DISABLED
    for boton in botonesEstado:
        boton["bg"] = "grey"
    exit_event.set()

def reanudarMonitoreo():
    lblEnMonitoreo.pack()
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    exit_event.clear()
    hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))
    hiloMonitoreo.start()

def monitorear(urls):
    while True:
        i = 0
        for url in urls:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
                    server.login("fcropalati@gmail.com",EMAIL_PASSWORD)
                    asunto='SITIO WEB CAIDO'
                    cuerpo='El sitio web '+url+' se encuentra caido en este momento'
                    msg = f'Subject:{asunto}\n\n{cuerpo}'
                    server.sendmail(EMAIL_ADDRESS,"fcropalati@gmail.com",msg)
                botonesEstado[i]["bg"] = "green"
            else:
                botonesEstado[i]["bg"] = "red"
            i+=1
        time.sleep(60)

        if exit_event.is_set():
            break

botonIngresar = Button(root, text="Ingresar URL", command=agregarUrl)
botonIngresar.pack()        

botonMonitorear = Button(root, text="Comenzar monitoreo", command=comenzarMonitoreo)
botonMonitorear.pack()

botonPararMonitoreo = Button(root, text="Parar monitoreo", command=detenerMonitoreo, state=DISABLED)
botonPararMonitoreo.pack()

botonReanudarMonitoreo = Button(root, text="Reanudar monitoreo", command=reanudarMonitoreo, state=DISABLED)
botonReanudarMonitoreo.pack()

root.mainloop()