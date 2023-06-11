# Use uma imagem base Python
FROM python:3.9-slim

# Cria um diretório Base na imagem
RUN mkdir -p /mlopsServer
RUN mkdir -p /Log

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /mlopsServer

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências usando o pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho do contêiner
COPY . /mlopsServer

# Defina a porta em que o aplicativo estará em execução (substitua 8000 pela porta apropriada, se necessário)
EXPOSE 8000
EXPOSE 80
EXPOSE 8080

# Execute o comando para iniciar o aplicativo
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
