import os

def rutaAdjunto(archivo):
    # Rutas para imagenes de la aplicación
    directorioScript = os.path.dirname(os.path.abspath(__file__))
    rutasRelativas = {
        'addItem' : "Resources/addItem.png",
        'removeItem' : "Resources/removeItem.png",
        'updateItem' : "Resources/updateItem.png",
        'sellItem' : "Resources/sellItem.png",
        'rebajaItem' : "Resources/rebajaItem.png",
        'showInventario' : "Resources/showInventario.png",
        'return' : "Resources/return.png",
        'icono' : "Resources/logoVentana.ico",
        'terminos' : "Resources/terminosCondiciones.txt",
        'finanzas' : 'Saved/finanzas.json',
        'inventario' : 'Saved/inventario.json',
        'historial' : 'Saved/historial.json'
    }
    if archivo in rutasRelativas:
        rutaAbsoluta = os.path.join(directorioScript, rutasRelativas[archivo])
        return rutaAbsoluta
    else:
        raise ValueError(f"No se ha podido obtener la ruta de la imagen {archivo} en las rutas predefinidas")