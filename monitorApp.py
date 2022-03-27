from cProfile import run
from cgitb import text
import email
import smtplib
import ssl
import time
import requests
from tkinter import *
import threading

root = Tk()
root.title("Monitoreo de paginas web")
root.iconbitmap('C:/Users/messi/Documents/Curso programacion/Python/monitoreoWeb/MONITOR APP/eyeReduced.ico')

exit_event = threading.Event()

port = 465
context = ssl.create_default_context()
urls = []
lblCargaCorrecta = Label(root,text="")
lblCargaCorrecta.grid(row=5,column=3)

urlEntrada = Entry(root, width=35)
urlEntrada.grid(row=0,column=0)

cont = 0
botonesEstado = []
lblsURL = []
def agregarUrl():
    global cont
    lblCargaCorrecta["text"] = ""
    urls.append(urlEntrada.get())
    lblPagina = Label(root,text=urlEntrada.get())
    lblPagina.grid(row=cont,column=1)
    global lblsURL
    lblsURL.append(lblPagina)
    global btnEstado
    btnEstado = Button(root,width=5,state=DISABLED,bg="grey")
    botonesEstado.append(btnEstado)
    btnEstado.grid(row=(cont+1),column=1)
    cont = cont + 2
    lblEnMonitoreo.grid(row=(cont+1),column=1)

botonIngresar = Button(root, text="Ingresar URL", command=agregarUrl)
botonIngresar.grid(row=1,column=0)       

emailEntrada = Entry(root, width=35)
emailEntrada.grid(row=0,column=3)

def setEmailReceiver():
    global EMAIL_RECEIVER
    EMAIL_RECEIVER = emailEntrada.get()
    lblCargaCorrecta["text"] = "Email receptor cargado"

botonSetEmailReceiver = Button(root,text="Cargar receptor",command=setEmailReceiver)
botonSetEmailReceiver.grid(row=0,column=4)

smtpEntrada = Entry(root, width=20)
smtpEntrada.grid(row=1,column=3)

def setSmtpServer():
    global SMTP_SERVER
    SMTP_SERVER = smtpEntrada.get()
    lblCargaCorrecta["text"] = "SMTP cargado"

botonSetSmtpServer = Button(root,text="Cargar smtp",command=setSmtpServer)
botonSetSmtpServer.grid(row=1,column=4)

portEntrada = Entry(root, width=20)
portEntrada.grid(row=2,column=3)

def setSmtpPort():
    global port
    port = portEntrada.get()
    lblCargaCorrecta["text"] = "SMTP port cargado"

botonSetSmtpPort = Button(root,text="Cargar puerto smtp",command=setSmtpPort)
botonSetSmtpPort.grid(row=2,column=4)

emailSenderEntrada = Entry(root, width=35)
emailSenderEntrada.grid(row=3,column=3)

def setEmailSender():
    global EMAIL_ADDRESS
    EMAIL_ADDRESS = emailSenderEntrada.get()
    lblCargaCorrecta["text"] = "Email emisor cargado"

botonSetEmailSender = Button(root,text="Cargar emisor",command=setEmailSender)
botonSetEmailSender.grid(row=3,column=4)

passSenderEntrada = Entry(root, width=35)
passSenderEntrada.grid(row=4,column=3)

def setPassSender():
    global EMAIL_PASSWORD
    EMAIL_PASSWORD = passSenderEntrada.get()
    lblCargaCorrecta["text"] = "Password emisor cargado"

botonSetPassSender = Button(root,text="Cargar emisor pass",command=setPassSender)
botonSetPassSender.grid(row=4,column=4)

hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))
lblEnMonitoreo = Label(root, text="")

def comenzarMonitoreo():
    lblCargaCorrecta["text"] = ""
    lblEnMonitoreo["text"] = "MONITOREO EN CURSO..."
    botonMonitorear["state"] = DISABLED
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    hiloMonitoreo.start()

def detenerMonitoreo():
    lblEnMonitoreo.grid_forget()
    botonReanudarMonitoreo["state"] = NORMAL
    botonPararMonitoreo["state"] = DISABLED
    for boton in botonesEstado:
        boton["bg"] = "grey"
    exit_event.set()

def reanudarMonitoreo():
    lblEnMonitoreo.grid(row=(cont+1),column=1)
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    exit_event.clear()
    hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))
    hiloMonitoreo.start()

def enviarMail(url):
    with smtplib.SMTP_SSL(SMTP_SERVER,port,context=context) as server:
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        asunto='SITIO WEB CAIDO'
        cuerpo='El sitio web '+url+' se encuentra caido en este momento'
        msg = f'Subject:{asunto}\n\n{cuerpo}'
        server.sendmail(EMAIL_ADDRESS,EMAIL_RECEIVER,msg)

def monitorear(urls):
    while True:
        i = 0
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    enviarMail(url)
                    botonesEstado[i]["bg"] = "red"
                else:
                    botonesEstado[i]["bg"] = "green"
            except:
                enviarMail(url)
                botonesEstado[i]["bg"] = "red"
            i+=1
        time.sleep(60)

        if exit_event.is_set():
            break

botonMonitorear = Button(root, text="Comenzar monitoreo", command=comenzarMonitoreo)
botonMonitorear.grid(row=0,column=2)

botonPararMonitoreo = Button(root, text="Parar monitoreo", command=detenerMonitoreo, state=DISABLED)
botonPararMonitoreo.grid(row=1,column=2)

botonReanudarMonitoreo = Button(root, text="Reanudar monitoreo", command=reanudarMonitoreo, state=DISABLED)
botonReanudarMonitoreo.grid(row=2,column=2)

root.mainloop()