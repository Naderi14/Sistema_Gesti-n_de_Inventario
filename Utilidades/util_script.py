import os, json, datetime
from Utilidades import util_script as us
from tkinter import *
from tkinter import messagebox

def ReturnCadenaProcesada(cadena):
    '''
        Función para procesar la cadena entrante y devolverla con vocales sin signos ortograficos
    '''
    letrasAcentuadas = ['á', 'à', 'ä', 'é', 'è', 'ë', 'í', 'ì', 'ï', 'ó', 'ò', 'ö', 'ú', 'ù', 'ü']
    cadenaProcesada = ''
    letraCambiada = False
    for letraCadena in cadena:
        for letraAcentuada in letrasAcentuadas:
            if letraAcentuada == letraCadena:
                if letraAcentuada == 'á' or letraAcentuada == 'à' or letraAcentuada == 'ä':
                    print("Letra acentuada hayada con la A")
                    letraCadena = 'a'
                if letraAcentuada == 'é' or letraAcentuada == 'è' or letraAcentuada == 'ë':
                    print("Letra acentuada hayada con la E")
                    letraCadena = 'e'
                if letraAcentuada == 'í' or letraAcentuada == 'ì' or letraAcentuada == 'ï':
                    print("Letra acentuada hayada con la I")
                    letraCadena = 'i'
                if letraAcentuada == 'ó' or letraAcentuada == 'ò' or letraAcentuada == 'ö':
                    print("Letra acentuada hayada con la O")
                    letraCadena = 'o'
                if letraAcentuada == 'ú' or letraAcentuada == 'ù' or letraAcentuada == 'ü':
                    print("Letra acentuada hayada con la U")
                    letraCadena = 'u'
                cadenaProcesada += letraCadena
                letraCambiada = True
        if letraCambiada == False:
            cadenaProcesada += letraCadena
        letraCambiada = False
    return cadenaProcesada

def listaVacia(lista):
    return len(lista) <= 0

# Puñado de alertas, errores e informaciones para notificar al usuario de sus acciones y condiciones del proceso de la aplicación
def showListaVacia():
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showwarning("Aviso", f"El inventario se encuentra vacío")

def showInProgress():
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showwarning("Aviso", "Esta funcionalidad se encuentra en desarrollo.\nDisculpe las molestias")

def showNoRuteSpecified():
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showerror("Error", "No se ha escpecificado ninguna ruta de guardado!")

def showProductoNotFound(id):
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showerror("Error", f"No existe ningún producto con ID:{id}")

def showProductoEncontrado():
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showinfo("Info", f"Producto encontrado")

def showNoProductoSeleccionado():
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showwarning("Alerta", f"No hay ningún producto seleccionado, busque la ID del producto")

def showNoDatosIntroducidos(nombreProducto):
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showwarning("Alerta", f"No se ha introducido ningún dato para el producto '{nombreProducto}'")

def showNoStockForSell(nombreProducto):
    '''
        Funcion de mensaje para el usuario
    '''
    messagebox.showwarning("Alerta", f"El producto '{nombreProducto}' se encuentra agotado")

# GUI FUNCTION
def CheckNuevoProducto(gui, nombreProducto, precioProducto, cantidadProducto, rebajaProducto):
    '''
        Funcion para control de excepciones de los datos de entrada para la creacion de un nuevo producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - nombreProducto: valor tipo string
            - precioProducto: valor tipo float
            - cantidadProducto: valor tipo int
            - rebajaProducto: valor tipo int
    '''
    nuevoProducto = []
    ok = 0
    # Comprobamos posibles errores de entrada y control de excepciones en cada caso
    if nombreProducto == "":
        messagebox.showerror("Error", "El nombre del producto no puede quedar vacío")
    else:
        nuevoProducto.append(nombreProducto)
        ok += 1
    try:
        precioProducto = round(float(precioProducto), 2)
        if precioProducto <= 0:
            raise ValueError
        else:
            nuevoProducto.append(precioProducto)
            ok += 1
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número mayor a 0")
    try:
        cantidadProducto = int(cantidadProducto)
        if cantidadProducto > 0:
            nuevoProducto.append(cantidadProducto)
            ok += 1
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "La cantidad ha de ser un número mayor a 0 y sin decimales")
    if rebajaProducto == False:
        estaRebajado = False
    else:
        try:
            rebajaProducto = int(rebajaProducto)
            if rebajaProducto > 0:
                estaRebajado = True
                if 0 < rebajaProducto < 101:
                    nuevoProducto.append(rebajaProducto)
                    nuevoProducto.append(estaRebajado)
                    ok += 1
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El porcentaje debe ser un número de 1 a 100 sin decimales\nDejar en blanco el campo si no se desea una rebaja inicial")

    # Condicional final para comprobar si todos los campos son correctos para enviar la lista de valores a procesar
    if ok == 3 and estaRebajado == False or ok == 4 and estaRebajado == True:
        gui.result = nuevoProducto
    else:
        messagebox.showwarning("Alerta", "Algunos de los datos introducidos no son correctos para crear un producto nuevo")

# GUI FUNCTION
def CheckNombreGUI(gui, nombreProducto):
    '''
        Funcion que sirve para control de excepciones para el nombre del producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - nombreProducto: valor tipo string
    '''
    if nombreProducto == "":
        messagebox.showerror("Error", "El nombre del producto no puede quedar vacío")
    else:
        gui.result = nombreProducto

# GUI FUNCTION
def CheckPrecioGUI(gui, precioProducto):
    '''
        Funcion que sirve para control de excepciones para el precio del producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - precioProducto: valor tipo float
    '''
    try:
        precioProducto = round(float(precioProducto), 2)
        if precioProducto <= 0:
            raise ValueError
        else:
            gui.result = precioProducto
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número mayor a 0")

# GUI FUNCTION
def CheckCantidadGUI(gui, cantidadProducto):
    '''
        Funcion que sirve para control de excepciones para la cantidad del producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - cantidadProducto: valor tipo int
    '''
    try:
        cantidadProducto = int(cantidadProducto)
        if cantidadProducto > 0:
            gui.result = cantidadProducto
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "La cantidad ha de ser un número mayor a 0 y sin decimales")
                
# GUI FUNCTION
def CheckRebajaGUI(gui, productoRebaja):
    '''
        Funcion que sirve para control de excepciones para la rebaja del producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - productoRebaja: valor tipo int
    '''
    try:
        productoRebaja = int(productoRebaja)
        if 0 < productoRebaja < 101:
            gui.result = productoRebaja
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El porcentaje debe ser entre 1 y 100, sin decimales")
               
# GUI FUNCTION
def CheckIDGUI(gui, id):
    '''
        Funcion que sirve para control de excepciones para la ID del producto
            - gui: instancia de la clase SGIgui, para poder manipular la variable result
            - id: valor tipo int
    '''
    try:
        id = int(id)
        if id > 0:
            gui.result = id
        else:
            raise ValueError
    except:
        messagebox.showerror("Error", "El ID debe ser mayor a 0, sin decimales")

# =================================================================
# -------------------- FUNCIONES DEPRECATED -----------------------
# =================================================================