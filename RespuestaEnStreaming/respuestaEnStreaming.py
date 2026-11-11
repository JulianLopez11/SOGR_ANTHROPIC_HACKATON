import json
import sys


def respuestaEnStreaming(lineas):

    resultados = []
    bloques = {}
    stop_reason = None
    input_tokens = 0
    output_tokens = 0
    for linea in lineas:
        linea = linea.strip()
        if not linea.startswith("data:"):
            continue
        dato = json.loads(linea[5:])
        tipo = dato["type"]
        if tipo == "message_start":
            bloques = {}
            stop_reason = None
            input_tokens = dato["message"]["usage"]["input_tokens"]
            output_tokens = dato["message"]["usage"].get("output_tokens", 0)
        elif tipo == "content_block_start":
            bloques[dato["index"]] = dato["content_block"].get("text", "")
        elif tipo == "content_block_delta":
            if dato["delta"]["type"] == "text_delta":
                bloques[dato["index"]] = bloques.get(dato["index"], "") + dato["delta"]["text"]
        elif tipo == "message_delta":
            stop_reason = dato["delta"]["stop_reason"]
            output_tokens = dato["usage"]["output_tokens"]
        elif tipo == "message_stop":
            texto = "".join(bloques[indice] for indice in sorted(bloques))
            resultados.append((texto, stop_reason, input_tokens, output_tokens))
    return resultados


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for texto, stop_reason, input_tokens, output_tokens in respuestaEnStreaming(sys.stdin):
        print(f"texto: {texto}")
        print(f"stop_reason: {stop_reason}")
        print(f"input_tokens: {input_tokens}")
        print(f"output_tokens: {output_tokens}")

main()
