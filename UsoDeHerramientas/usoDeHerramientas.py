import json
import sys

CLIMA = {"Bogotá": 14, "Medellín": 24, "Cali": 26}


def ejecutar(nombre, entrada):

    if nombre == "calculadora":
        operacion = entrada.get("operacion")
        a = entrada.get("a")
        b = entrada.get("b")
        if operacion == "sumar":
            return str(a + b), False
        if operacion == "restar":
            return str(a - b), False
        if operacion == "multiplicar":
            return str(a * b), False
        if operacion == "dividir":
            if b == 0:
                return "error: división por cero", True
            return str(a // b), False
        return f"error: operación desconocida: {operacion}", True
    if nombre == "clima":
        ciudad = entrada.get("ciudad")
        if ciudad in CLIMA:
            return f"{CLIMA[ciudad]} °C", False
        return f"error: ciudad desconocida: {ciudad}", True
    return f"error: herramienta desconocida: {nombre}", True


def usoDeHerramientas(respuestas):

    salida = []
    llamadas = 0
    errores = 0
    for respuesta in respuestas:
        if respuesta["stop_reason"] == "tool_use":
            for bloque in respuesta["content"]:
                if bloque["type"] != "tool_use":
                    continue
                resultado, es_error = ejecutar(bloque["name"], bloque["input"])
                llamadas += 1
                errores += es_error
                salida.append(f"tool_result {bloque['id']} {resultado}")
        elif respuesta["stop_reason"] == "end_turn":
            texto = "".join(bloque["text"] for bloque in respuesta["content"] if bloque["type"] == "text")
            salida.append(f"final: {texto}")
    salida.append(f"resumen: {llamadas} llamadas, {errores} errores")
    return salida


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    respuestas = [json.loads(linea) for linea in sys.stdin if linea.strip()]
    for linea in usoDeHerramientas(respuestas):
        print(linea)

main()
