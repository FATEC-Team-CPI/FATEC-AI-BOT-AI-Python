from fastapi import UploadFile, File
from app.config import s3, BUCKET_NAME
from docling.document_converter import DocumentConverter
from pathlib import Path


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


