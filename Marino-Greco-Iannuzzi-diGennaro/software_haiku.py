#software realizzato da Mariano e di Gennaro, interfacci realizzata da Greco ed Iannuzzi.
from csv import reader
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import Menu
from tkinter.filedialog import asksaveasfile, test
import sys
sys.stdout.reconfigure(encoding='utf-8')

window = tk.Tk()
window.geometry("770x500")
window.title("Generatore di haiku")
window.resizable(False, False)
Barra_del_menu= Menu(window)
menu_1= Menu(Barra_del_menu)
Barra_del_menu.add_cascade(label="Menu", menu=menu_1, font=24)
window.config(menu=Barra_del_menu)
text_1="Benvenuto nel generatore casuale di Hauku. Premi il bottone e genera il tuo Haiku"
text_box = tk.Label(window, text=text_1, fg="red", font=("Times New Roman", 17) )
text_box.grid(row=0)
def copia():
    files = [('File di testo', '*.txt'),
             ('Pdf', '*.pdf')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
def creatori():
    messagebox.showinfo('Creatori' , 'I creatori del programma sono: Mariano, Greco, Iannuzzi, di Gennaro')
menu_1.add_command(label="Creatori", command=creatori)
menu_1.add_command(label="Copia", command=copia)
menu_1.add_command(label="Chiudi", command=exit)

# Estrattore casuale
def estrazione(lista):
    p=random.randint(0,len(lista)-1) 
    x=lista[p] 
    lista.remove(x) 
    return x

 #Estrazione casuale del csv
lista_csv = ['versi.csv']
a = estrazione(lista_csv)

#Apertura e lettura del file csv
with open( a , 'r' , encoding="utf-8") as csv_file:
    csv_reader = reader(csv_file)
    list_of_column = list(csv_reader)
nuova_lista_1 = []
nuova_lista_2 = []
nuova_lista_3 = []
for i in list_of_column: 
    nuova_lista_1.append(i[0])
    nuova_lista_2.append(i[1])
    nuova_lista_3.append(i[2])

def estrattore_completo_haiku():
    x=estrazione(nuova_lista_1)
    y=estrazione(nuova_lista_2)
    z=estrazione(nuova_lista_3)
    text_box_1= tk.Label(window, text=x, fg="blue", font=("Times New Roman", 20) )
    text_box_1.grid(row=3, column=0)
    text_box_2= tk.Label(window, text=y, fg="blue", font=("Times New Roman", 20) )
    text_box_2.grid(row=4, column=0)
    text_box_3= tk.Label(window, text=z, fg="blue", font=("Times New Roman", 20) )
    text_box_3.grid(row=5, column=0)

first_button = tk.Button(text="PREMI IL BOTTONE", command = estrattore_completo_haiku, font=20, width=20)
first_button.grid(row=2, column=0)

def estrattore_verso_1():
    x=estrazione(nuova_lista_1)
    text_box_1= tk.Label(window, text=x, fg="blue", font=("Times New Roman", 20) )
    text_box_1.grid(row=3, column=0)

cambia_verso_1 = tk.Button (text= 'Cambia il 1° verso', command = estrattore_verso_1, font=20)
cambia_verso_1.grid(row=6, column=0)

def estrattore_verso_2():
    y=estrazione(nuova_lista_2)
    text_box_2= tk.Label(window, text=y, fg="blue", font=("Times New Roman", 20) )
    text_box_2.grid(row=4, column=0)

cambia_verso_2 = tk.Button (text= 'Cambia il 2° verso', command = estrattore_verso_2, font=20)
cambia_verso_2.grid(row=7, column=0)

def estrattore_verso_3():
    z=estrazione(nuova_lista_3)
    text_box_3= tk.Label(window, text=z, fg="blue", font=("Times New Roman", 20) )
    text_box_3.grid(row=5, column=0)

cambia_verso_3 = tk.Button (text= 'Cambia il 3° verso', command = estrattore_verso_3, font=20)
cambia_verso_3.grid(row=8, column=0)



window.mainloop()