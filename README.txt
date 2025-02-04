Gestión de Inventario con SQLite

Este proyecto permite gestionar un inventario de productos mediante una interfaz de línea de comandos. 
La aplicación utiliza SQLite como base de datos para almacenar la información y colorama para mejorar la experiencia visual en la consola.

Funcionalidades

Conexión a la Base de Datos
La aplicación establece una conexión con una base de datos SQLite llamada inventario.db. Si la base de datos no existe, se crea automáticamente.

Creación de Tabla de Productos
Si la tabla productos no existe, se crea. Esta tabla almacena la información de cada producto, incluyendo:
id: Identificador único del producto (autoincrementable).
nombre: Nombre del producto.
descripción: Descripción del producto.
cantidad: Cantidad disponible del producto.
precio: Precio del producto.
categoria: Categoría a la que pertenece el producto.

Agregar un Producto
Permite ingresar los detalles de un nuevo producto, como el nombre, descripción, cantidad, precio y categoría. Una vez ingresados, el producto se guarda en la base de datos.

Mostrar Inventario
Muestra todos los productos almacenados en la base de datos. Si no hay productos, se muestra un mensaje indicando que el inventario está vacío.

Actualizar Cantidad de un Producto
Permite actualizar la cantidad de un producto existente en el inventario. Se solicita el ID del producto y la nueva cantidad. Si el ID no existe o la cantidad ingresada no es válida, 
se muestra un mensaje de error.

Eliminar un Producto
Permite eliminar un producto del inventario. Se solicita el ID del producto a eliminar. Si el ID no es válido, se muestra un mensaje de error.

Buscar Producto
Permite buscar productos por ID, nombre o categoría. Los resultados que coincidan con el criterio de búsqueda proporcionado son mostrados.

Generar Reporte de Productos con Bajo Stock
Solicita un valor límite para definir el "bajo stock". Muestra los productos cuyo stock (cantidad) sea igual o menor que el límite establecido.

Menú Principal
Al ejecutar el programa, se presenta un menú interactivo con las siguientes opciones:
Agregar producto: Permite agregar un nuevo producto al inventario.
Mostrar inventario: Muestra todos los productos actualmente registrados en el inventario.
Actualizar cantidad de producto: Permite modificar la cantidad de un producto existente.
Eliminar producto: Elimina un producto del inventario.
Buscar producto: Permite buscar productos por ID, nombre o categoría.
Generar reporte de bajo stock: Muestra un reporte de los productos que tienen una cantidad inferior o igual al límite ingresado.
Salir: Finaliza la aplicación.

Consideraciones
La aplicación maneja entradas de usuario mediante la función input(), validando que las cantidades y precios sean números válidos.
Los mensajes de interacción están coloreados para mejorar la experiencia del usuario:
Verde para solicitudes de entrada.
Rojo para mensajes de error.
Azul para el menú y opciones principales.
Cyan para mensajes de confirmación.

Dependencias
Este proyecto utiliza la librería colorama para mejorar la experiencia visual en la consola.