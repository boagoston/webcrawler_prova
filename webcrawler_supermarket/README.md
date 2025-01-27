

## **Web Crawler - Compra Agora**

Este é um projeto de web scraping desenvolvido utilizando a biblioteca Scrapy para extrair dados do website Compra Agora. O script foi projetado para navegar pelas categorias do site, coletar informações sobre os produtos e salvar as URLs processadas em um arquivo.

## Descrição

Este web crawler percorre o site Compra Agora para extrair informações dos produtos em várias categorias. Para cada produto, ele coleta os seguintes dados:

 - Nome do produto 
 - Marca do produto 
 - URL da imagem do produto

Além disso, o crawler salva as URLs de cada página processada em um arquivo de texto chamado `processed_urls.txt.`

## Observação

Embora o objetivo inicial do projeto fosse incluir a etapa de login (com usuário e senha fornecidos), a funcionalidade de login não foi implementada devido a dificuldades para definir o payload utilizado no endpoint de login: `https://www.compra-agora.com/cliente/logar`

*Devido ao payload ir criptografado , não foi compreedido o processo de criptografia*

visto  à constatação de que as informações solicitadas (descrição, fabricante e URL da imagem) podem ser acessadas sem a necessidade de autenticação. Após testar a navegação pelo site, foi observado que todos os dados necessários podem ser extraídos diretamente das páginas de categoria, sem requerer o login do usuário. Por isso, o foco foi mantido na extração dos itens por categoria, deixando de lado a implementação do login, já que não impactaria a coleta dos dados desejados.

## Requisitos

Todos os requisitos estão no requirements.txt e o passo a passo de sua instalação estará no guia de execução junto ao docker

## Estrutura do Código

O script começará a execução, coletando dados das categorias do site e salvando as URLs processadas em processed_urls.txt. Além disso, ele exibirá logs no terminal com informações sobre os produtos extraídos.

`CrawlingSpider`: A classe principal do spider, responsável por iniciar o scraping, navegar pelas categorias e processar os produtos.
`start_requests:` Envia uma solicitação inicial para o site e começa a extração.
`parse`: Função responsável por extrair as categorias do site e gerar novas solicitações para cada uma delas.
`parse_produtos`: Processa a resposta da API da categoria e cria novas solicitações para cada página de produtos.
`parse_produtos_pagina`: Processa as páginas de produtos, extraindo informações como nome, marca e URL da imagem.
`save_processed_url`: Função que salva as URLs processadas em um arquivo de texto.


### Exemplo de Saída

![exemplo](https://i.imgur.com/O6vnwVF.png)

### EXECUÇÃO 

Depois de buildar e executar sua imagem docker e estar na raiz da mesma. O terminal precisa refletir a imagem abaixo:

![](https://i.imgur.com/9LjycDB.png)

Execute a sequencia de comandos abaixo para executar o codigo

    cd webcrawler_supermarket/
    cd webcrawler_supermarket/
    cd spiders
    scrapy crawl crawling_compra

Após o ultimo comando o crawler deve começar a execução e extrair os produtos de compra-agora.
Quando a execução finalizar , podemos utilizar o comando **ls** para verificar o conteudo da pasta e se tudo estiver ocorrido bem teremos 2 arquivos 

processed_urls.txt 
produtos.json

executando o cat em cada um , teremos os respectivos resultados (exemplo)

processed_urls.txt

![alt]https://i.imgur.com/1dYlxeQ.png)


produtos.json

![alt](https://i.imgur.com/jPewuzM.png)


