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
        self.rebaja = porcentaje
        self.precio -= self.precio * (porcentaje / 100)
        self.precio = round(self.precio,2)
        self.estaRebajado = True

    def QuitarRebaja(self):
        self.precio = self.precioReal
        self.rebaja = 0.0
        self.estaRebajado = False

    def ActualizarNombre(self, nombreProucto):
        self.nombreProducto = nombreProucto

    def ActualizarPrecio(self, precio, mantenerRebaja = False):
        if mantenerRebaja:
            self.precioReal = precio
            self.precio = precio
            self.AplicarRebaja(self.rebaja)
        else:
            self.QuitarRebaja()
            self.precio = precio
            self.precioReal = precio

    def ActualizarCantidad(self, cantidad):
        self.cantidad = cantidad

    def __str__(self):
        if self.estaRebajado:
            return f"#{self.id} | Producto: {self.nombreProducto} | Precio: {self.precioReal}€ - {self.rebaja}% = {self.precio}€ | Total: {self.precio * self.cantidad}€ | Cantidad: {self.cantidad} unidades"
        else:
            return f"#{self.id} | Producto: {self.nombreProducto} | Precio: {self.precio}€/u | Total: {round(self.precio * self.cantidad,2)}€ | Cantidad: {self.cantidad} unidades"