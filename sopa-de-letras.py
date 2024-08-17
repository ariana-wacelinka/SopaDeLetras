import tkinter as tk
from tkinter import messagebox
import random
import string

class InterfazPrincipal:
    def __init__(self): 
        self.root = tk.Tk()
        self.root.configure(bg='#2e2e2e')
        self.palabra = []
        self.root.title("Sopa de Letras")
        self.CrearInterfaz()

    def CrearInterfaz(self):
        tk.Label(self.root, text="Ingrese palabras con longitud maxima de 10 caracteres, separadas por comas:", bg='#2e2e2e',fg='#FFFFFF', font=('Sans Serif', 16)).pack()
        self.inputPalabras = tk.Entry(self.root, bg="#b8c0ff", width=50, font=('Sans Serif', 16))
        self.inputPalabras.pack(padx=20, pady=15)
        tk.Button(self.root, bg="#b8c0ff", font=('Sans Serif', 12), text="Iniciar Sopa de Letras", command=self.iniciarSopa).pack()

    def validarInput(self, inputAvalidar):
        palabras = inputAvalidar.split(',')
        for palabra in palabras:
            palabra = palabra.strip()
            if len(palabra) > 10 or len(palabra) == 0:
                return False
            if ' ' in palabra:
                return False
            if any(caracter.isdigit() for caracter in palabra):
                return False
        return True

    def iniciarSopa(self):
        inputAvalidar = self.inputPalabras.get()
        if self.validarInput(inputAvalidar):
            palabras = [palabra.upper().strip() for palabra in inputAvalidar.split(',')]
            self.root.destroy()
            InterfazSopaDeLetras(palabras)
        else:
            messagebox.showerror("Input incorrecto", "Las palabras deben\n-Tener entre 1 y 10 caracteres\n-No contener números\n-No contener espacios.")

class InterfazSopaDeLetras:
    def __init__(self, palabras):
        self.ventana = tk.Tk()
        self.ventana.configure(bg='#2e2e2e')
        self.ventana.title("Sopa de Letras")
        self.palabras = palabras
        self.crearInterfaz()
        self.SopaLetras = SopaDeLetras(self.ColumnaSopa, 15, 15, self.palabras)
        self.ListarPalabras()
        self.ventana.mainloop()

    def crearInterfaz(self):
        self.ColumnaSopa = tk.Frame(self.ventana, width=int(0.8 * self.ventana.winfo_screenwidth()), bg='#2e2e2e')
        self.ColumnaSopa.grid(row=0, column=0, padx=10, pady=10)
        
        self.ColumnaPalabras = tk.Frame(self.ventana, width=int(0.2 * self.ventana.winfo_screenwidth()), bg='#2e2e2e')
        self.ColumnaPalabras.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


    def ListarPalabras(self):
        for palabra in self.palabras:
            tk.Label(self.ColumnaPalabras, text=palabra, bg='#2e2e2e',fg='#FFFFFF', font=('Sans Serif', 16)).pack(pady=5)

class SopaDeLetras:
    def __init__(self, interfaz, filas, columnas, palabras):
        self.interfaz = interfaz
        self.filas = filas
        self.columnas = columnas
        self.palabras = sorted([palabra for palabra in palabras], key=self.tamanio, reverse=True)
        self.palabrasParaInsertar = []
        self.casillas = []
        self.crearGrid()
        self.insertarPalabras()
        self.letrasRandom()

    def crearGrid(self):
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                button = tk.Button(self.interfaz, text='', width=2, height=1, font=('Sans Serif', 16), bg="#b8c0ff")
                button.grid(row=i, column=j)
                button.bind("<Button-1>", self.seleccionarLetras)
                fila.append(button)
            self.casillas.append(fila)

    def insertarPalabras(self):
        for palabra in self.palabras:
            if self.colocar_palabra(palabra):
                self.palabrasParaInsertar.append(palabra)

    def colocar_palabra(self, palabra):
        intentos = 0
        while intentos < 225:
            direccion = random.choice(['horizontal', 'vertical'])
            derecho = random.choice([True, False])
            if direccion == 'horizontal' and self.insertarPalabraHorizontal(palabra, derecho):
                return True
            elif direccion == 'vertical' and self.insertarPalabraVertical(palabra, derecho):
                return True
            intentos += 1
        return False

    def insertarPalabraHorizontal(self, palabra, derecho):
        if not derecho:
            palabra = palabra[::-1]
        inicioFila = random.randint(0, self.filas - 1)
        inicioColumna = random.randint(0, self.columnas - len(palabra))
        if all(self.casillas[inicioFila][inicioColumna + i]['text'] in ('', palabra[i]) for i in range(len(palabra))):
            for i in range(len(palabra)):
                self.casillas[inicioFila][inicioColumna + i]['text'] = palabra[i]
            return True
        return False

    def insertarPalabraVertical(self, palabra, derecho):
        if not derecho:
            palabra = palabra[::-1]
        inicioFila = random.randint(0, self.filas - len(palabra))
        inicioColumna = random.randint(0, self.columnas - 1)
        if all(self.casillas[inicioFila + i][inicioColumna]['text'] in ('', palabra[i]) for i in range(len(palabra))):
            for i in range(len(palabra)):
                self.casillas[inicioFila + i][inicioColumna]['text'] = palabra[i]
            return True
        return False

    def letrasRandom(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.casillas[i][j]['text'] == '':
                    self.casillas[i][j]['text'] = random.choice(string.ascii_uppercase)

    def seleccionarLetras(self, event):
        boton = event.widget
        if boton.cget('bg') == "#b8c0ff":
            boton.config(bg="#f2cc8f")
        else:
            boton.config(bg="#b8c0ff")

    def tamanio(self, palabra):
        return len(palabra)

InterfazPrincipal().root.mainloop()