import logging
from mcp.server.fastmcp import FastMCP
import chromadb
from app.config import db, s3, BUCKET_NAME


"""
Ferramentas para a IA utlizar
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fatec-mcp")


mcp = FastMCP("fatec-docs", json_response=True)


@mcp.tool()
async def list_available_documents() -> list[dict]:
    """
    Lista todos os documentos disponíveis na base de conhecimento
    da FATEC Itaquera. SEMPRE chame esta função primeiro, antes de
    buscar, para identificar qual documento é mais relevante.
    
    Retorna uma lista de documentos com seus metadados.
    """
    logger.info("📋 Listando documentos disponíveis...")
    documents = await document_repository.list_all()
    logger.info(f"✅ {len(documents)} documentos encontrados")
    return documents


@mcp.tool()
async def search_fatec_documents(
    query: str,
    document_type: str
) -> list[dict]:
    """
    Busca informações dentro de um documento da FATEC Itaquera.
    Só chame após usar list_available_documents() para identificar
    o document_type correto.
    
    Args:
        query: Pergunta ou termo de busca do usuário
        document_type: Tipo exato do documento (ex: calendario_academico, 
                      edital_vestibular, grade_curricular, regulamento, contato)
    
    Retorna uma lista de resultados com conteúdo, fonte e relevância.
    """

    logger.info(f"🔍 Buscando em documentos...")
    
    results = await db.search(
        query=query,
        document_type=document_type,
        limit=5
    )
    
    if not results:
        logger.warning(f"⚠️ Nenhum resultado encontrado para: {query}")
    else:
        logger.info(f"✅ {len(results)} resultado(s) encontrado(s)")
    
    return results