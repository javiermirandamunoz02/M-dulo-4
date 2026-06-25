# E-commerce CLI — Versión POO, Roles y Persistencia

## Descripción del Proyecto
Este proyecto es una reestructuración robusta de la aplicación de tienda virtual en consola. Se migró el paradigma imperativo estructural del Módulo 3 hacia el paradigma de **Programación Orientada a Objetos (POO)**. Incorpora separación de responsabilidades mediante roles funcionales (ADMIN y CLIENTE) y cuenta con persistencia básica en archivos de texto plano para simular transacciones operativas.

## Conceptos Avanzados de POO Aplicados
1. **Composición:** La clase `Catalogo` compone y coordina instancias de objetos `Producto`. Si el catálogo se destruye en memoria, las referencias a dichos productos dejan de persistir en ese ciclo de ejecución.
2. **Herencia:** Las clases `Admin` y `Cliente` extienden el comportamiento base de la clase abstracta conceptual `Usuario`, compartiendo la propiedad `username` pero implementando menús e interacciones polimórficas totalmente separadas.
3. **Encapsulación y Control de Errores:** Centralización del control de flujo mediante excepciones personalizadas (`excepciones.py`) para evitar la inyección de números negativos o llamadas a IDs de productos corruptos o inexistentes.
4. **Persistencia en Disco:** Escritura en flujo síncrono (`with open`) para el guardado automático de cambios en el inventario (`catalogo.txt`) y la impresión de recibos de caja tradicionales (`ordenes.txt`).

## Instrucciones de Ejecución
Asegúrese de tener los archivos `excepciones.py`, `modelos.py` y `main.py` ubicados exactamente en la misma carpeta o directorio de trabajo.

Ejecute la aplicación desde su consola o terminal preferida mediante el siguiente comando:
```bash
python main.py
