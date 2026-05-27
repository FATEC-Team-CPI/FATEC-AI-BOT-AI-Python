from fastapi import UploadFile, File
from app.config import s3, BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path
import io
import boto3
import os
import shutil
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import db


"""
Serviços de coleta, formatação e armazenamento dos documentos
    get documento
    docling
    banco vetorial
"""

async def read_file(file: UploadFile):
    """
    Coleta arquivo e verifica tipo e tamanho
    """
    
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
    """
    Converte documento em Marckdown
    """
        
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
        
def convert_data_and_store(file_md, filename):
    """
    Converte documento em chunk, depois embadding e armazena no DB 
    """

    file_md.seek(0)
    chunks = text_splitter.split_text(file_md)

    #EMBADDING

    db.add_texts(texts=chunks, metadatas=[{"source": filename}] * len(chunks))



def search_localstack(file_md: io.BytesIO, filename):
    """
    Procura documento no localstack
    """

    return{
        "message": "Erro ao salvar arquivo no localstack.",
    }

def set_data_localstack(file_md: io.BytesIO, filename):
    """
    Atualiza metadados do documento no localstack
    """

    return{
        "message": "Erro ao salvar arquivo no localstack.",
    }



