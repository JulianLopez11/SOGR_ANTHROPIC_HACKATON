import sys

CAPACIDAD_SOLICITUDES = 3
RECARGA_SOLICITUDES = 1
CAPACIDAD_TOKENS = 100
RECARGA_TOKENS = 20


def esperar(falta, recarga):

    if falta <= 0:
        return 0
    return -(-falta // recarga)


def limitesDeVelocidad(peticiones):

    solicitudes = CAPACIDAD_SOLICITUDES
    tokens = CAPACIDAD_TOKENS
    anterior = 0
    respuestas = []
    for tiempo, nuevos, de_cache in peticiones:
        transcurrido = tiempo - anterior
        anterior = tiempo
        solicitudes = min(CAPACIDAD_SOLICITUDES, solicitudes + transcurrido * RECARGA_SOLICITUDES)
        tokens = min(CAPACIDAD_TOKENS, tokens + transcurrido * RECARGA_TOKENS)
        if solicitudes >= 1 and tokens >= nuevos:
            solicitudes -= 1
            tokens -= nuevos
            respuestas.append("ok")
        else:
            espera = max(esperar(1 - solicitudes, RECARGA_SOLICITUDES), esperar(nuevos - tokens, RECARGA_TOKENS))
            respuestas.append(f"429 retry-after={espera}")
    return respuestas


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    peticiones = []
    for linea in sys.stdin:
        partes = linea.split()
        if partes and partes[0] == "REQUEST":
            peticiones.append(tuple(map(int, partes[1:4])))
    for respuesta in limitesDeVelocidad(peticiones):
        print(respuesta)

main()
