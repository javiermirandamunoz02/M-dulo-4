class EcommerceError(Exception):
    """Clase base para excepciones del ecommerce."""
    pass

class ProductoNoEncontradoError(EcommerceError):
    """Se lanza cuando un ID de producto no existe en el catálogo."""
    pass

class CantidadInvalidaError(EcommerceError):
    """Se lanza cuando la cantidad ingresada es menor o igual a cero."""
    pass

class CarritoVacioError(EcommerceError):
    """Se lanza cuando un cliente intenta pagar un carrito sin ítems."""
    pass