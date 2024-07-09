from GestorInventario.producto_script import Producto
from Utilidades import util_script as us
from pathlib import Path
import os
import json
import rute_script as rs
import xlsxwriter
import datetime as dt
from datetime import datetime as dtt

class Gestor():
    def __init__(self):
        self.productos = []
        self.fechasValorBruto = []
        self.saldoCuenta = 0
        self.valorBruto = 0

    def BuscarProductoGUI(self, id):
        '''
            Función para que se encarga de buscar un producto en la lista de productos
            Como parámetro requiere un ID tipo entero y devuelve el objeto de la lista hayado con ese ID
        '''
        if not us.listaVacia(self.productos):
            encontrado = False
            for producto in self.productos:
                if producto.id == id:
                    encontrado = True
                    us.showProductoEncontrado()
                    return producto
            if not encontrado:
                us.showProductoNotFound(id)
            return None
        else:
            us.showListaVacia()

    def AgregarProductoGUI(self, nombreProducto, cantidad, precio, rebaja = 0, estaRebajado = False):
        '''
            Función que agrega una nueva instancia de tipo Producto a la lista de productos requiriendo de varios parámetros:
                - nombreProducto (String)
                - cantidad (int)
                - precio (float)
                - rebaja (int) por defecto será 0
                - estaRebajado (bool) por defecto será False
            Se calculará el valor bruto en función del precio y la cantidad y luego se almacena el objeto a la lista de productos
        '''
        self.valorBruto += round(precio * cantidad, 2)
        self.PasarValorHistorial()
        producto = Producto(nombreProducto, cantidad, precio, precio, rebaja, estaRebajado)
        self.productos.append(producto)
        print(self.productos)

    def ActualizarProductoGUI(self, producto, nombreProducto, cantidad, precio, opcion):
        '''
            Función que actualiza un producto aportado como parámetro requiriendo de varios parámetros:
                - producto (objeto tipo Producto(nombreProducto, cantidad, precio, precioReal, rebaja, estaRebajado))
                - nombreProducto (String)
                - cantidad (int)
                - precio (float)
            Como la aplicación permite actualizar 1, 2 o 3 propiedades del producto indistintamente cualesquiera que sean, llamaremos
            por separado la funcion heredada de tipo Producto del parametro que no venga por defecto correspondiente para su actualización
            En caso de ser el precio o la cantidad, actualizaremos el valor bruto acorde a los nuevos datos insertados
        '''
        if nombreProducto != "":
            producto.ActualizarNombre(nombreProducto)
        if cantidad != None and precio != None:
            self.valorBruto -= round(producto.precio * producto.cantidad, 2)
            self.valorBruto += round(precio * cantidad, 2)
            self.PasarValorHistorial()
            producto.ActualizarCantidad(cantidad)
            producto.ActualizarPrecio(precio, opcion)
        elif precio != None and cantidad == None:
            self.valorBruto -= round(producto.precio * producto.cantidad, 2)
            self.valorBruto += round(precio * producto.cantidad, 2)
            self.PasarValorHistorial()
            producto.ActualizarPrecio(precio, opcion)
        else:
            self.valorBruto -= round(producto.precio * producto.cantidad, 2)
            self.valorBruto += round(producto.precio * cantidad, 2)
            self.PasarValorHistorial()
            producto.ActualizarCantidad(cantidad)

    def VenderProductoGUI(self, producto, cantidad):
        '''
            Funcion que gestiona la accion de vender un producto teniendo como entrada los siguientes parametros:
                - producto: valor objeto de tipo producto
                - cantidad: valor de tipo entero
            Se asignara la suma ganada por la venta al saldoCuenta y se le resta al valorBruto haciendo referencia de que ya no
            tenemos esos productos consignados en el almacén y por tanto, menor valor bruto
        '''
        self.saldoCuenta += round(cantidad * producto.precio, 2)
        self.valorBruto -= round(producto.precioReal * cantidad, 2)
        self.PasarValorHistorial()
        cantidadNueva = producto.cantidad - cantidad
        producto.ActualizarCantidad(cantidadNueva)

    def EliminarProductoGUI(self, producto, opcion):
        '''
            Función en que se elimina un producto del almacén vendiendo o sin vender su stock remanente
        '''
        eliminado = False
        if opcion == 1:
            if producto.cantidad > 0:
                self.saldoCuenta += round(producto.cantidad * producto.precio, 2)
                self.valorBruto -= round(producto.precio * producto.cantidad, 2)
                self.productos.remove(producto)
                eliminado = True
            else:
                us.showNoStockForSell(producto.nombreProducto)
        elif opcion == 2:
            self.valorBruto -= round(producto.precio * producto.cantidad, 2)
            self.productos.remove(producto)
            eliminado = True
        if eliminado:
            self.PasarValorHistorial()
            return eliminado
    
    def AbrirArchivo(self):
        archivoInventario = Path(rs.rutaSave("inventario"))
        archivoFinanzas = Path(rs.rutaSave("finanzas"))
        archivoHistorial = Path(rs.rutaSave("historial"))
        valorBrutoTemp = 0
        try:
            contenidoInventario = archivoInventario.read_text()
            contenidoFinanzas = archivoFinanzas.read_text()
            contenidoHistorial = archivoHistorial.read_text()
        except FileNotFoundError:
            self.GuardarArchivo()
        else:
            productos = json.loads(contenidoInventario)
            valores = json.loads(contenidoFinanzas)
            historiales = json.loads(contenidoHistorial)
            try:
                # Cargamos la lista de productos guardados en local a memoria
                for producto in productos:
                    productoObj = Producto(producto['nombre'], producto['cantidad'], producto['precioReal'], producto['precio'], producto['rebaja'], producto['estaRebajado'])
                    valorBrutoTemp += productoObj.precioReal * productoObj.cantidad
                    self.productos.append(productoObj)
                # Cargamos los valores financieros a memoria
                self.saldoCuenta = valores['saldoCuenta']
                self.valorBruto = valores['valorBruto']
                # Aquí calcularemos el inventario cargado y compararemos si el valor bruto cargado corresponde con este inventario
                if self.valorBruto != valorBrutoTemp:
                    self.valorBruto = valorBrutoTemp

                # Abrimos y cargamos el historial de fechas y valores brutos a memoria
                try:
                    for historial in historiales:
                        fechaActual = historial['fecha']
                        valorActual = historial['valorBruto']
                        saldoActual = historial['saldoCuenta']
                        pasoHistorial = {
                            'fecha' : fechaActual,
                            'valorBruto' : valorActual,
                            'saldoCuenta' : saldoActual
                        }
                        self.fechasValorBruto.append(pasoHistorial)
                except KeyError:
                    print("El diccionario al que se intenta acceder, se encuentra sin las keys exigidas")
            except TypeError:
                print("El archivo esta vacio, proseguimos con el programa")
    
    def PasarValorHistorial(self):
        fechaActual = dt.date.today()
        fechaCadena = fechaActual.isoformat()
        pasoHistorial = {
            'fecha' : fechaCadena,
            'valorBruto' : self.valorBruto,
            'saldoCuenta' : self.saldoCuenta
        }
        self.fechasValorBruto.append(pasoHistorial)

    def GuardarArchivo(self):
        archivoInventario = Path(rs.rutaSave("inventario"))
        archivoFinanzas = Path(rs.rutaSave("finanzas"))
        archivoHistorial = Path(rs.rutaSave("historial"))

        # Cargando los productos con la funcion de ObjToDict() que convierto explicitamente objetos a diccionarios
        productos = json.dumps(self.ObjToDict(), indent=4)
        archivoInventario.write_text(productos)

        # Creando un diccionario para guardar los valores financieros
        valores = {
            'valorBruto' : self.valorBruto,
            'saldoCuenta' : self.saldoCuenta
        }
        finanzas = json.dumps(valores, indent=4)
        archivoFinanzas.write_text(finanzas)

        # Cargando la lista de diccionarios en un json para guardarlo en su fichero local correspondiente .json
        historial = json.dumps(self.fechasValorBruto, indent=4)
        archivoHistorial.write_text(historial)

    def ObjToDict(self):
        if not us.listaVacia(self.productos):
            self.exportProductos = []
            for producto in self.productos:
                dictProducto = {
                    'id' : producto.id,
                    'nombre' : producto.nombreProducto,
                    'cantidad' : producto.cantidad,
                    'precioReal' : producto.precioReal,
                    'precio' : producto.precio,
                    'rebaja' : producto.rebaja,
                    'estaRebajado' : producto.estaRebajado
                }
                self.exportProductos.append(dictProducto)
            return self.exportProductos
        
    def ExportarExcel(self, rutaGuardado = ''):
        '''
            Funcion que sirve para poder exportar toda la información del inventario, en un archivo de hojas de calculo
            Para la ejecución correcta de esta función, requeriremos de un argumento de ruta de guardado que es una ruta de tipo Path
            con su nombre de archivo y ruta, con esta información podremos localizar y abrir el documento excel para insertar sus filas y columnas
        '''
        headersExport = ["ID", "Nombre", "Cantidad", "Precio_Real", "Precio", "Rebaja", "Esta_Rebajado"]

        # Si no se recibe una ruta de Guardado, se asignará la predefinida por la clase xlsxwriter que es en el directorio de ejecución de la aplicación
        if rutaGuardado:
            exportarEnRuta = os.path.join(rutaGuardado)
            workbook = xlsxwriter.Workbook(exportarEnRuta)
            worksheet = workbook.add_worksheet()

            for columna, header in enumerate(headersExport):
                worksheet.write(0, columna, header)

            for fila, producto in enumerate(self.productos, 1):
                worksheet.write(fila, 0, producto.id)
                worksheet.write(fila, 1, producto.nombreProducto)
                worksheet.write(fila, 2, producto.cantidad)
                worksheet.write(fila, 3, producto.precioReal)
                worksheet.write(fila, 4, producto.precio)
                worksheet.write(fila, 5, producto.rebaja)
                worksheet.write(fila, 6, producto.estaRebajado)
            workbook.close()
        else:
            us.showNoRuteSpecified()

        
    # =================================================================
    # -------------------- FUNCIONES DEPRECATED -----------------------
    # =================================================================