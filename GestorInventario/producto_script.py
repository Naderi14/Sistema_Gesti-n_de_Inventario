class Producto():
    id = 1

    def __init__(self, nombreProducto, cantidad, precioReal, precio, rebaja, estaRebajado):
        self.id = Producto.id
        Producto.id += 1
        self.nombreProducto = nombreProducto
        self.cantidad = cantidad
        self.precioReal = precioReal
        self.precio = precio
        if rebaja > 0:
            self.AplicarRebaja(rebaja)
        else:
            self.rebaja = rebaja
            self.estaRebajado = estaRebajado

    def AplicarRebaja(self, porcentaje):
        '''
            Funcion para aplicar una rebaja al producto
                - porcentaje: parametro para calcular la rebaja
        '''
        self.rebaja = porcentaje
        self.precio -= self.precio * (porcentaje / 100)
        self.precio = round(self.precio,2)
        self.estaRebajado = True

    def QuitarRebaja(self):
        '''
            Funcion para quitar una rebaja existente al producto
        '''
        self.precio = self.precioReal
        self.rebaja = 0.0
        self.estaRebajado = False

    def ActualizarNombre(self, nombreProucto):
        '''
            Funcion para actualizar el nombre del producto
                - nombreProducto: Nuevo nombre de entrada por el que sustituir
        '''
        self.nombreProducto = nombreProucto

    def ActualizarPrecio(self, precio, mantenerRebaja = False):
        '''
            Funcion para actualizar el precio del producto
                - precio: nuevo precio por el que sustituir
                - mantenerRebaja: estado en el que se gestionará mantener la rebaja con el nuevo precio, o quitar la rebaja con el nuevo precio
                    · Por defecto esta en False
        '''
        if mantenerRebaja:
            self.precioReal = precio
            self.precio = precio
            self.AplicarRebaja(self.rebaja)
        else:
            self.QuitarRebaja()
            self.precio = precio
            self.precioReal = precio

    def ActualizarCantidad(self, cantidad):
        '''
            Funcion para actualizar la cantidad del producto   
                - cantidad: nueva cantidad por el que sustituir
        '''
        self.cantidad = cantidad