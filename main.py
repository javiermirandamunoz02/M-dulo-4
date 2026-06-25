from modelos import Catalogo, Admin, Cliente
from excepciones import EcommerceError

class TiendaApplication:
    def __init__(self):
        self.catalogo = Catalogo()
        self.usuario_activo = None

    def ejecutar(self):
        print("Bienvenido/a al Sistema de Ecommerce CLI (Versión POO)")
        while True:
            print("\nSeleccione su Rol de Ingreso:")
            print("1) Administrador (ADMIN)")
            print("2) Cliente (CLIENTE)")
            print("0) Cerrar Aplicación")
            rol_opcion = input("Opción: ").strip()

            if rol_opcion == "1":
                self.usuario_activo = Admin("Administrador_Sistema")
                self.bucle_admin()
            elif rol_opcion == "2":
                self.usuario_activo = Cliente("Estudiante_Bootcamp")
                self.bucle_cliente()
            elif rol_opcion == "0":
                print("\nGracias por usar nuestra plataforma. ¡Hasta pronto!")
                break
            else:
                print("[!] Opción inválida. Intente de nuevo.")

    def imprimir_tabla_productos(self, lista_productos):
        """Método auxiliar estético para pintar los productos."""
        print(f"\n{'ID':<5} | {'Nombre':<25} | {'Categoría':<15} | {'Precio':<10}")
        print("-" * 65)
        for prod in lista_productos:
            print(f"{prod.id:<5} | {prod.nombre:<25} | {prod.categoria:<15} | ${prod.precio:>.2f}")

    # --- FLUJOS DE MENÚS CON CAPTURA DE EXCEPCIONES ---

    def bucle_admin(self):
        while True:
            print(self.usuario_activo.obtener_menu())
            opc = input("Seleccione una opción: ").strip()

            try:
                if opc == "1":
                    self.imprimir_tabla_productos(self.catalogo.listar())
                
                elif opc == "2":
                    id_p = int(input("Ingrese ID único del nuevo producto: "))
                    # Verificar duplicado antes de pedir el resto de datos
                    try:
                        self.catalogo.buscar_por_id(id_p)
                        print("[!] Error: Ya existe un producto con ese ID.")
                        continue
                    except Exception:
                        pass # Si lanza error es bueno, significa que está libre el ID
                    
                    nom = input("Nombre del producto: ").strip()
                    cat = input("Categoría: ").strip().lower()
                    pre = float(input("Precio (>0): "))
                    self.catalogo.crear(id_p, nom, cat, pre)
                    print("[✓] Producto creado y guardado con éxito.")

                elif opc == "3":
                    id_p = int(input("Ingrese el ID del producto a actualizar: "))
                    self.catalogo.buscar_por_id(id_p) # Validará existencia primero
                    nom = input("Nuevo nombre: ").strip()
                    cat = input("Nueva categoría: ").strip().lower()
                    pre = float(input("Nuevo precio (>0): "))
                    self.catalogo.actualizar(id_p, nom, cat, pre)
                    print("[✓] Producto modificado correctamente.")

                elif opc == "4":
                    id_p = int(input("Ingrese el ID del producto a eliminar: "))
                    self.catalogo.eliminar(id_p)
                    print("[✓] Producto removido del catálogo.")

                elif opc == "0":
                    break
                else:
                    print("[!] Opción no válida.")
            
            except ValueError:
                print("[Error de Tipo] Ingrese valores numéricos válidos en los campos correspondientes.")
            except EcommerceError as e:
                print(f"[Error de Negocio] {e}")
            finally:
                print("\n--- Operación procesada ---")

    def bucle_cliente(self):
        while True:
            print(self.usuario_activo.obtener_menu())
            opc = input("Seleccione una opción: ").strip()

            try:
                if opc == "1":
                    self.imprimir_tabla_productos(self.catalogo.listar())
                
                elif opc == "2":
                    busqueda = input("Ingrese término de búsqueda (nombre o categoría): ").strip().lower()
                    filtrados = [p for p in self.catalogo.listar() if busqueda in p.nombre.lower() or busqueda in p.categoria.lower()]
                    if not filtrados:
                        print(f"[i] No se encontraron resultados para '{busqueda}'.")
                    else:
                        self.imprimir_tabla_productos(filtrados)

                elif opc == "3":
                    id_p = int(input("Ingrese el ID del producto que desea comprar: "))
                    cant = int(input("Ingrese la cantidad (>0): "))
                    self.usuario_activo.carrito.agregar(self.catalogo, id_p, cant)
                    print("[✓] Agregado al carrito.")

                elif opc == "4":
                    carro = self.usuario_activo.carrito
                    if not carro.items:
                        print("\n[i] Tu carrito está vacío.")
                        continue
                    
                    print(f"\n--- DETALLE DE TU CARRITO ---")
                    print(f"{'Nombre':<25} | {'Cantidad':<8} | {'Precio U.':<10} | {'Subtotal':<10}")
                    print("-" * 62)
                    for id_p, cant in carro.items.items():
                        prod = self.catalogo.buscar_por_id(id_p)
                        sub = prod.precio * cant
                        print(f"{prod.nombre:<25} | {cant:<8} | ${prod.precio:<9.2f} | ${sub:.2f}")
                    print("-" * 62)
                    print(f"{'TOTAL ACUMULADO:':>48} ${carro.calcular_total(self.catalogo):.2f}")

                elif opc == "5":
                    self.usuario_activo.carrito.vaciar()
                    print("[✓] Carrito vaciado.")

                elif opc == "6":
                    self.usuario_activo.confirmar_compra(self.catalogo)

                elif opc == "0":
                    break
                else:
                    print("[!] Opción no válida.")

            except ValueError:
                print("[Error de Tipo] Entrada inválida. Asegúrese de escribir números enteros para IDs y cantidades.")
            except EcommerceError as e:
                print(f"[Error de Negocio] {e}")
            finally:
                print("\n--- Operación procesada ---")


if __name__ == "__main__":
    app = TiendaApplication()
    app.ejecutar()