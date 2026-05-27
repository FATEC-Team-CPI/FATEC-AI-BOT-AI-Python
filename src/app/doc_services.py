from fastapi import UploadFile, File
from app.config import s3, BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path
import io
import boto3

"""
Serviços de coleta, formatação e armazenamento dos documentos
    get documento
    docling
    banco vetorial
"""


s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",  
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)


async def read_file(file: UploadFile):
    
    allowTypeDocument = ["application/pdf", "text/plain"]
    
    try:
        if file.content_type not in allowTypeDocument:
            return False
        
        if file.size > 31457280:
            # 32 MB
            return False
        
        return True

    except:
        return False
        
    
def docling_convert(file):
    try:
        converter = DocumentConverter()
        filename = (str(file.filename)).replace(" ", "_").lower()
        doc = converter.convert(file).document
        
        conteudo = doc.export_to_markdown()
        file_md = io.BytesIO(conteudo.encode("utf-8"))
        
        
        return file_md, filename
    except Exception as e:
        print(e)
        return None, None
        
        
def printa(file_md: io.BytesIO):
    file_md.seek(0)
    print(file_md.read().decode("utf-8"))


def search_localstack(file_md: io.BytesIO, filename):

    return{
        "message": "Erro ao salvar arquivo no localstack.",
    }


