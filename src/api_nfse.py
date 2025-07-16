from fastapi import FastAPI
import subprocess
import uvicorn

app = FastAPI()

@app.post("/emitir_nfse")
def emitir_nfse():
    try:
        # Executa o script Python para emitir NFSe
        result = subprocess.run(['python', 'emissao_nfse.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/buscar_tomador")
def buscar_tomador():
    try:
        # Executa o script Python para buscar dados do tomador
        result = subprocess.run(['python', 'buscar_tomador.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000, log_level="info")

