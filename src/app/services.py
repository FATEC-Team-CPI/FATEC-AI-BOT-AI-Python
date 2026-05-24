from fastapi import UploadFile, File
from app.config import s3, BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path
import os

async def read_file(file: UploadFile = File(...)):
    
    allowTypeDocument = [".pdf",".txt"]

    try:
        content = await file.read()

        if(content.suffix not in allowTypeDocument):
            return{
                "message": "Erro ao ler arquivo, o formato do arquivo não é compatível.",
            }
        
        if(os.path.getsize(content) > 31457280):
            return{
                "message": "Erro ao ler arquivo pois ele é maior que 30 MB.",
            }

        return content
        
    except:
        return{
            "message": "Erro ao ler arquivo, verifique se o formato do arquivo é compatível.",
        }
        
    


def docling_convert(content):

    try:
        converter = DocumentConverter()
        doc = converter.convert(content).document

        Path("documento.md").write_text(doc.export_to_markdown())

        filename = (str(content.filename)).replace(" ","").lower()

        with open(filename, 'w',encoding="utf-8") as doc:
            doc.write(doc.export_to_markdown())

        return doc, filename
    
    except:
        return{
            "message": "Erro ao converter arquivo.",
        }


def save_localstack(doc, filename):

    try:

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key= filename,
            Body=doc
        )

    except:
        return{
            "message": "Erro ao salvar arquivo no localstack.",
        }


