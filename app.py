import sqlite3
from colorama import Fore, Style

# Conexión a la base de datos
def conectar_db():
    return sqlite3.connect('inventario.db')

# Crear tabla de productos si no existe
def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Agregar un nuevo producto
def agregar_producto():
    nombre = input(Fore.GREEN + "Ingrese el nombre del producto: " + Style.RESET_ALL)
    descripcion = input(Fore.GREEN + "Ingrese la descripción del producto: " + Style.RESET_ALL)
    
    cantidad = input(Fore.GREEN + "Ingrese la cantidad del producto: " + Style.RESET_ALL)
    while not cantidad.isdigit():
        print(Fore.RED + "Por favor, ingrese un número válido para la cantidad." + Style.RESET_ALL)
        cantidad = input(Fore.GREEN + "Ingrese la cantidad del producto: " + Style.RESET_ALL)
    cantidad = int(cantidad)

    precio = input(Fore.GREEN + "Ingrese el precio del producto: " + Style.RESET_ALL)
    while not precio.replace('.', '', 1).isdigit():
        print(Fore.RED + "Por favor, ingrese un precio válido." + Style.RESET_ALL)
        precio = input(Fore.GREEN + "Ingrese el precio del producto: " + Style.RESET_ALL)
    precio = float(precio)

    categoria = input(Fore.GREEN + "Ingrese la categoría del producto: " + Style.RESET_ALL)

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conn.commit()
    conn.close()

    print(Fore.CYAN + f"Producto '{nombre}' agregado al inventario." + Style.RESET_ALL)

# Mostrar todos los productos en el inventario
def mostrar_inventario():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    
    if not productos:
        print(Fore.RED + "No hay productos en el inventario." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Inventario actual:" + Style.RESET_ALL)
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}")
    conn.close()

# Actualizar la cantidad de un producto
def actualizar_producto():
    id_producto = input(Fore.GREEN + "Ingrese el ID del producto a actualizar: " + Style.RESET_ALL)
    while not id_producto.isdigit():
        print(Fore.RED + "Por favor, ingrese un ID válido." + Style.RESET_ALL)
        id_producto = input(Fore.GREEN + "Ingrese el ID del producto a actualizar: " + Style.RESET_ALL)
    
    nueva_cantidad = input(Fore.GREEN + "Ingrese la nueva cantidad: " + Style.RESET_ALL)
    while not nueva_cantidad.isdigit():
        print(Fore.RED + "Por favor, ingrese una cantidad válida." + Style.RESET_ALL)
        nueva_cantidad = input(Fore.GREEN + "Ingrese la nueva cantidad: " + Style.RESET_ALL)
    nueva_cantidad = int(nueva_cantidad)

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE productos SET cantidad = ? WHERE id = ?
    ''', (nueva_cantidad, id_producto))
    conn.commit()
    conn.close()

    print(Fore.CYAN + f"Cantidad del producto ID {id_producto} actualizada a {nueva_cantidad}." + Style.RESET_ALL)

# Eliminar un producto
def eliminar_producto():
    id_producto = input(Fore.GREEN + "Ingrese el ID del producto a eliminar: " + Style.RESET_ALL)
    while not id_producto.isdigit():
        print(Fore.RED + "Por favor, ingrese un ID válido." + Style.RESET_ALL)
        id_producto = input(Fore.GREEN + "Ingrese el ID del producto a eliminar: " + Style.RESET_ALL)
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM productos WHERE id = ?
    ''', (id_producto,))
    conn.commit()
    conn.close()

    print(Fore.CYAN + f"Producto ID {id_producto} eliminado del inventario." + Style.RESET_ALL)

# Buscar productos por ID, nombre o categoría
def buscar_producto():
    criterio = input(Fore.GREEN + "¿Desea buscar por ID, nombre o categoría? " + Style.RESET_ALL).lower()
    if criterio not in ['id', 'nombre', 'categoria']:
        print(Fore.RED + "No se encontraron resultados de la busqueda." + Style.RESET_ALL)
        return
    
    valor = input(Fore.GREEN + f"Ingrese el valor de búsqueda para {criterio}: " + Style.RESET_ALL)

    # Usar match() para verificar el valor de búsqueda antes de la consulta SQL
    if criterio == 'nombre' or criterio == 'categoria':
        # Match para nombre o categoría (busca coincidencias parciales en el valor)
        if match := valor.lower():  # Si el valor no es vacío o nulo, utilizamos match
            print(Fore.CYAN + f"Buscando productos cuyo {criterio} coincida con '{valor}'..." + Style.RESET_ALL)
        else:
            print(Fore.RED + "No se ha ingresado un valor válido para la búsqueda." + Style.RESET_ALL)
            return

    conn = conectar_db()
    cursor = conn.cursor()
    
    # Búsqueda en base de datos utilizando LIKE para 'nombre' o 'categoria' 
    if criterio == 'id':
        # Buscamos por ID (usamos exactamente el valor ingresado)
        cursor.execute("SELECT * FROM productos WHERE id = ?", (valor,))
    elif criterio == 'nombre':
        # Buscamos productos con nombre que coincidan parcialmente con el valor dado
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + valor + '%',))
    elif criterio == 'categoria':
        # Buscamos productos con categoría que coincidan parcialmente con el valor dado
        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + valor + '%',))
    
    productos = cursor.fetchall()
    if not productos:
        print(Fore.RED + "No se encontraron productos que coincidan con los criterios." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Resultados de búsqueda:" + Style.RESET_ALL)
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}")
    
    conn.close()


# Generar reporte de productos con bajo stock
def reporte_bajo_stock():
    limite = input(Fore.GREEN + "Ingrese el límite de stock bajo: " + Style.RESET_ALL)
    while not limite.isdigit():
        print(Fore.RED + "Por favor, ingrese un número válido para el límite." + Style.RESET_ALL)
        limite = input(Fore.GREEN + "Ingrese el límite de stock bajo: " + Style.RESET_ALL)
    limite = int(limite)

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    
    if not productos:
        print(Fore.RED + "No hay productos con bajo stock." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"Reporte de productos con stock inferior o igual a {limite}:" + Style.RESET_ALL)
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}")
    
    conn.close()

# Menú principal
def mostrar_menu():
    crear_tabla()
    
    while True:
        print(Fore.BLUE + "\nMenú de Gestión de Inventario" + Style.RESET_ALL)
        print("1. Agregar producto")
        print("2. Mostrar inventario")
        print("3. Actualizar cantidad de producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Generar reporte de bajo stock")
        print("7. Salir")
        
        opcion = input(Fore.GREEN + "Seleccione una opción (1-7): " + Style.RESET_ALL)
        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            mostrar_inventario()
        elif opcion == '3':
            actualizar_producto()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            buscar_producto()
        elif opcion == '6':
            reporte_bajo_stock()
        elif opcion == '7':
            print(Fore.CYAN + "¡Hasta luego!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, seleccione una opción del 1 al 7." + Style.RESET_ALL)

# Ejecutar el programa
if __name__ == "__main__":
    mostrar_menu()

