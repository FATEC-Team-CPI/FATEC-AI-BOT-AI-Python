
from fastapi import FastAPI, UploadFile, File
from config import s3,BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path
from services import read_file, docling_convert, save_localstack

app = FastAPI(title="IABotAgent FATEC API")


@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/upload-documentos")
async def upload(file: UploadFile = File(...)):

    try:
        content = read_file(file)
        doc, filename = docling_convert(content)
        save_localstack(doc, filename)

        return{
            "message":  doc.filename + "salvo com sucesso",
        }

    except OSError:
        return{
            "message": "Erro ao fazer upload de arquivo.",
        }



@app.get("/listar-documentos")
def listar():
    dados = db.get()
    arquivos = list({m['source'] for m in dados['metadatas']}) if dados['metadatas'] else []
    return {"documentos": arquivos}

