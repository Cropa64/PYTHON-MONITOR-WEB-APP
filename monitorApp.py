from asyncio.windows_events import NULL
import smtplib
import ssl
import time
import requests
from tkinter import *
import threading
import logging

root = Tk()
root.title("Monitoreo de paginas web")
root.iconbitmap('eyeReduced.ico')
exit_event = threading.Event()
context = ssl.create_default_context()

logging.basicConfig(filename='monitor.log',level=logging.WARNING,format='%(asctime)s:%(levelname)s:%(message)s')

lblCargaCorrecta = Label(root,text="")
lblCargaCorrecta.grid(row=5,column=3)

urlEntrada = Entry(root, width=35)
urlEntrada.insert(END,"https://")
urlEntrada.grid(row=0,column=0)

cont = 0
mailEnviadoArray = []
botonesEstado = []
lblsURL = []
urls = []
def agregarUrl():
    global cont
    lblCargaCorrecta["text"] = ""
    urls.append(urlEntrada.get())
    mailEnviadoArray.append(False)
    lblPagina = Label(root,text=urlEntrada.get())
    lblPagina.grid(row=cont,column=1)
    lblsURL.append(lblPagina)
    global btnEstado
    btnEstado = Button(root,width=5,disabledforeground="black",bg="grey",state=DISABLED)
    botonesEstado.append(btnEstado)
    btnEstado.grid(row=(cont+1),column=1)
    cont = cont + 2

botonIngresar = Button(root, text="Ingresar URL", command=agregarUrl)
botonIngresar.grid(row=1,column=0)

def limpiarURLs():
    for i in range(0,len(urls)):
        lblsURL[i].destroy()
        botonesEstado[i].destroy()
    urls.clear()
    mailEnviadoArray.clear()
    lblsURL.clear()
    botonesEstado.clear()
    global cont
    cont = 0

botonLimpiarURL = Button(root, text="Limpiar URLs", command=limpiarURLs)
botonLimpiarURL.grid(row=2,column=0)

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

EMAIL_ADDRESS = ""
def setEmailSender():
    global EMAIL_ADDRESS
    EMAIL_ADDRESS = emailSenderEntrada.get()
    lblCargaCorrecta["text"] = "Email emisor cargado"

botonSetEmailSender = Button(root,text="Cargar emisor",command=setEmailSender)
botonSetEmailSender.grid(row=3,column=4)

passSenderEntrada = Entry(root, width=35)
passSenderEntrada.grid(row=4,column=3)

EMAIL_PASSWORD = ""
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
    botonLimpiarURL["state"] = DISABLED
    hiloMonitoreo.start()

def detenerMonitoreo():
    logging.info("Monitoreo detenido")
    lblEnMonitoreo.grid_forget()
    botonIngresar["state"] = NORMAL
    botonPararMonitoreo["state"] = DISABLED
    botonLimpiarURL["state"] = NORMAL
    exit_event.set()
    for boton in botonesEstado:
        boton["bg"] = "grey"
        boton["text"] = ""
    for i in range(0,len(mailEnviadoArray)):
        mailEnviadoArray[i] = False

def reanudarMonitoreo():
    lblEnMonitoreo.grid(row=(cont+1),column=1)
    lblCargaCorrecta["text"] = ""
    botonReanudarMonitoreo["state"] = DISABLED
    botonPararMonitoreo["state"] = NORMAL
    botonIngresar["state"] = DISABLED
    botonLimpiarURL["state"] = DISABLED
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
    if EMAIL_ADDRESS != "" and EMAIL_PASSWORD != "" and EMAIL_RECEIVER and SMTP_SERVER != "" and port:
        server = smtplib.SMTP_SSL(SMTP_SERVER,port,context=context)
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        asunto='SITIO WEB CAIDO'
        cuerpo='El sitio web '+url+' se encuentra caido en este momento'
        msg = f'Subject:{asunto}\n\n{cuerpo}'
        if mailEnviadoArray[i] == False:
            for email in EMAIL_RECEIVER:
                server.sendmail(EMAIL_ADDRESS,email,msg)
                logging.info('Mail enviado a {}'.format(email))
            mailEnviadoArray[i] = True
        server.close()

def monitorear(urls):
    while True:
        logging.info('pooleando...')
        for botonEstado in botonesEstado:
            botonEstado["text"] = ""
        i = 0
        for url in urls:
            try:
                botonPararMonitoreo["state"] = DISABLED
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    logging.warning('{} : {}'.format(url,r.status_code))
                    botonesEstado[i]["bg"] = "red"
                    botonesEstado[i]["text"] = r.status_code
                    enviarMail(url,i)
                else:
                    logging.info('{} : {}'.format(url,r.status_code))
                    botonesEstado[i]["bg"] = "green"
                    mailEnviadoArray[i] = False
                botonesEstado[i]["fg"] = "red"
                botonesEstado[i]["text"] = r.status_code
            except:
                logging.warning('{}'.format(url))
                botonesEstado[i]["bg"] = "red"
                botonesEstado[i]["text"] = "ERROR"
                enviarMail(url,i)
            i+=1
        botonPararMonitoreo["state"] = NORMAL
        time.sleep(10)
        if exit_event.is_set():
            botonReanudarMonitoreo["state"] = NORMAL
            break
    
root.mainloop()