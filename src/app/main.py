
from fastapi import FastAPI, UploadFile, File
from app.config import s3, BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path
from app.services import read_file, docling_convert, save_localstack


app = FastAPI(title="IABotAgent FATEC API")


@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/teste")
def teste(file: UploadFile = File(...)):
    return {"message": file.content_type}

@app.post("/upload-documento")
async def upload(file: UploadFile = File(...)):

    try:
 
        content = await read_file(file)

        if (content == False):
            return{
                "message":  "erro"
            }
        

        doc, filename = docling_convert(content)

        return{
                "message":  ""+str(doc)+" "+str(filename)+""
            }

        # save_localstack(doc, filename)

        

    except OSError:
        return{
            "message": "Erro ao fazer upload de arquivo.",
        }



# @app.get("/listar-documentos")
# def listar():
#     dados = db.get()
#     arquivos = list({m['source'] for m in dados['metadatas']}) if dados['metadatas'] else []
#     return {"documentos": arquivos}

