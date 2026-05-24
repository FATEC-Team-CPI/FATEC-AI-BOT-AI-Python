# 1. Define a imagem base
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia requirements primeiro (para cache do Docker)
COPY requirements.txt .
RUN chmod +x /usr/local/bin/entrypoint.sh

# 4. Instala as dependências do projeto de forma leve
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o restante do código
COPY src/ .

# 6. Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# 7. Expõe a porta que a aplicação vai utilizar
EXPOSE 8000

# 8. Comando que inicia a sua aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
