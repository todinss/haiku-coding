import random
import tkinter as tk

def estrattore():
    f=open('HaikuUno.txt') 
    f2=open('HaikuDue.txt')
    f3=open('HaikuTre.txt')
    haiku1=random.choice(f.readlines())
    haiku2=random.choice(f2.readlines())
    haiku3=random.choice(f3.readlines())
    haiku_completo=[haiku1,haiku2,haiku3]
    haiku_testo=tk.Label(app, text=haiku_completo)
    haiku_testo.grid(row=2, column=0)

app=tk.Tk()
app.geometry("1000x750")
app.title("Generatore di Haiku")
bottone = tk.Button(text="Premere il bottone per generare l'Haiku", width=142, command = estrattore)
bottone.grid(row=1, column=0)
app.mainloop()
    
