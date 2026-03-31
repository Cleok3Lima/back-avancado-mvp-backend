# Dockerfile — Backend FastAPI
# Usa Python 3.11 em uma imagem slim (leve) para reduzir o tamanho final da imagem

FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache de camadas do Docker
# (se requirements.txt não mudar, essa camada não é reconstruída)
COPY requirements.txt .

# Instala as dependências sem cache para manter a imagem enxuta
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o uvicorn vai escutar
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com uvicorn
# --host 0.0.0.0 garante que o servidor aceite conexões externas ao container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
