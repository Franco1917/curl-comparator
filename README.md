# curl-comparator

# Comparador Visual de Endpoints por cURL

Este proyecto es una herramienta en **Python** con interfaz gráfica que permite comparar **respuestas de dos endpoints** a partir de sus cURL.  
Es ideal para **documentar migraciones de APIs** y validar que un endpoint antiguo y uno nuevo devuelvan resultados equivalentes.

---


Ejemplo comparando dos endpoints:

<img width="1057" height="921" alt="Captura desde 2025-09-10 16-09-26" src="https://github.com/user-attachments/assets/9d418536-f16f-43bd-afbc-624b8e170e3f" />

- **Panel izquierdo:** respuesta del endpoint antiguo  
- **Panel derecho:** respuesta del endpoint nuevo  
- Diferencias resaltadas en **rojo**  

---

## ✨ Características

- Permite pegar **cURL completos** de los endpoints antiguo y nuevo.  
- Soporta **cURL con saltos de línea, comillas simples/dobles, headers y body JSON**.  
- Muestra las respuestas en **paneles lado a lado**.  
- **Resalta diferencias** en rojo para ver rápidamente discrepancias.  
- Scroll sincronizado para comparar línea por línea.  

---

## 📦 Requisitos

- Python 3.8 o superior  
- Librerías Python:

```bash
pip install requests



USO : -python3 curl-comparator.py
      -python curl-comparator.py
