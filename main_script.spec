# main_script.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_script.pyw'],
    pathex=['C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI'],
    binaries=[],
    datas=[
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Saved\\finanzas.json', 'Saved'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Saved\\inventario.json', 'Saved'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\addItem.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\removeItem.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\updateItem.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\sellItem.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\rebajaItem.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\showInventario.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\return.png', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\logoVentana.ico', 'Resources'),
        ('C:\\Users\\Fran\\Desktop\\Sistema_de_Gestion_de_Inventario\\SGI_Project_GUI\\Resources\\terminosCondiciones.txt', 'Resources')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main_script',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main_script'
)