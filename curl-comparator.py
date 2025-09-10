import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import re

def parse_simple_curl(curl_string):
    curl_string = curl_string.replace('\\\n', ' ').replace('\n', ' ').strip()
    method_match = re.search(r"-X\s+'?(\w+)'?", curl_string)
    method = method_match.group(1) if method_match else 'GET'
    url_match = re.search(r"curl .*?'(http[s]?://.*?)'", curl_string)
    url = url_match.group(1) if url_match else None
    data_match = re.search(r"-d\s+'(.*)'|-d\s+\"(.*)\"", curl_string)
    data = data_match.group(1) if data_match and data_match.group(1) else (data_match.group(2) if data_match and data_match.group(2) else None)
    headers = {}
    for h in re.findall(r"-H\s+'(.*?):\s*(.*?)'", curl_string):
        headers[h[0]] = h[1]
    return method, url, headers, data

def compare_curls():
    curl_old = text_curl_old.get("1.0", tk.END).strip()
    curl_new = text_curl_new.get("1.0", tk.END).strip()

    try:
        method_old, url_old, headers_old, data_old = parse_simple_curl(curl_old)
        method_new, url_new, headers_new, data_new = parse_simple_curl(curl_new)
    except Exception as e:
        result_text.set(f"❌ Error al parsear cURL: {e}")
        return

    if not url_old or not url_new:
        result_text.set("❌ No se pudo detectar la URL en uno de los cURL")
        return

    try:
        resp_old = requests.request(method_old, url_old, headers=headers_old, data=data_old)
        resp_new = requests.request(method_new, url_new, headers=headers_new, data=data_new)
    except Exception as e:
        result_text.set(f"❌ Error al hacer requests: {e}")
        return

    # Convertir respuestas a JSON o texto plano
    try:
        json_old = resp_old.json()
        text_old = json.dumps(json_old, indent=2).splitlines()
    except:
        text_old = resp_old.text.splitlines()

    try:
        json_new = resp_new.json()
        text_new = json.dumps(json_new, indent=2).splitlines()
    except:
        text_new = resp_new.text.splitlines()

    # Limpiar los paneles
    text_left.delete("1.0", tk.END)
    text_right.delete("1.0", tk.END)

    # Comparar línea por línea
    max_len = max(len(text_old), len(text_new))
    for i in range(max_len):
        line_old = text_old[i] if i < len(text_old) else ''
        line_new = text_new[i] if i < len(text_new) else ''
        if line_old == line_new:
            text_left.insert(tk.END, line_old + '\n')
            text_right.insert(tk.END, line_new + '\n')
        else:
            text_left.insert(tk.END, line_old + '\n', 'diff')
            text_right.insert(tk.END, line_new + '\n', 'diff')

    # Configurar colores
    text_left.tag_config('diff', foreground='red')
    text_right.tag_config('diff', foreground='red')

    # Resultado general
    if text_old == text_new:
        result_text.set("✅ Las respuestas son idénticas")
    else:
        result_text.set("❌ Las respuestas son diferentes")

# GUI
root = tk.Tk()
root.title("Comparador Visual de Endpoints por cURL")

# cURL Inputs
tk.Label(root, text="cURL Endpoint Antiguo:").grid(row=0, column=0, sticky="w")
text_curl_old = scrolledtext.ScrolledText(root, width=80, height=5)
text_curl_old.grid(row=1, column=0, padx=5, pady=5)

tk.Label(root, text="cURL Endpoint Nuevo:").grid(row=2, column=0, sticky="w")
text_curl_new = scrolledtext.ScrolledText(root, width=80, height=5)
text_curl_new.grid(row=3, column=0, padx=5, pady=5)

tk.Button(root, text="Comparar", command=compare_curls).grid(row=4, column=0, pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, fg="blue").grid(row=5, column=0, sticky="w")

# Paneles de comparación
frame_compare = tk.Frame(root)
frame_compare.grid(row=6, column=0, padx=5, pady=5)

text_left = scrolledtext.ScrolledText(frame_compare, width=60, height=30)
text_left.grid(row=0, column=0, padx=5)

text_right = scrolledtext.ScrolledText(frame_compare, width=60, height=30)
text_right.grid(row=0, column=1, padx=5)

# Scroll sincronizado
def sync_scroll(*args):
    text_left.yview(*args)
    text_right.yview(*args)

text_left.config(yscrollcommand=sync_scroll)
text_right.config(yscrollcommand=sync_scroll)

root.mainloop()

