FROM python:3.11-slim

WORKDIR /app

# Copie arquivos de requirements e instale dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY app ./app

# Exponha a porta utilizada pelo Uvicorn
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Comando padrão para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]