import logging
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.app.doc_services import (
    read_file,
    docling_convert,
    convert_data_and_store,
    save_localstack,
    search_localstack,
)

logger = logging.getLogger(__name__)

# Executor compartilhado para funções síncronas pesadas
executor = ThreadPoolExecutor(max_workers=4)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando IABotAgent FATEC API...")
    yield
    executor.shutdown(wait=True)
    logger.info("API encerrada.")


app = FastAPI(title="IABotAgent FATEC API", lifespan=lifespan)


# --- Response Models ---
class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_armazenados: bool


class DocumentoExisteResponse(BaseModel):
    filename: str
    exists: bool


# --- Helpers ---
async def _run(func, *args):
    """Roda função síncrona em thread para não bloquear o event loop."""
    from asyncio import get_event_loop
    return await get_event_loop().run_in_executor(executor, func, *args)


# --- Rotas ---
@app.post("/upload-documento", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    # 1. Valida tipo e tamanho
    if not await read_file(file):
        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido. Envie um PDF ou TXT de até 32 MB."
        )

    # 2. Converte para Markdown via Docling
    file_md, filename = await _run(docling_convert, file)
    if file_md is None:
        raise HTTPException(
            status_code=422,
            detail="Falha ao processar o documento. Verifique se o arquivo não está corrompido."
        )

    # 3. Gera chunks, embeddings e armazena no banco vetorial
    stored = await _run(convert_data_and_store, file_md, filename)

    return UploadResponse(
        message="Upload realizado com sucesso.",
        filename=filename,
        chunks_armazenados=stored,
    )


@app.get("/documentos/{filename}", response_model=DocumentoExisteResponse)
async def verificar_documento(filename: str):
    resultado = await _run(search_localstack, filename)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")
    return DocumentoExisteResponse(**resultado)