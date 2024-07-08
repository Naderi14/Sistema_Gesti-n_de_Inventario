from GestorInventario.producto_script import Producto
from Utilidades import util_script as us
from pathlib import Path
import os
import json
import rute_script as rs
import xlsxwriter

class Gestor():
    headersExport = ["ID", "Nombre", "Cantidad", "Precio_Real", "Precio", "Rebaja", "Esta_Rebajado"]
    saldoCuenta = 0.0
    valorBruto = 0.0

    def __init__(self):
        self.productos = []

    def BuscarProductoGUI(self, id):
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
        self.valorBruto += round(precio * cantidad,2)
        producto = Producto(nombreProducto, cantidad, precio, precio, rebaja, estaRebajado)
        self.productos.append(producto)
        print(self.productos)

    def ActualizarProductoGUI(self, producto, nombreProducto, cantidad, precio):
        if nombreProducto != "":
            producto.ActualizarNombre(nombreProducto)
        if cantidad != None:
            producto.ActualizarCantidad(cantidad)
        if precio != None:
            self.valorBruto -= producto.precio * producto.cantidad
            self.valorBruto += round(precio * producto.cantidad,2)
            producto.ActualizarPrecio(precio)

    def VenderProductoGUI(self, producto, cantidad):
        self.saldoCuenta += cantidad * producto.precio
        self.valorBruto -= round(producto.precioReal * cantidad,2)
        cantidadNueva = producto.cantidad - cantidad
        producto.ActualizarCantidad(cantidadNueva)

    def EliminarProductoGUI(self, producto, opcion):
        if opcion == 1:
            self.saldoCuenta += producto.cantidad * producto.precio
            self.valorBruto -= round(producto.precio * producto.cantidad,2)
            self.productos.remove(producto)
        elif opcion == 2:
            self.valorBruto -= round(producto.precio * producto.cantidad,2)
            self.productos.remove(producto)
    
    def AbrirArchivo(self):
        archivoInventario = Path(rs.rutaSave("inventario"))
        archivoFinanzas = Path(rs.rutaSave("finanzas"))
        valorBrutoTemp = 0
        try:
            contenidoInventario = archivoInventario.read_text()
            contenidoFinanzas = archivoFinanzas.read_text()
        except FileNotFoundError:
            self.GuardarArchivo()
        else:
            productos = json.loads(contenidoInventario)
            valores = json.loads(contenidoFinanzas)
            try:
                for producto in productos:
                    productoObj = Producto(producto['nombre'], producto['cantidad'], producto['precioReal'], producto['precio'], producto['rebaja'], producto['estaRebajado'])
                    valorBrutoTemp += productoObj.precioReal * productoObj.cantidad
                    self.productos.append(productoObj)
                self.saldoCuenta = valores['saldoCuenta']
                self.valorBruto = valores['valorBruto']
                # Aquí calcularemos el inventario cargado y compararemos si el valor bruto cargado corresponde con este inventario
                if self.valorBruto != valorBrutoTemp:
                    self.valorBruto = valorBrutoTemp
                #print("Valor Bruto: ",self.valorBruto, "\nValor Bruto Temporal: ", valorBrutoTemp)                  
            except TypeError:
                print("El archivo esta vacio, proseguimos con el programa")

    def GuardarArchivo(self):
        archivoInventario = Path(rs.rutaSave("inventario"))
        archivoFinanzas = Path(rs.rutaSave("finanzas"))

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
        # Si no se recibe una ruta de Guardado, se asignará la predefinida por la clase xlsxwriter que es en el directorio de ejecución de la aplicación
        if rutaGuardado:
            exportarEnRuta = os.path.join(rutaGuardado)
            workbook = xlsxwriter.Workbook(exportarEnRuta)
            worksheet = workbook.add_worksheet()

            for columna, header in enumerate(self.headersExport):
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