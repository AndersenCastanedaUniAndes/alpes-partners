import threading
import time

from alpespartners.modulos.marketing_influencers.infraestructura.consumidores import (
    suscribirse_a_comandos,
    suscribirse_a_eventos,
)


def _run(target):
    t = threading.Thread(target=target, daemon=True)
    t.start()
    return t


def main():
    # Run both consumers so we can see event flow in logs
    threads = [
        _run(suscribirse_a_comandos),
        _run(suscribirse_a_eventos),
    ]

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
