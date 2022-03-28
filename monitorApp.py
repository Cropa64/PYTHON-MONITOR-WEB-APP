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
mailEnviadoArray = []
botonesEstado = []
def agregarUrl():
    global cont
    lblCargaCorrecta["text"] = ""
    urls.append(urlEntrada.get())
    mailEnviadoArray.append(False)
    lblPagina = Label(root,text=urlEntrada.get())
    lblPagina.grid(row=cont,column=1)
    global btnEstado
    btnEstado = Button(root,width=5,state=DISABLED,bg="grey")
    botonesEstado.append(btnEstado)
    btnEstado.grid(row=(cont+1),column=1)
    cont = cont + 2

botonIngresar = Button(root, text="Ingresar URL", command=agregarUrl)
botonIngresar.grid(row=1,column=0)       

emailEntrada = Entry(root, width=35)
emailEntrada.grid(row=0,column=3)

EMAIL_RECEIVER = []
def setEmailReceiver():
    global EMAIL_RECEIVER
    EMAIL_RECEIVER.append(emailEntrada.get()) 
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

lblEnMonitoreo = Label(root, text="MONITOREO EN CURSO...")

hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))
def comenzarMonitoreo():
    lblCargaCorrecta["text"] = ""
    botonIngresar["state"] = DISABLED
    lblEnMonitoreo.grid(row=(cont+1),column=1)
    botonMonitorear["state"] = DISABLED
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    hiloMonitoreo.start()

def detenerMonitoreo():
    lblEnMonitoreo.grid_forget()
    botonIngresar["state"] = NORMAL
    botonPararMonitoreo["state"] = DISABLED
    exit_event.set()
    for boton in botonesEstado:
        boton["bg"] = "grey"
    for i in range(0,len(mailEnviadoArray)):
        mailEnviadoArray[i] = False

def reanudarMonitoreo():
    lblEnMonitoreo.grid(row=(cont+1),column=1)
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    botonIngresar["state"] = DISABLED
    global hiloMonitoreo
    hiloMonitoreo = threading.Thread(target=lambda: monitorear(urls))
    hiloMonitoreo.start()
    exit_event.clear()

botonMonitorear = Button(root, text="Comenzar monitoreo", command=comenzarMonitoreo)
botonMonitorear.grid(row=0,column=2)

botonPararMonitoreo = Button(root, text="Parar monitoreo", command=detenerMonitoreo, state=DISABLED)
botonPararMonitoreo.grid(row=1,column=2)

botonReanudarMonitoreo = Button(root, text="Reanudar monitoreo", command=reanudarMonitoreo, state=DISABLED)
botonReanudarMonitoreo.grid(row=2,column=2)

def enviarMail(url,i):
    server = smtplib.SMTP_SSL(SMTP_SERVER,port,context=context)
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    asunto='SITIO WEB CAIDO'
    cuerpo='El sitio web '+url+' se encuentra caido en este momento'
    msg = f'Subject:{asunto}\n\n{cuerpo}'
    if mailEnviadoArray[i] == False:
        for email in EMAIL_RECEIVER:
            server.sendmail(EMAIL_ADDRESS,email,msg)
        mailEnviadoArray[i] = True
    server.close()

def monitorear(urls):
    while True:
        print("hilo")
        i = 0
        for url in urls:
            try:
                botonPararMonitoreo["state"] = DISABLED
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    print("bad")
                    botonesEstado[i]["bg"] = "red"
                    enviarMail(url,i)
                else:
                    print("ok")
                    botonesEstado[i]["bg"] = "green"
                    mailEnviadoArray[i] = False
            except:
                print("except")
                botonesEstado[i]["bg"] = "red"
                enviarMail(url,i)
            i+=1
        botonPararMonitoreo["state"] = NORMAL
        time.sleep(10)
        if exit_event.is_set():
            botonReanudarMonitoreo["state"] = NORMAL
            break
    
root.mainloop()