from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Servicio de gráficos funcionando 🎨"}

@app.post("/grafico")
async def generar_grafico(request: Request):
    body = await request.json()
    x = body.get("x", [])
    y = body.get("y", [])
    titulo = body.get("titulo", "Gráfico generado")
    tipo = body.get("tipo", "lineas")

    if not x or not y:
        return {"error": "Debes enviar listas 'x' y 'y'"}

    fig, ax = plt.subplots()

    if tipo == "barras":
        ax.bar(x, y)
    else:
        ax.plot(x, y, marker='o')

    ax.set_title(titulo)
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")