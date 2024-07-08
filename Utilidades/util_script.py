import os
from Utilidades import util_script as us
from tkinter import *
from tkinter import messagebox

def listaVacia(lista):
    return len(lista) <= 0

def showListaVacia():
    messagebox.showwarning("Aviso", f"El inventario se encuentra vacío")

def showInProgress():
    messagebox.showwarning("Aviso", "Esta funcionalidad se encuentra en desarrollo.\nDisculpe las molestias")

def showNoRuteSpecified():
    messagebox.showerror("Error", "No se ha escpecificado ninguna ruta de guardado!")

def showProductoNotFound(id):
    messagebox.showerror("Error", f"No existe ningún producto con ID:{id}")

def showProductoEncontrado():
    messagebox.showinfo("Info", f"Producto encontrado")

def showNoProductoSeleccionado():
    messagebox.showwarning("Alerta", f"No hay ningún producto seleccionado, busque la ID del producto")

def showNoDatosIntroducidos(nombreProducto):
    messagebox.showwarning("Alerta", f"No se ha introducido ningún dato para el producto {nombreProducto}")

# GUI FUNCTION
def CheckNuevoProducto(gui, nombreProducto, precioProducto, cantidadProducto, rebajaProducto):
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
    if nombreProducto == "":
        messagebox.showerror("Error", "El nombre del producto no puede quedar vacío")
    else:
        gui.result = nombreProducto

# GUI FUNCTION
def CheckPrecioGUI(gui, precioProducto):
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