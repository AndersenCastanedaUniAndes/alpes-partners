#!/usr/bin/env python3
"""
Script para ejecutar los consumidores de eventos de tracking
"""
import asyncio
import threading
from consumidores import ConsumidorComandos


def main():
    consumidor = ConsumidorComandos()
    
    # Ejecutar consumidores en hilos separados
    thread_impresiones = threading.Thread(
        target=consumidor.suscribirse_a_comandos_impresion
    )
    thread_conversiones = threading.Thread(
        target=consumidor.suscribirse_a_comandos_conversion
    )
    
    thread_impresiones.start()
    thread_conversiones.start()
    
    try:
        thread_impresiones.join()
        thread_conversiones.join()
    except KeyboardInterrupt:
        print("Deteniendo consumidores...")
        consumidor.cerrar()


if __name__ == "__main__":
    main()
