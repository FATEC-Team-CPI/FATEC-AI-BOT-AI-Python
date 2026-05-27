from fastapi import UploadFile
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import db, s3, BUCKET_NAME
import io
import os
import logging
import tempfile

logger = logging.getLogger(__name__)

# Definido uma vez, reutilizado em toda a aplicação
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

ALLOWED_TYPES = ["application/pdf", "text/plain"]
MAX_FILE_SIZE = 32 * 1024 * 1024  # 32 MB


# --- Validação ---
async def read_file(file: UploadFile) -> bool:
    """Valida tipo e tamanho do arquivo."""
    try:
        if file.content_type not in ALLOWED_TYPES:
            logger.warning("Tipo não permitido: %s", file.content_type)
            return False
        if file.size > MAX_FILE_SIZE:
            logger.warning("Arquivo muito grande: %s bytes", file.size)
            return False
        return True
    except Exception as e:
        logger.exception("Erro ao validar arquivo: %s", e)
        return False


# --- Conversão com Docling ---
def docling_convert(file: UploadFile) -> tuple[io.BytesIO, str] | tuple[None, None]:
    """
    Salva o arquivo temporariamente em disco e converte para Markdown via Docling.
    O Docling espera um caminho de arquivo, não um objeto UploadFile.
    """
    tmp_path = None
    try:
        filename = file.filename.replace(" ", "_").lower()
        suffix = os.path.splitext(filename)[-1] or ".pdf"

        # Salva temporariamente para o Docling conseguir ler
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            tmp.write(file.file.read())

        converter = DocumentConverter()
        doc = converter.convert(tmp_path).document
        conteudo = doc.export_to_markdown()
        file_md = io.BytesIO(conteudo.encode("utf-8"))

        return file_md, filename

    except Exception as e:
        logger.exception("Erro ao converter documento: %s", e)
        return None, None

    finally:
        # Garante remoção do arquivo temporário mesmo em caso de erro
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# --- Chunking + Embedding + Armazenamento ---
def convert_data_and_store(file_md: io.BytesIO, filename: str) -> bool:
    """Divide o documento em chunks, gera embeddings e armazena no banco vetorial."""
    try:
        file_md.seek(0)
        texto = file_md.read().decode("utf-8")
        chunks = text_splitter.split_text(texto)

        if not chunks:
            logger.warning("Nenhum chunk gerado para: %s", filename)
            return False

        db.add_texts(
            texts=chunks,
            metadatas=[{"source": filename}] * len(chunks)
        )
        logger.info("%d chunks armazenados para '%s'", len(chunks), filename)
        return True

    except Exception as e:
        logger.exception("Erro ao armazenar chunks: %s", e)
        return False

