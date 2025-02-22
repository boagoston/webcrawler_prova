# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos do seu projeto para dentro do container
COPY . /app

# Atualize o pip
RUN pip install --upgrade pip

# Instale as dependências do arquivo requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copiar o script de entrada
COPY entrypoint.sh /entrypoint.sh

# Tornar o script executável
RUN chmod +x /entrypoint.sh

# Configurar o entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Exponha a porta, caso precise de uma porta para o seu app
# EXPOSE 8000  # Descomente caso use uma aplicação web

# Comando para rodar a aplicação (substitua conforme necessário)

