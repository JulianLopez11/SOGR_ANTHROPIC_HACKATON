import json
import sys
import unicodedata


def normalizar(texto):

    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")
    limpio = "".join(c if c.isalnum() else " " for c in sin_tildes)
    return " ".join(limpio.split())


def pasa(esperado, respuesta):

    return f" {normalizar(esperado)} " in f" {normalizar(respuesta)} "


def evaluacionEnRespuestas(casos):

    categorias = {}
    for caso in casos:
        aprobadas, total = categorias.get(caso["categoria"], (0, 0))
        categorias[caso["categoria"]] = (aprobadas + pasa(caso["esperado"], caso["respuesta"]), total + 1)
    return sorted(categorias.items())


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    casos = [json.loads(linea) for linea in sys.stdin if linea.strip()]
    resultados = evaluacionEnRespuestas(casos)
    aprobadas = 0
    for categoria, (bien, total) in resultados:
        aprobadas += bien
        print(f"{categoria}: {bien}/{total}")
    decimas = (aprobadas * 2000 + len(casos)) // (2 * len(casos))
    print(f"total: {aprobadas}/{len(casos)} ({decimas // 10}.{decimas % 10}%)")

main()
