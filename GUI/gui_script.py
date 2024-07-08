from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from GestorInventario.gestor_script import Gestor
from Utilidades import util_script as us
from PIL import Image, ImageTk
import rute_script as rs
import matplotlib.pyplot as plt

class SGIgui(ttk.Frame):
    def __init__(self, root):
        # Inicializamos propiedades de SGIApp
        self.root = root
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=4)
        self.root.rowconfigure(0, weight=1)
        self.icono = self.CargarImagen(rs.rutaAdjunto('icono'), (32,32))
        self.root.wm_iconphoto(True, self.icono)
        self.gestor = Gestor()
        self.gestor.AbrirArchivo()
        self.botonActivo = None
        self.productoSeleccionado = None
        self.opcionRebaja = IntVar()
        self.opcionVenderBeforeRmv = IntVar()
        self.imagenReturn = self.CargarImagen(rs.rutaAdjunto('return'), (50,50))

        # Creacion y configuracion del frame de botones del programa
        self.buttonFrame = Frame(self.root, bg='#88ABAD', bd=5, relief='groove')
        self.buttonFrame.grid(row=0, column=0, sticky='nsew')
        self.buttonFrame.grid_propagate(False)
        self.CrearBotones()

        # <<<<<<<<< ------- CREACION de los Frames de las diferentes funcionalidades de la APP --------- >>>>>>>
        self.frames = {}

        # Welcome Frame Config
        self.frames['welcomeFrame'] = Frame(self.root, bg='#5890B0', bd=5, relief='groove') # #FFC0CB = Rosa, #FFFCAD = Amarillo
        self.frames['welcomeFrame'].grid(row=0, column=1, sticky='nsew')
        self.frames['welcomeFrame'].rowconfigure(0, weight=2)
        self.frames['welcomeFrame'].rowconfigure(1, weight=1)
        self.frames['welcomeFrame'].grid_propagate(False)
        self.frames['welcomeFrame'].pack_propagate(False)
        Label(self.frames['welcomeFrame'], text="Bienvenid@ a\n\nS.G.I. Manager\n\nSistema de Gestión de Inventario", 
              bg='#618469', font=('Helvetica', 24, 'bold'), bd=1, relief='sunken').pack(side='top', anchor='n', fill='x', expand=1)
        Label(self.frames['welcomeFrame'], text="Saldo Cuenta: ", font=("Helvetica", 14, 'bold'), bd=1, bg="#5890B0", justify="right").place(x=50, y=300)
        Label(self.frames['welcomeFrame'], text="Valor Bruto: ", font=("Helvetica", 14, 'bold'), bd=1, bg="#5890B0", justify="right").place(x=50, y=400)
        Label(self.frames['welcomeFrame'], text="€", font=("Helvetica", 15), bd=1, bg="#5890B0", justify="right").place(x=425, y=300)
        Label(self.frames['welcomeFrame'], text="€", font=("Helvetica", 15), bd=1, bg="#5890B0", justify="right").place(x=425, y=400)
        self.saldoCuenta = Listbox(self.frames['welcomeFrame'], font=("Helvetica", 14), bd=1, bg="#50F0B0", justify="left", width=20, height=1)
        self.valorBruto = Listbox(self.frames['welcomeFrame'], font=("Helvetica", 14), bd=1, bg="#50F0B0", justify="left", width=20, height=1)
        
        # Crear y configuracion de cada Frame del menú 
        self.ConfigurarFrame('addFrame', '#FFFCAD', "SGI / Agregar un producto nuevo",
                             "Poder agregar un producto nuevo para gestionarlo en inventario activo.\nDebe introducir todos los datos requeridos para completar la acción.")
        self.ConfigurarFrame('updateFrame', '#FFFCAD', "SGI / Actualizar un producto",
                             "Poder actualizar un valor concreto o varios de un mismo producto.\nDebe introducir todos los datos requeridos para completar la acción.")
        self.ConfigurarFrame('sellFrame', '#FFFCAD', "SGI / Vender un producto",
                             "Insertar el producto con el que se ha realizado la venta para\nactualizar el stock del producto y la salida de datos financieros.")
        self.ConfigurarFrame('rebajaFrame', '#FFFCAD', "SGI / Gestionar Rebajas", 
                             "Poder agregar o quitar estados de producto en rebajas.")
        self.ConfigurarFrame('removeFrame', '#FFFCAD', "SGI / Eliminar un producto de la base de datos", 
                             "Poder eliminar de la base de datos un producto existente.\nUna vez realizada la acción, es irreversible")
        self.ConfigurarFrame('showFrame', '#FFFCAD', "SGI / Mostrar inventario", 
                             "Lista de todos los productos del inventario")


        self.frames['welcomeFrame'].tkraise()
        self.CrearMenu()
        self.InfoEtiquetas(100)

    def AbrirTerminos(self):
        ''' 
        Función para poder abrir una nueva ventana en la que cargaremos un .txt previamente adjuntado en los Resources del programa
        ''' 
        terminosScreen = Toplevel(self.root)
        terminosScreen.title("Términos y Condiciones de Uso")
        terminosScreen.wm_iconphoto(True, self.icono)

        terminosFrame = Frame(terminosScreen, width=800, height=600)
        terminosFrame.pack_propagate(False)
        terminosFrame.pack(side='top', fill='both', expand=1)

        scrollbar = Scrollbar(terminosFrame)
        scrollbar.pack(side='right', fill="y")

        text = Text(terminosFrame, wrap='word', yscrollcommand=scrollbar.set)
        text.pack(side='left', fill='both', expand=1)

        scrollbar.config(command=text.yview)

        with open(rs.rutaAdjunto('terminos'), "r", encoding="utf-8") as file:
            terminosTexto = file.read()

        text.insert('end', terminosTexto)


    def CrearMenu(self):
        '''
            Funcion para crear la barra de menú de la ventana root
        '''
        self.menubar = Menu(self.root)

        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Gráfico Financiero", command=self.GenerarGrafica)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exportar Inventario", command=self.ExportarInv)
        self.fileMenu.add_separator()

        self.sgiMenu = Menu(self.menubar, tearoff=0)
        self.sgiMenu.add_command(label="Info SGI", command=self.AbrirTerminos)
        self.sgiMenu.add_separator()
        self.sgiMenu.add_command(label="Salir", command=self.root.destroy)

        self.menubar.add_cascade(label="S. G. I.", menu=self.sgiMenu)
        self.menubar.add_cascade(label="Inventario", menu=self.fileMenu)
        self.root.config(menu=self.menubar)

    def CrearBotones(self):
        '''
            Funcion como dice su nombre, para crear los botones, cargando la imagen correspondiente mediante la ruta en la carpeta Recursos de la App
        '''
        self.iconoAgregar = self.CargarImagen(rs.rutaAdjunto('addItem'), (50,50))
        self.iconoActualizar = self.CargarImagen(rs.rutaAdjunto('updateItem'), (50,50))
        self.iconoVender = self.CargarImagen(rs.rutaAdjunto('sellItem'), (50,50))
        self.iconoRebaja = self.CargarImagen(rs.rutaAdjunto('rebajaItem'), (50,50))
        self.iconoEliminar = self.CargarImagen(rs.rutaAdjunto('removeItem'), (50,50))
        self.iconoShow = self.CargarImagen(rs.rutaAdjunto('showInventario'), (50,50))

        self.botonAgregarP = Button(self.buttonFrame, width=155, height=100, text="Agregar un producto", image=self.iconoAgregar, compound='top', command=lambda: self.CambiarFrame('addFrame'))
        self.botonAgregarP.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.botonActualizarP = Button(self.buttonFrame, width=155, height=100, text="Actualizar un producto", image=self.iconoActualizar, compound='top', command=lambda: self.CambiarFrame('updateFrame'))
        self.botonActualizarP.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.botonVenderP = Button(self.buttonFrame, width=155, height=100, text="Vender un producto", image=self.iconoVender, compound='top', command=lambda: self.CambiarFrame('sellFrame'))
        self.botonVenderP.grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.botonAplicarR = Button(self.buttonFrame, width=155, height=100, text="Gestionar Rebajas", image=self.iconoRebaja, compound='top', command=lambda: self.CambiarFrame('rebajaFrame'))
        self.botonAplicarR.grid(row=3, column=0, sticky='w', padx=10, pady=10)
        self.botonEliminarP = Button(self.buttonFrame, width=155, height=100, text="Eliminar un producto", image=self.iconoEliminar, compound='top', command=lambda: self.CambiarFrame('removeFrame'))
        self.botonEliminarP.grid(row=4, column=0, sticky='w', padx=10, pady=10)
        self.botonMostrarI = Button(self.buttonFrame, width=155, height=100, text="Mostrar inventario", image=self.iconoShow, compound='top', command=lambda: self.CambiarFrame('showFrame'))
        self.botonMostrarI.grid(row=5, column=0, sticky='w', padx=10, pady=10)

    def CambiarFrame(self, nombreFrame):
        '''
            Función para realizar un cambio de Frame(derecha) a medida que nos vamos por los distintos menús mediante los botones de la izquierda
            restauraremos todos los botones a su color por defecto y hayaremos que Frame fue llamado para cambiar para colorear el botón del menú correspondiente
        '''
        # Resetear variables de los Entrys y ListBox
        self.entryNombre1.delete(0, 'end')
        self.entryNombre1.insert(0, "Ej: Jabón de manos")
        self.entryNombre2.delete(0, 'end')
        self.entryNombre2.insert(0, "Ej: Jabón de manos")
        self.entryPrecio1.delete(0, 'end')
        self.entryPrecio1.insert(0, "Ej: 1.45")
        self.entryPrecio2.delete(0, 'end')
        self.entryPrecio2.insert(0, "Ej: 1.45")
        self.entryCantidad1.delete(0, 'end')
        self.entryCantidad1.insert(0, "Ej: 10")
        self.entryCantidad2.delete(0, 'end')
        self.entryCantidad2.insert(0, "Ej: 10")
        self.entryCantidad3.delete(0, 'end')
        self.entryCantidad3.insert(0, "Ej: 10")
        self.entryRebaja1.delete(0, 'end')
        self.entryRebaja1.insert(0, "Ej: 25")
        self.entryRebaja2.delete(0, 'end')
        self.entryRebaja2.insert(0, "Ej: 25")
        self.entryID1.delete(0, 'end')
        self.entryID1.insert(0, "Ej: 4")
        self.entryID2.delete(0, 'end')
        self.entryID2.insert(0, "Ej: 4")
        self.entryID3.delete(0, 'end')
        self.entryID3.insert(0, "Ej: 4")
        self.entryID4.delete(0, 'end')
        self.entryID4.insert(0, "Ej: 4")
        self.infoNombre0.delete(0, "end")
        self.infoNombre1.delete(0, "end")
        self.infoNombre2.delete(0, "end")
        self.infoNombre3.delete(0, "end")
        self.infoPrecio0.delete(0, "end")
        self.infoPrecio1.delete(0, "end")
        self.infoPrecio2.delete(0, "end")
        self.infoPrecio3.delete(0, "end")
        self.infoCantidad0.delete(0, "end")
        self.infoCantidad1.delete(0, "end")
        self.infoCantidad2.delete(0, "end")
        self.infoCantidad3.delete(0, "end")
        self.infoRebaja.delete(0, "end")
        self.productoSeleccionado = None

        # Activar el boton correspondiente con el frame seleccionado
        if self.botonActivo:
            self.botonActivo.config(bg="#FFFFFF")
        self.frames[nombreFrame].tkraise()
        if nombreFrame == 'addFrame':
            self.botonActivo = self.botonAgregarP
        elif nombreFrame == 'updateFrame':
            self.botonActivo = self.botonActualizarP
        elif nombreFrame == 'sellFrame':
            self.botonActivo = self.botonVenderP
        elif nombreFrame == 'rebajaFrame':
            self.botonActivo = self.botonAplicarR
        elif nombreFrame == 'removeFrame':
            self.botonActivo = self.botonEliminarP
        elif nombreFrame == 'showFrame':
            self.MostrarLista()
            self.botonActivo = self.botonMostrarI
        self.botonActivo.config(bg="#8BC0CC")
        if nombreFrame == 'welcomeFrame':
            self.InfoEtiquetas(100)
            self.botonActivo.config(bg="#FFFFFF")

    # Funciones de FocusIn y FocusOut de los Entry de todos los menús
    def entryNombreFocusIn1(self, event):
        if self.entryNombre1.get() == "Ej: Jabón de manos":
            self.entryNombre1.delete(0, "end")
            self.entryNombre1.config(fg="Black")
    
    def entryNombreFocusOut1(self, event):
        if self.entryNombre1.get() == "":
            self.entryNombre1.insert(0, "Ej: Jabón de manos")
            self.entryNombre1.config(fg="Gray")

    def entryNombreFocusIn2(self, event):
        if self.entryNombre2.get() == "Ej: Jabón de manos":
            self.entryNombre2.delete(0, "end")
            self.entryNombre2.config(fg="Black")
    
    def entryNombreFocusOut2(self, event):
        if self.entryNombre2.get() == "":
            self.entryNombre2.insert(0, "Ej: Jabón de manos")
            self.entryNombre2.config(fg="Gray")

    def entryPrecioFocusIn1(self, event):
        if self.entryPrecio1.get() == "Ej: 1.45":
            self.entryPrecio1.delete(0, "end")
            self.entryPrecio1.config(fg="Black")

    def entryPrecioFocusOut1(self, event):
        if self.entryPrecio1.get() == "":
            self.entryPrecio1.insert(0, "Ej: 1.45")
            self.entryPrecio1.config(fg="Gray")

    def entryPrecioFocusIn2(self, event):
        if self.entryPrecio2.get() == "Ej: 1.45":
            self.entryPrecio2.delete(0, "end")
            self.entryPrecio2.config(fg="Black")

    def entryPrecioFocusOut2(self, event):
        if self.entryPrecio2.get() == "":
            self.entryPrecio2.insert(0, "Ej: 1.45")
            self.entryPrecio2.config(fg="Gray")

    def entryCantidadFocusIn1(self, event):
        if self.entryCantidad1.get() == "Ej: 10":
            self.entryCantidad1.delete(0, "end")
            self.entryCantidad1.config(fg="Black")

    def entryCantidadFocusOut1(self, event):
        if self.entryCantidad1.get() == "":
            self.entryCantidad1.insert(0, "Ej: 10")
            self.entryCantidad1.config(fg="Gray")

    def entryCantidadFocusIn2(self, event):
        if self.entryCantidad2.get() == "Ej: 10":
            self.entryCantidad2.delete(0, "end")
            self.entryCantidad2.config(fg="Black")

    def entryCantidadFocusOut2(self, event):
        if self.entryCantidad2.get() == "":
            self.entryCantidad2.insert(0, "Ej: 10")
            self.entryCantidad2.config(fg="Gray")

    def entryCantidadFocusIn3(self, event):
        if self.entryCantidad3.get() == "Ej: 10":
            self.entryCantidad3.delete(0, "end")
            self.entryCantidad3.config(fg="Black")

    def entryCantidadFocusOut3(self, event):
        if self.entryCantidad3.get() == "":
            self.entryCantidad3.insert(0, "Ej: 10")
            self.entryCantidad3.config(fg="Gray")

    def entryRebajaFocusIn1(self, event):
        if self.entryRebaja1.get() == "Ej: 25":
            self.entryRebaja1.delete(0, "end")
            self.entryRebaja1.config(fg="Black")

    def entryRebajaFocusOut1(self, event):
        if self.entryRebaja1.get() == "":
            self.entryRebaja1.insert(0, "Ej: 25")
            self.entryRebaja1.config(fg="Gray")

    def entryRebajaFocusIn2(self, event):
        if self.entryRebaja2.get() == "Ej: 25":
            self.entryRebaja2.delete(0, "end")
            self.entryRebaja2.config(fg="Black")

    def entryRebajaFocusOut2(self, event):
        if self.entryRebaja2.get() == "":
            self.entryRebaja2.insert(0, "Ej: 25")
            self.entryRebaja2.config(fg="Gray")

    def entryIDFocusIn1(self, event):
        if self.entryID1.get() == "Ej: 4":
            self.entryID1.delete(0, "end")
            self.entryID1.config(fg="Black")

    def entryIDFocusOut1(self, event):
        if self.entryID1.get() == "":
            self.entryID1.insert(0, "Ej: 4")
            self.entryID1.config(fg="Gray")

    def entryIDFocusIn2(self, event):
        if self.entryID2.get() == "Ej: 4":
            self.entryID2.delete(0, "end")
            self.entryID2.config(fg="Black")

    def entryIDFocusOut2(self, event):
        if self.entryID2.get() == "":
            self.entryID2.insert(0, "Ej: 4")
            self.entryID2.config(fg="Gray")

    def entryIDFocusIn3(self, event):
        if self.entryID3.get() == "Ej: 4":
            self.entryID3.delete(0, "end")
            self.entryID3.config(fg="Black")

    def entryIDFocusOut3(self, event):
        if self.entryID3.get() == "":
            self.entryID3.insert(0, "Ej: 4")
            self.entryID3.config(fg="Gray")

    def entryIDFocusIn4(self, event):
        if self.entryID4.get() == "Ej: 4":
            self.entryID4.delete(0, "end")
            self.entryID4.config(fg="Black")

    def entryIDFocusOut4(self, event):
        if self.entryID4.get() == "":
            self.entryID4.insert(0, "Ej: 4")
            self.entryID4.config(fg="Gray")

    def ConfigurarFrame(self, nombreFrame, bgColor, labelTitle, labelText):
        '''
            Función para ahorrar decenas de lineas de codigo repetitivo para crear y configurar inicialmente cada Frame de los 
            distintos menús de la aplicación
        '''
        self.frames[nombreFrame] = Frame(self.root, bg=bgColor, bd=5, relief='groove')
        self.frames[nombreFrame].grid(row=0, column=1, sticky='nsew')
        self.frames[nombreFrame].grid_propagate(False)
        self.frames[nombreFrame].pack_propagate(False)

        self.frames[nombreFrame].rowconfigure(0, weight=1)
        self.frames[nombreFrame].rowconfigure(1, weight=5)
        self.frames[nombreFrame].columnconfigure(0, weight=1)

        topFrame = Frame(self.frames[nombreFrame], bg='#97C371', bd=5, relief='groove')
        topFrame.grid(row=0, column=0, sticky='nsew')
        topFrame.grid_propagate(False)
        topFrame.pack_propagate(False)
        Label(topFrame, text=labelTitle, bg="#97C371", font=('Helvetica', 20, 'bold'), bd=1).pack(anchor='nw', padx=25, pady=5)
        Label(topFrame, text=labelText, bg="#97C371", font=('Comic Sans', 12), bd=1, justify='left').pack(anchor='nw', padx=25)
        
        self.botFrame = Frame(self.frames[nombreFrame], bg="#FFFCAD", bd=5, relief='groove')
        self.botFrame.grid(row=1, column=0, sticky='nsew')
        self.botFrame.grid_propagate(False)
        self.botFrame.pack_propagate(False)
        self.botonReturn = Button(self.botFrame, text="Volver", width=125, height=75, image=self.imagenReturn, compound='top', 
               command=lambda: self.CambiarFrame('welcomeFrame')).pack(padx=5, pady=5, anchor='se', side='bottom')

        # Aquí vendran configudaros los aspectos específicos para cada Frame
        if nombreFrame == 'addFrame':
            self.botFrame.config(bg="#E6E6FA") # Lavanda
            Label(self.botFrame, text="Nombre del producto: ", font=("Helvetica", 14), bd=1, bg="#E6E6FA", justify="right").grid(row=0, column=0, sticky='w', padx=10, pady=10)
            self.entryNombre1 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryNombre1.insert(0, "Ej: Jabón de manos")
            self.entryNombre1.bind("<FocusIn>", self.entryNombreFocusIn1)
            self.entryNombre1.bind("<FocusOut>", self.entryNombreFocusOut1)
            self.entryNombre1.grid(row=0, column=1, padx=10, pady=10)
            Label(self.botFrame, text="Precio del producto: ", font=("Helvetica", 14), bd=1, bg="#E6E6FA", justify="right").grid(row=1, column=0, sticky='w', padx=10, pady=10)
            self.entryPrecio1 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryPrecio1.insert(0, "Ej: 1.45")
            self.entryPrecio1.bind("<FocusIn>", self.entryPrecioFocusIn1)
            self.entryPrecio1.bind("<FocusOut>", self.entryPrecioFocusOut1)
            self.entryPrecio1.grid(row=1, column=1, padx=10, pady=10)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#E6E6FA", justify="left").grid(row=1, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Cantidad del producto: ", font=("Helvetica", 14), bd=1, bg="#E6E6FA", justify="right").grid(row=2, column=0, sticky='w', padx=10, pady=10)
            self.entryCantidad1 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryCantidad1.insert(0, "Ej: 10")
            self.entryCantidad1.bind("<FocusIn>", self.entryCantidadFocusIn1)
            self.entryCantidad1.bind("<FocusOut>", self.entryCantidadFocusOut1)
            self.entryCantidad1.grid(row=2, column=1, padx=10, pady=10)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#E6E6FA", justify="left").grid(row=2, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Porcentaje de rebaja (Opcional): ", font=("Helvetica", 14), bd=1, bg="#E6E6FA", justify="right").grid(row=4, column=0, sticky='w', padx=10, pady=10)
            self.entryRebaja1 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryRebaja1.insert(0, "Ej: 25")
            self.entryRebaja1.bind("<FocusIn>", self.entryRebajaFocusIn1)
            self.entryRebaja1.bind("<FocusOut>", self.entryRebajaFocusOut1)
            self.entryRebaja1.grid(row=4, column=1, padx=10, pady=10)
            Label(self.botFrame, text="%", font=("Helvetica", 12), bd=1, bg="#E6E6FA", justify="left").grid(row=4, column=2, sticky='w', pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=5, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=5, column=1, sticky='ew', pady=20)
            Button(self.botFrame, text="Submit", width=30, height=2, bg="#CCC", command=self.AgregarProducto).grid(row=6, column=1, sticky='w', padx=10, pady=10)

        elif nombreFrame == 'updateFrame':
            self.botFrame.config(bg="#B0E0E6") # Menta
            Label(self.botFrame, text="ID del producto: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=0, column=0, sticky='w', padx=10, pady=10)
            self.entryID1 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryID1.insert(0, "Ej: 4")
            self.entryID1.bind("<FocusIn>", self.entryIDFocusIn1)
            self.entryID1.bind("<FocusOut>", self.entryIDFocusOut1)
            self.entryID1.grid(row=0, column=1, padx=10, pady=10)
            Button(self.botFrame, text="Buscar ID", width=30, height=2, bg="#CCC", command=self.BuscarID).grid(row=1, column=1, sticky='w', padx=10, pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=1, sticky='ew', pady=20)

            Label(self.botFrame, text="Nombre del producto: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=3, column=0, sticky='w', padx=10, pady=10)
            self.infoNombre0 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="left", width=20, height=1)
            Label(self.botFrame, text="Precio del producto: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=4, column=0, sticky='w', padx=10, pady=10)
            self.infoPrecio0 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="left", width=20, height=1)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#B0E0E6", justify="left").grid(row=4, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Cantidad en Stock: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=5, column=0, sticky='w', padx=10, pady=10)
            self.infoCantidad0 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="left", width=20, height=1)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#B0E0E6", justify="left").grid(row=5, column=2, sticky='w', pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=6, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=6, column=1, sticky='ew', pady=20)

            Label(self.botFrame, text="Actualizar Nombre: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=7, column=0, sticky='w', padx=10, pady=10)
            self.entryNombre2 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryNombre2.insert(0, "Ej: Jabón de manos")
            self.entryNombre2.bind("<FocusIn>", self.entryNombreFocusIn2)
            self.entryNombre2.bind("<FocusOut>", self.entryNombreFocusOut2)
            self.entryNombre2.grid(row=7, column=1, padx=10, pady=10)
            Label(self.botFrame, text="Actualizar Precio: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=8, column=0, sticky='w', padx=10, pady=10)
            self.entryPrecio2 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryPrecio2.insert(0, "Ej: 1.45")
            self.entryPrecio2.bind("<FocusIn>", self.entryPrecioFocusIn2)
            self.entryPrecio2.bind("<FocusOut>", self.entryPrecioFocusOut2)
            self.entryPrecio2.grid(row=8, column=1, padx=10, pady=10)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#B0E0E6", justify="left").grid(row=8, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Actualizar Cantidad: ", font=("Helvetica", 14), bd=1, bg="#B0E0E6", justify="right").grid(row=9, column=0, sticky='w', padx=10, pady=10)
            self.entryCantidad2 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryCantidad2.insert(0, "Ej: 10")
            self.entryCantidad2.bind("<FocusIn>", self.entryCantidadFocusIn2)
            self.entryCantidad2.bind("<FocusOut>", self.entryCantidadFocusOut2)
            self.entryCantidad2.grid(row=9, column=1, padx=10, pady=10)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#B0E0E6", justify="left").grid(row=9, column=2, sticky='w', pady=10)
            Button(self.botFrame, text="Actualizar", width=30, height=2, bg="#CCC", command=self.ActualizarProducto).grid(row=10, column=1, sticky='w', padx=10, pady=10)

        elif nombreFrame == 'sellFrame':
            self.botFrame.config(bg="#FFDAB9") # Durazno
            Label(self.botFrame, text="ID del producto: ", font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="right").grid(row=0, column=0, sticky='w', padx=10, pady=10)
            self.entryID2 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryID2.insert(0, "Ej: 4")
            self.entryID2.bind("<FocusIn>", self.entryIDFocusIn2)
            self.entryID2.bind("<FocusOut>", self.entryIDFocusOut2)
            self.entryID2.grid(row=0, column=1, padx=10, pady=10)
            Button(self.botFrame, text="Buscar ID", width=30, height=2, bg="#CCC", command=self.BuscarID).grid(row=1, column=1, sticky='w', padx=15, pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=1, sticky='ew', pady=20)
        

            Label(self.botFrame, text="Nombre del producto: ", font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="right").grid(row=4, column=0, sticky='w', padx=10, pady=10)
            self.infoNombre1 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="left", width=20, height=1)
            Label(self.botFrame, text="Precio del producto: ", font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="right").grid(row=5, column=0, sticky='w', padx=10, pady=10)
            self.infoPrecio1 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="left", width=20, height=1)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#FFDAB9", justify="left").grid(row=5, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Cantidad en Stock: ", font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="right").grid(row=6, column=0, sticky='w', padx=10, pady=10)
            self.infoCantidad1 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="left", width=20, height=1)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#FFDAB9", justify="left").grid(row=6, column=2, sticky='w', pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=7, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=7, column=1, sticky='ew', pady=20)
            Label(self.botFrame, text="Cantidad a vender: ", font=("Helvetica", 14), bd=1, bg="#FFDAB9", justify="right").grid(row=8, column=0, sticky='w', padx=10, pady=10)
            self.entryCantidad3 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryCantidad3.insert(0, "Ej: 10")
            self.entryCantidad3.bind("<FocusIn>", self.entryCantidadFocusIn3)
            self.entryCantidad3.bind("<FocusOut>", self.entryCantidadFocusOut3)
            self.entryCantidad3.grid(row=8, column=1, padx=10, pady=10)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#FFDAB9", justify="left").grid(row=8, column=2, sticky='w', pady=10)
            Button(self.botFrame, text="Vender", width=30, height=2, bg="#CCC", command=self.VenderProducto).grid(row=9, column=1, sticky='w', padx=15, pady=10)

        elif nombreFrame == 'rebajaFrame':
            self.botFrame.config(bg="#F0E68C") # Luz de Luna
            Label(self.botFrame, text="ID del producto: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=0, column=0, sticky='w', padx=10, pady=10)
            self.entryID3 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryID3.insert(0, "Ej: 4")
            self.entryID3.bind("<FocusIn>", self.entryIDFocusIn3)
            self.entryID3.bind("<FocusOut>", self.entryIDFocusOut3)
            self.entryID3.grid(row=0, column=1, padx=10, pady=10)
            Button(self.botFrame, text="Buscar ID", width=30, height=2, bg="#CCC", command=self.BuscarID).grid(row=1, column=1, sticky='w', padx=15, pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=1, sticky='ew', pady=20)
                

            Label(self.botFrame, text="Nombre del producto: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=4, column=0, sticky='w', padx=10, pady=10)
            self.infoNombre2 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="left", width=20, height=1)
            Label(self.botFrame, text="Precio del producto: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=5, column=0, sticky='w', padx=10, pady=10)
            self.infoPrecio2 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="left", width=20, height=1)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#F0E68C", justify="left").grid(row=5, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Cantidad en Stock: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=6, column=0, sticky='w', padx=10, pady=10)
            self.infoCantidad2 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="left", width=20, height=1)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#F0E68C", justify="left").grid(row=6, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Rebaja: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=7, column=0, sticky='w', padx=10, pady=10)
            self.infoRebaja = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="left", width=20, height=1)
            Label(self.botFrame, text="%", font=("Helvetica", 12), bd=1, bg="#F0E68C", justify="left").grid(row=7, column=2, sticky='w', pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=8, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=8, column=1, sticky='ew', pady=20)
            Label(self.botFrame, text="Porcentaje Rebaja: ", font=("Helvetica", 14), bd=1, bg="#F0E68C", justify="right").grid(row=9, column=0, sticky='w', padx=10, pady=10)
            self.entryRebaja2 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryRebaja2.insert(0, "Ej: 25")
            self.entryRebaja2.bind("<FocusIn>", self.entryRebajaFocusIn2)
            self.entryRebaja2.bind("<FocusOut>", self.entryRebajaFocusOut2)
            self.entryRebaja2.grid(row=9, column=1, padx=10, pady=10)
            Label(self.botFrame, text="%", font=("Helvetica", 12), bd=1, bg="#F0E68C", justify="left").grid(row=9, column=2, sticky='w', pady=10)
            Button(self.botFrame, text="Quitar Rebaja", width=30, height=2, bg="#CCC", command=self.QuitarRebaja).grid(row=10, column=0, sticky='w', padx=15, pady=10)
            Button(self.botFrame, text="Aplicar Rebaja", width=30, height=2, bg="#CCC", command=self.AplicarRebaja).grid(row=10, column=1, sticky='w', padx=15, pady=10)


        elif nombreFrame == 'removeFrame':
            self.botFrame.config(bg="#F4C2C2") # Rosa Pastel
            Label(self.botFrame, text="ID del producto: ", font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="right").grid(row=0, column=0, sticky='w', padx=10, pady=10)
            self.entryID4 = Entry(self.botFrame, width=40, bg="#FFEFFF", fg="Gray")
            self.entryID4.insert(0, "Ej: 4")
            self.entryID4.bind("<FocusIn>", self.entryIDFocusIn4)
            self.entryID4.bind("<FocusOut>", self.entryIDFocusOut4)
            self.entryID4.grid(row=0, column=1, padx=10, pady=10)
            Button(self.botFrame, text="Buscar ID", width=30, height=2, bg="#CCC", command=self.BuscarID).grid(row=1, column=1, sticky='w', padx=15, pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=2, column=1, sticky='ew', pady=20)


            Label(self.botFrame, text="Nombre del producto: ", font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="right").grid(row=4, column=0, sticky='w', padx=10, pady=10)
            self.infoNombre3 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="left", width=20, height=1)
            Label(self.botFrame, text="Precio del producto: ", font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="right").grid(row=5, column=0, sticky='w', padx=10, pady=10)
            self.infoPrecio3 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="left", width=20, height=1)
            Label(self.botFrame, text="€", font=("Helvetica", 12), bd=1, bg="#F4C2C2", justify="left").grid(row=5, column=2, sticky='w', pady=10)
            Label(self.botFrame, text="Cantidad en Stock: ", font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="right").grid(row=6, column=0, sticky='w', padx=10, pady=10)
            self.infoCantidad3 = Listbox(self.botFrame, font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="left", width=20, height=1)
            Label(self.botFrame, text="uds.", font=("Helvetica", 12), bd=1, bg="#F4C2C2", justify="left").grid(row=6, column=2, sticky='w', pady=10)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=7, column=0, sticky='ew', pady=20)
            Frame(self.botFrame, height=2, bd=1, relief='sunken', bg='black').grid(row=7, column=1, sticky='ew', pady=20)
            Label(self.botFrame, text="Vender stock antes de eliminar: ", font=("Helvetica", 14), bd=1, bg="#F4C2C2", justify="right").grid(row=8, column=0, sticky='w', padx=10, pady=10)
            radio1 = Radiobutton(self.botFrame, text="Si", variable=self.opcionVenderBeforeRmv, value=1, bg="#F4C2C2")
            radio1.grid(row=8, column=1, padx=10, pady=10, sticky='w')
            radio2 = Radiobutton(self.botFrame, text="No", variable=self.opcionVenderBeforeRmv, value=2, bg="#F4C2C2")
            radio2.grid(row=8, column=1, padx=10, pady=10, sticky='ns')
            Button(self.botFrame, text="Eliminar", width=30, height=2, bg="#CCC", command=self.EliminarProducto).grid(row=9, column=1, sticky='w', padx=15, pady=10)

        elif nombreFrame == 'showFrame':
            self.listaProductos = Listbox(self.botFrame, bg="#95E19B", font=("Helvetica", 14), justify='left', relief='groove', bd=5)
            self.listaProductos.pack(fill="both", expand=1)
            self.listaProductos.bind('<Button-1>', self.QuitarSeleccionLista)
            self.listaProductos.bind('<Button-2>', self.QuitarSeleccionLista)
            
            self.botFrame.config(bg="#ADD8E6") # Celeste

    def QuitarSeleccionLista(self, event = None):
        return "break"

    def MostrarLista(self):
        #self.frameLista = Frame(self.botFrame, bg="#65919B")
        #self.frameLista.pack(fill="both", expand=1)
        self.listaProductos.delete(0, "end")
        self.listaProductos.insert(END, "---------------------------------------------------------------------------------------------------------------------------")
        # Añadimos los productos a la lista
        for producto in self.gestor.productos:
            #self.listaProductos.insert(END, f"ID:{producto.id} | {producto.nombreProducto} | {producto.cantidad}uds. | {producto.precio}€")
            if producto.estaRebajado == False:
                texto = f" ID:{producto.id}    |    {producto.nombreProducto}    |    {producto.cantidad} uds.    |    {producto.precio}€\n"
            else:
                texto = f" ID:{producto.id}    |    {producto.nombreProducto}    |    {producto.cantidad} uds.    |    {producto.precioReal}€ - {producto.rebaja}% = {producto.precio}€\n"
            self.listaProductos.insert(END, texto)
            self.listaProductos.insert(END, "---------------------------------------------------------------------------------------------------------------------------")
            #listaItem = Label(self.botFrame, text=texto, font=("Helvetica", 14), bd=1, bg="#65919B", width=50, justify="right").pack(fill='y',anchor='nw', padx=5, pady=5)
        
        #canvas = Canvas(self.frameLista, bg="#65919B")
        #canvas.pack(fill="both", expand=1)

        #scrollBar = Scrollbar(self.frameLista, orient='vertical', command=canvas.yview)
        #canvas.config(yscrollcommand=scrollBar.set)
        #scrollBar.pack(side="right", fill="y")

    def BuscarID(self):
        # Reset de todas las etiquetas
        self.infoNombre1.delete(0, "end")
        self.infoNombre2.delete(0, "end")
        self.infoNombre3.delete(0, "end")
        self.infoPrecio1.delete(0, "end")
        self.infoPrecio2.delete(0, "end")
        self.infoPrecio3.delete(0, "end")
        self.infoCantidad1.delete(0, "end")
        self.infoCantidad2.delete(0, "end")
        self.infoCantidad3.delete(0, "end")
        self.infoRebaja.delete(0, "end")
        self.result = None
        id = "Ej: 4"
        if self.entryID1.get() != "Ej: 4":
            id = self.entryID1.get()
            numEntry = 0 # Esta variable es para saber donde se han de informar los datos en la GUI del producto encontrado mas adelante en InfoEtiquetas()
        elif self.entryID2.get() != "Ej: 4":
            id = self.entryID2.get()
            numEntry = 1
        elif self.entryID3.get() != "Ej: 4":
            id = self.entryID3.get()
            numEntry = 2
        elif self.entryID4.get() != "Ej: 4":
            id = self.entryID4.get()
            numEntry = 3

        us.CheckIDGUI(self, id)

        if self.result:
            self.productoSeleccionado = self.gestor.BuscarProductoGUI(self.result)
            self.InfoEtiquetas(numEntry)
            
    def InfoEtiquetas(self, numEntry):
        if self.productoSeleccionado:
            if numEntry == 0:
                self.infoNombre0.insert(0, f"{self.productoSeleccionado.nombreProducto}")
                self.infoNombre0.grid(row=3, column=1, sticky='w', padx=10, pady=10)
                self.infoPrecio0.insert(0, f"{self.productoSeleccionado.precio}")
                self.infoPrecio0.grid(row=4, column=1, sticky='w', padx=10, pady=10)
                self.infoCantidad0.insert(0, f"{self.productoSeleccionado.cantidad}")
                self.infoCantidad0.grid(row=5, column=1, sticky='w', padx=10, pady=10)
            if numEntry == 1:
                self.infoNombre1.insert(0, f"{self.productoSeleccionado.nombreProducto}")
                self.infoNombre1.grid(row=4, column=1, sticky='w', padx=10, pady=10)
                self.infoPrecio1.insert(0, f"{self.productoSeleccionado.precio}")
                self.infoPrecio1.grid(row=5, column=1, sticky='w', padx=10, pady=10)
                self.infoCantidad1.insert(0, f"{self.productoSeleccionado.cantidad}")
                self.infoCantidad1.grid(row=6, column=1, sticky='w', padx=10, pady=10)
            if numEntry == 2:
                self.infoNombre2.insert(0, f"{self.productoSeleccionado.nombreProducto}")
                self.infoNombre2.grid(row=4, column=1, sticky='w', padx=10, pady=10)
                self.infoPrecio2.insert(0, f"{self.productoSeleccionado.precio}")
                self.infoPrecio2.grid(row=5, column=1, sticky='w', padx=10, pady=10)
                self.infoCantidad2.insert(0, f"{self.productoSeleccionado.cantidad}")
                self.infoCantidad2.grid(row=6, column=1, sticky='w', padx=10, pady=10)
                self.infoRebaja.insert(0, f"{self.productoSeleccionado.rebaja}")
                self.infoRebaja.grid(row=7, column=1, sticky='w', padx=10, pady=10)
            if numEntry == 3:
                self.infoNombre3.insert(0, f"{self.productoSeleccionado.nombreProducto}")
                self.infoNombre3.grid(row=4, column=1, sticky='w', padx=10, pady=10)
                self.infoPrecio3.insert(0, f"{self.productoSeleccionado.precio}")
                self.infoPrecio3.grid(row=5, column=1, sticky='w', padx=10, pady=10)
                self.infoCantidad3.insert(0, f"{self.productoSeleccionado.cantidad}")
                self.infoCantidad3.grid(row=6, column=1, sticky='w', padx=10, pady=10)
        if numEntry == 100:
            self.saldoCuenta.delete(0, 'end')
            self.saldoCuenta.insert(0, f"{round(self.gestor.saldoCuenta, 2)}")
            self.saldoCuenta.place(x=200, y=300)
            self.valorBruto.delete(0, 'end')
            self.valorBruto.insert(0, f"{round(self.gestor.valorBruto, 2)}")
            self.valorBruto.place(x=200, y=400)
            self.saldoCuenta.bind('<Button-1>', self.QuitarSeleccionLista)
            self.saldoCuenta.bind('<Button-2>', self.QuitarSeleccionLista)
            self.valorBruto.bind('<Button-1>', self.QuitarSeleccionLista)
            self.valorBruto.bind('<Button-2>', self.QuitarSeleccionLista)

    def AgregarProducto(self):
        '''
            Funcion aun en desarrollo
        '''
        self.result = None

        if self.entryNombre1.get() != "Ej: Jabón de manos":
            nombre = self.entryNombre1.get()
        else:
            nombre = ""
        precio = self.entryPrecio1.get()
        cantidad = self.entryCantidad1.get()
        porcentajeRebaja = self.entryRebaja1.get()
        if porcentajeRebaja == None or porcentajeRebaja == "Ej: 25" or porcentajeRebaja == "":
            us.CheckNuevoProducto(self, nombre, precio, cantidad, False)
        else:
            us.CheckNuevoProducto(self, nombre, precio, cantidad, porcentajeRebaja)

        if len(self.result) == 5:
            if self.result[0] and self.result[1] and self.result[2] and self.result[3] and self.result[4]:
                nombre = self.result[0]
                precio = self.result[1]
                cantidad = self.result[2]
                rebaja = self.result[3]
                estaRebajado = self.result[4]
                self.gestor.AgregarProductoGUI(nombre, cantidad, precio, rebaja, estaRebajado)
                messagebox.showinfo("Info", "Producto agregado correctamente con rebaja")
                self.InfoEtiquetas(100)
                self.CambiarFrame('addFrame')
                self.gestor.GuardarArchivo()
        else:
            if self.result[0] and self.result[1] and self.result[2]:
                nombre = self.result[0]
                precio = self.result[1]
                cantidad = self.result[2]
                self.gestor.AgregarProductoGUI(nombre, cantidad, precio)
                messagebox.showinfo("Info", "Producto agregado correctamente")
                self.InfoEtiquetas(100)
                self.CambiarFrame('addFrame')
                self.gestor.GuardarArchivo()

    def ActualizarProducto(self):
        if self.productoSeleccionado:
            opcion = False
            itemsIntroducidos = False
            itemsProducto = {
                'nombre' : None,
                'precio' : None,
                'cantidad' : None
            }
            if self.entryNombre2.get() == "Ej: Jabón de manos" and self.entryCantidad2.get() == "Ej: 10" and self.entryPrecio2.get() == "Ej: 1.45":
                us.showNoDatosIntroducidos(self.productoSeleccionado.nombreProducto)
            if self.entryNombre2.get() != "Ej: Jabón de manos":
                self.result = None
                nombre = self.entryNombre2.get()
                us.CheckNombreGUI(self, nombre)
                if self.result != None:
                    itemsProducto['nombre'] = self.result
                    itemsIntroducidos = True
                    print("NOMBRE INTRODUCIDO CORRECTAMENTE")
            if self.entryPrecio2.get() != "Ej: 1.45":
                self.result = None
                precio = self.entryPrecio2.get()
                us.CheckPrecioGUI(self, precio)
                if self.result != None:
                    if self.productoSeleccionado.estaRebajado:
                        opcion = messagebox.askyesno("Producto Rebajado", f"El producto '{self.productoSeleccionado.nombreProducto}' tiene una rebaja del {self.productoSeleccionado.rebaja}%, quiere mantener el producto en rebaja?")
                    itemsProducto['precio'] = self.result
                    itemsIntroducidos = True
                    print("PRECIO INTRODUCIDO CORRECTAMENTE")
            if self.entryCantidad2.get() != "Ej: 10":
                self.result = None
                cantidad = self.entryCantidad2.get()
                us.CheckCantidadGUI(self, cantidad)
                if self.result != None:
                    itemsProducto['cantidad'] = self.result
                    itemsIntroducidos = True
                    print("CANTIDAD INTRODUCIDO CORRECTAMENTE")
            if itemsIntroducidos == True:
                if itemsProducto['nombre'] != None and itemsProducto['cantidad'] != None and itemsProducto['precio'] != None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, itemsProducto['nombre'], itemsProducto['cantidad'], itemsProducto['precio'], opcion)
                elif itemsProducto['nombre'] == None and itemsProducto['cantidad'] != None and itemsProducto['precio'] != None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, "", itemsProducto['cantidad'], itemsProducto['precio'], opcion)
                elif itemsProducto['nombre'] != None and itemsProducto['cantidad'] == None and itemsProducto['precio'] != None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, itemsProducto['nombre'], None, itemsProducto['precio'], opcion)
                elif itemsProducto['nombre'] != None and itemsProducto['cantidad'] != None and itemsProducto['precio'] == None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, itemsProducto['nombre'], itemsProducto['cantidad'], None, opcion)
                elif itemsProducto['nombre'] != None and itemsProducto['cantidad'] == None and itemsProducto['precio'] == None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, itemsProducto['nombre'], None, None, opcion)
                elif itemsProducto['nombre'] != None and itemsProducto['cantidad'] == None and itemsProducto['precio'] == None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, itemsProducto['nombre'], None, None, opcion)
                elif itemsProducto['nombre'] == None and itemsProducto['cantidad'] != None and itemsProducto['precio'] == None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, "", itemsProducto['cantidad'], None, opcion)
                elif itemsProducto['nombre'] == None and itemsProducto['cantidad'] == None and itemsProducto['precio'] != None:
                    self.gestor.ActualizarProductoGUI(self.productoSeleccionado, "", None, itemsProducto['precio'], opcion)
                
                messagebox.showinfo("Info", f"Producto '{self.productoSeleccionado.nombreProducto}' actualizado correctamente")
                self.gestor.GuardarArchivo()
                self.InfoEtiquetas(100)
                self.CambiarFrame('updateFrame')
        else:
            us.showNoProductoSeleccionado()

    def VenderProducto(self):
        # Lógica para vender un producto
        if self.productoSeleccionado:
            if self.productoSeleccionado.cantidad != 0:
                if self.entryCantidad3.get() == "Ej: 10":
                    us.showNoDatosIntroducidos(self.productoSeleccionado.nombreProducto)
                else:
                    self.result = None
                    cantidad = self.entryCantidad3.get()
                    us.CheckCantidadGUI(self, cantidad)
                    if self.result != None:
                        if self.result > self.productoSeleccionado.cantidad or self.result <= 0:
                            messagebox.showerror("Error", f"La cantidad no puede ser inferior a 1 ni ser mayor a la cantidad en Stock del producto")
                        else:
                            self.gestor.VenderProductoGUI(self.productoSeleccionado, self.result)
                            messagebox.showinfo("Info", f"Se han vendido {self.result}uds. del producto '{self.productoSeleccionado.nombreProducto}'")
                            self.gestor.GuardarArchivo()
                            self.InfoEtiquetas(100)
                            self.CambiarFrame('sellFrame')
            else:
                messagebox.showwarning("Alerta", f"El producto '{self.productoSeleccionado.nombreProducto}' se encuentra agotado")
        else:
            us.showNoProductoSeleccionado()


    def AplicarRebaja(self):
        # Lógica para aplicar una rebaja
        if self.productoSeleccionado:
            if self.productoSeleccionado.estaRebajado == False:
                if self.entryRebaja2.get() == "Ej: 25":
                    us.showNoDatosIntroducidos(self.productoSeleccionado.nombreProducto)
                else:
                    self.result = None
                    rebaja = self.entryRebaja2.get()
                    us.CheckRebajaGUI(self, rebaja)
                    if self.result != None:
                        self.productoSeleccionado.AplicarRebaja(self.result)
                        print("Rebaja Aplicada")
                        messagebox.showinfo("Info", f"Se ha aplicado una rebaja del {self.result}% al producto '{self.productoSeleccionado.nombreProducto}'")
                        self.gestor.GuardarArchivo()
                        self.CambiarFrame('rebajaFrame')
            else:
                messagebox.showwarning("Alerta", f"El producto '{self.productoSeleccionado.nombreProducto}' ya contiene una rebaja, quítela antes de aplicar otra.")
        else:
            us.showNoProductoSeleccionado()

    def QuitarRebaja(self):
        # Lógica para quitar una rebaja
        if self.productoSeleccionado:
            if self.productoSeleccionado.estaRebajado == True:
                self.productoSeleccionado.QuitarRebaja()
                print("Rebaja Quitada")
                messagebox.showinfo("Info", f"Se ha quitado la rebaja al producto '{self.productoSeleccionado.nombreProducto}'")
                self.gestor.GuardarArchivo()
                self.CambiarFrame('rebajaFrame')
            else:
                messagebox.showwarning("Alerta", f"El producto '{self.productoSeleccionado.nombreProducto}' no se encuentra con ninguna rebaja.")
        else:
            us.showNoProductoSeleccionado()

    def EliminarProducto(self):
        # Lógica para eliminar un producto
        if self.productoSeleccionado:
            print(f"{self.opcionVenderBeforeRmv.get()} | {self.productoSeleccionado.nombreProducto}")
            self.gestor.EliminarProductoGUI(self.productoSeleccionado, self.opcionVenderBeforeRmv.get())
            if self.opcionVenderBeforeRmv.get() == 1:
                messagebox.showinfo("Info", f"Se ha eliminado el producto '{self.productoSeleccionado.nombreProducto}' vendiendo su stock de {self.productoSeleccionado.cantidad}uds.")
            elif self.opcionVenderBeforeRmv.get() == 2:
                messagebox.showinfo("Info", f"Se ha eliminado el producto '{self.productoSeleccionado.nombreProducto}'")
            self.gestor.GuardarArchivo()
            self.InfoEtiquetas(100)
            self.CambiarFrame('removeFrame')
        else:
            us.showNoProductoSeleccionado()
                

    def SalirApp(self):
        self.root.destroy()

    def CargarImagen(self, ruta, size):
        '''
            Funcion para cargar una imagen, con la ruta de entrada y su tamaño en (x,y) en pixeles
            Se devolverá una instancia de la libreria PhotoImage con la ruta de la imagen ya reescalada
        '''
        imagen = Image.open(ruta)
        imagen = imagen.resize(size)
        return ImageTk.PhotoImage(imagen)
    
    def ExportarInv(self):
        rutaArchivo = fd.asksaveasfilename(
            title="Exportar Inventario en Excel",
            initialdir='.',
            defaultextension='.xlsx',
            filetypes=[
                ("Spreadsheets Files", "*.xlsx"),
                ("Excel Docs", "*.xls")
            ]
        )
        ruta = rutaArchivo

        self.gestor.ExportarExcel(ruta)

    def GenerarGrafica(self):
        fechas = []
        valores = []
        valorMaximo = 0

        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots()

        for item in self.gestor.fechasValorBruto:
            fechas.append(item['fecha'])
            valores.append(int(item['valorBruto']))
            if item['valorBruto'] > valorMaximo:
                valorMaximo = item['valorBruto']
        
        margenGrafico = (valorMaximo * 0.2) + valorMaximo
        ax.plot(fechas, valores, color='red')

        ax.set_title("Histórico Valor Bruto Relativo", fontsize=20)
        ax.set_xlabel('', fontsize=14)
        fig.autofmt_xdate()
        ax.set_ylabel("Valor bruto ( € )", fontsize=14)
        plt.ylim((-15, margenGrafico))

        plt.show()
