import json
import sys

ENTRADA = 300
ESCRITURA_CACHE = 375
LECTURA_CACHE = 30
SALIDA = 1500


def formatear(centesimas):

    millonesimas = (centesimas + 50) // 100
    return f"${millonesimas // 1000000}.{millonesimas % 1000000:06d}"


def costosConCacheDePrompts(usos):

    costos = []
    sin_cache = 0
    aciertos = 0
    for uso in usos:
        entrada = uso.get("input_tokens", 0)
        escritura = uso.get("cache_creation_input_tokens", 0)
        lectura = uso.get("cache_read_input_tokens", 0)
        salida = uso.get("output_tokens", 0)
        costos.append(entrada * ENTRADA + escritura * ESCRITURA_CACHE + lectura * LECTURA_CACHE + salida * SALIDA)
        sin_cache += (entrada + escritura + lectura) * ENTRADA + salida * SALIDA
        if lectura > 0:
            aciertos += 1
    return costos, sum(costos), sin_cache, aciertos


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    usos = [json.loads(linea) for linea in sys.stdin if linea.strip()]
    costos, total, sin_cache, aciertos = costosConCacheDePrompts(usos)
    for i, costo in enumerate(costos, 1):
        print(f"solicitud {i}: {formatear(costo)}")
    print(f"total: {formatear(total)}")
    print(f"sin_cache: {formatear(sin_cache)}")
    print(f"ahorro: {formatear(sin_cache - total)}")
    print(f"aciertos_de_cache: {aciertos}/{len(usos)}")

main()
