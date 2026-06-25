import os
from datetime import datetime
from excepciones import ProductoNoEncontradoError, CantidadInvalidaError, CarritoVacioError

class Producto:
    def __init__(self, id_prod, nombre, categoria, precio):
        self.id = id_prod
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    def to_line(self):
        """Convierte el objeto a una línea de texto para el archivo."""
        return f"{self.id},{self.nombre},{self.categoria},{self.precio}\n"


class Catalogo:
    def __init__(self, archivo_ruta="catalogo.txt"):
        self.archivo_ruta = archivo_ruta
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Lee el catálogo desde el archivo de texto si existe."""
        if not os.path.exists(self.archivo_ruta):
            # Catálogo inicial por defecto si el archivo no existe
            self.productos = {
                1: Producto(1, "Camiseta Algodón", "ropa", 19.90),
                2: Producto(2, "Pantalón Jean", "ropa", 39.99),
                3: Producto(3, "Audífonos Bluetooth", "tecnologia", 59.50),
                4: Producto(4, "Teclado Mecánico", "tecnologia", 85.00),
                5: Producto(5, "Lámpara de Escritorio", "hogar", 25.00)
            }
            self.guardar_en_archivo()
            return

        try:
            with open(self.archivo_ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        id_p, nom, cat, pre = linea.strip().split(",")
                        self.productos[int(id_p)] = Producto(int(id_p), nom, cat, float(pre))
        except (IOError, ValueError):
            print("[!] Error crítico al leer el archivo de catálogo. Usando datos vacíos.")

    def guardar_en_archivo(self):
        """Escribe el estado actual del catálogo en el archivo de texto."""
        try:
            with open(self.archivo_ruta, "w", encoding="utf-8") as f:
                for prod in self.productos.values():
                    f.write(prod.to_line())
        except IOError:
            print("[!] Error: No se pudo escribir en el archivo de catálogo.")

    def listar(self):
        return list(self.productos.values())

    def buscar_por_id(self, id_prod):
        if id_prod not in self.productos:
            raise ProductoNoEncontradoError(f"El producto con ID {id_prod} no existe.")
        return self.productos[id_prod]

    def crear(self, id_prod, nombre, categoria, precio):
        if precio <= 0:
            raise CantidadInvalidaError("El precio debe ser mayor a 0.")
        self.productos[id_prod] = Producto(id_prod, nombre, categoria, precio)
        self.guardar_en_archivo()

    def actualizar(self, id_prod, nombre, categoria, precio):
        prod = self.buscar_por_id(id_prod)
        if precio <= 0:
            raise CantidadInvalidaError("El precio debe ser mayor a 0.")
        prod.nombre = nombre
        prod.categoria = categoria
        prod.precio = precio
        self.guardar_en_archivo()

    def eliminar(self, id_prod):
        self.buscar_por_id(id_prod)  # Valida si existe
        del self.productos[id_prod]
        self.guardar_en_archivo()


class Carrito:
    def __init__(self):
        self.items = {}  # Estructura: {id_producto: cantidad}

    def agregar(self, catalogo, id_prod, cantidad):
        if cantidad <= 0:
            raise CantidadInvalidaError("La cantidad a agregar debe ser mayor a cero.")
        
        # Validar existencia en catálogo llamando a su método
        catalogo.buscar_por_id(id_prod)
        
        if id_prod in self.items:
            self.items[id_prod] += cantidad
        else:
            self.items[id_prod] = cantidad

    def calcular_total(self, catalogo):
        total = 0.0
        for id_prod, cant in self.items.items():
            prod = catalogo.buscar_por_id(id_prod)
            total += prod.precio * cant
        return total

    def vaciar(self):
        self.items.clear()


# --- JERARQUÍA DE USUARIOS (HERENCIA) ---

class Usuario:
    def __init__(self, username):
        self.username = username

    def obtener_menu(self):
        raise NotImplementedError("Cada rol debe implementar su propio menú.")


class Admin(Usuario):
    def obtener_menu(self):
        return """
--- MENÚ ADMINISTRADOR ---
1) Listar productos del catálogo
2) Crear producto nuevo
3) Actualizar producto existente
4) Eliminar producto del catálogo
0) Cambiar de Rol / Salir
"""


class Cliente(Usuario):
    def __init__(self, username):
        super().__init__(username)
        self.carrito = Carrito()

    def obtener_menu(self):
        return """
--- MENÚ CLIENTE ---
1) Ver catálogo de productos
2) Buscar producto por nombre o categoría
3) Agregar producto al carrito
4) Ver carrito y total
5) Vaciar carrito
6) Confirmar compra (Pagar)
0) Cambiar de Rol / Salir
"""

    def confirmar_compra(self, catalogo, archivo_ordenes="ordenes.txt"):
        if not self.carrito.items:
            raise CarritoVacioError("No puedes confirmar la compra porque el carrito está vacío.")

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = self.carrito.calcular_total(catalogo)

        try:
            with open(archivo_ordenes, "a", encoding="utf-8") as f:
                f.write(f"=== ORDEN DE COMPRA - {ahora} ===\n")
                f.write(f"Cliente: {self.username}\n")
                f.write("Productos:\n")
                for id_prod, cant in self.carrito.items.items():
                    prod = catalogo.buscar_por_id(id_prod)
                    subtotal = prod.precio * cant
                    f.write(f" - [{id_prod}] {prod.nombre} x{cant} | Unitario: ${prod.precio:.2f} | Subtotal: ${subtotal:.2f}\n")
                f.write(f"TOTAL PAGADO: ${total:.2f}\n")
                f.write("=" * 40 + "\n\n")
            
            self.carrito.vaciar()
            print("[✓] ¡Compra procesada y registrada en 'ordenes.txt' con éxito!")
        except IOError:
            print("[!] Error crítico del sistema: No se pudo registrar la orden en el archivo.")