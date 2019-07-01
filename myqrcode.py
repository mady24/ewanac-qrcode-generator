import pyqrcode
import png
import sys
import os
import json
from datetime import date
from firebase import firebase
from sys import exit


def menu():
    continuer = 'n'
    while continuer != 'o':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(">---------------------------generateur de qr code---------------------------<")
        print(">--------1: creer un nouveau qr code en mettant les info du site------------<")
        print('>------------------------2: creer un  nouveau QR code-----------------------<')
        print('>-------------------------3: afficher base de donnees-----------------------<')
        print('>----------------------------------o: quitter-------------------------------<')
        continuer = input()
        if continuer == '1':
            fill_qr()
        if continuer == '2':
            create_qr()
        if continuer == '3':
            getbase()

def create_qr():
    nonSite = ""
    village = ""
    typeOuvrage = ""
    sysLavMain = ""
    popMenage = ""
    longitude = ""
    latitude = ""
    commune = ""
    departement = ""
    region = ""
    dateMiseService = ""
    today = date.today()
    now = today.strftime("%d/%m/%Y")
    data = postbase(nonSite, village, typeOuvrage, sysLavMain, popMenage, longitude, latitude, commune, departement, region, dateMiseService, now)
    #array = [nonSite, longitude, latitude, commune, departement, region, dateMiseService, now]
    #data = '.'.join(array)
    generate_qr(data,nonSite)


def fill_qr():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Donner le nom du menage", end=' ')
    nonSite = input()
    print("Donner le nom du village", end=' ')
    village = input()
    print("Donner le type d'ouvrage", end=' ')
    typeOuvrage = input()
    print("Exist-il un systeme de lavage de main o/n", end=' ')
    sysLavMain = input()
    print("Donner le population du menage", end=' ')
    popMenage = input()
    print("donner la longitude dusite", end=' ')
    longitude = input()
    print("donner la latitude du site", end=' ')
    latitude = input()
    print("donner la commune ou communaute rural du site", end=' ')
    commune = input()
    print("donner le departement du site", end=' ')
    departement = input()
    print("donner la region du site", end=' ')
    region = input()
    print("donner la date de mise en service site", end=' ')
    dateMiseService = input()
    today = date.today()
    now = today.strftime("%d/%m/%Y")
    data = postbase(nonSite, village, typeOuvrage, sysLavMain, popMenage, longitude, latitude, commune, departement, region, dateMiseService, now)
    #array = [nonSite, longitude, latitude, commune, departement, region, dateMiseService, now]
    #data = '.'.join(array)
    generate_qr(data,nonSite)


def getbase():
  fire = firebase.FirebaseApplication('https://e-wanacc.firebaseio.com/', None)
  result = fire.get('/site', None)
  os.system('cls' if os.name == 'nt' else 'clear')
  print(result)
  os.system("pause")
  

def postbase(nonSite, village, typeOuvrage, sysLavMain, popMenage, longitude, latitude, commune, departement, region, dateMiseService, now):
   fire = firebase.FirebaseApplication('https://e-wanacc.firebaseio.com/', None)
   count = fire.get('/count/nbre', None)
   new_site = {"commune":commune,"dateservie":dateMiseService,"departement":departement,"etat":"excellent","lastdate":now,"lattitude":latitude,"longitude":longitude,"nomSite":nonSite,"region":region,"village":village,"typeOuvrage":typeOuvrage,"sysLavMain":sysLavMain,"popMenage":popMenage}
   count +=1
   results = fire.put('/count', 'nbre',count)
   result = fire.post('/site', new_site, params={'print': 'pretty'})
   data = json.dumps(result)
   data1 = json.loads(data)
   topass = [data1['name'],count]

   return topass

def generate_qr(data,nonSite):
   link_to_post = data[0]
   url=pyqrcode.create(link_to_post)
   #url.svg(sys.stdout, scale=1)
   url.png(f"{data[1]}.png", scale=8, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
   print("Printing QR code")
   print(url.terminal())


menu()

os._exit(-1)