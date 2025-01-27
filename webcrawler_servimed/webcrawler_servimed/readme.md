## **Servimed - Web Scraping para Retorno de Faturamento**

Este é um projeto de web scraping desenvolvido utilizando a biblioteca Scrapy para coletar informações detalhadas sobre um pedido específico no sistema da Servimed. O script realiza o login no site, pesquisa o pedido baseado no número fornecido e extrai os detalhes do retorno de faturamento, incluindo os itens do pedido e o motivo da rejeição, caso existam. Os dados são retornados no formato JSON e salvos em um arquivo.

## Descrição

Este web scraper é projetado para coletar informações de pedidos no site da Servimed. Para cada pedido, ele coleta as seguintes informações:

- Motivo da rejeição do pedido
- Itens do pedido, contendo:
  - Código do produto
  - Descrição do produto
  - Quantidade faturada

O script usa os tokens de autenticação (`sessiontoken` e `accesstoken`) já obtidos de uma sessão anterior, devido a dificuldades no processo de geração do `uuid` para autenticação. Isso permite que o processo de scraping funcione sem a necessidade de uma autenticação ativa.

## Observação

Embora o script tenha sido projetado para fazer login automaticamente, não foi possível gerar o `uuid` dinâmico para o header `accesstoken`, resultando na utilização de valores fixos para os tokens de acesso. Este procedimento evita o erro 403, mas o ideal seria que o processo de login fosse automatizado com os tokens dinâmicos.

### Utilização do `cffi` e Simulação de Navegador

Para garantir a compatibilidade e o correto processamento das requisições HTTP, foi utilizado o middleware `CurlCffiMiddleware`, que integra a biblioteca `requests` com a funcionalidade do `cffi` (C Foreign Function Interface). Este middleware foi projetado para interceptar as requisições feitas pelo Scrapy e adaptá-las para serem processadas pelo `requests`, com headers, cookies e corpo da requisição manipulados corretamente.

Além disso, a requisição HTTP é configurada para "impersonar" um navegador Chrome (versão 110) através do header `impersonate="chrome110"`. Isso permite que o scraper simule a navegação no site como se fosse um usuário utilizando o Chrome, o que pode ser necessário para evitar bloqueios ou bloqueios de acesso devido a comportamentos típicos de bots.

A função `process_request` do middleware captura a requisição, converte os headers e cookies para o formato adequado e envia a requisição utilizando o `requests.request`. A resposta obtida é então convertida em um objeto `TextResponse` do Scrapy, que mantém a compatibilidade com o restante do processo de scraping.

Esse método é utilizado para contornar algumas limitações que o Scrapy possui ao lidar com requisições HTTP mais complexas, especialmente em casos onde é necessário um controle mais preciso dos headers e cookies da requisição.

## Requisitos

- Python 3.10+
- Scrapy (instalado através do `pip install scrapy`)

Todos os requisitos estão listados no arquivo `requirements.txt` e serão instalados junto com o Docker.

## Execução

Depois de buildar e executar sua imagem docker e estar na raiz da mesma. O terminal precisa refletir a imagem abaixo:

![alt](https://i.imgur.com/9LjycDB.png)

Para executar o script, basta rodar a sequencia de comandos abaixo substituindo `<número_do_pedido>` pelo número do pedido desejado:

    cd webcrawler_servimed
    cd webcrawler_servimed
    python3 busca_servimed.py <numero_do_pedido>

Após a execução é possivel verificar os pedidos na pasta pedido

    cd pedidos
    cat <pedido_xxxxxxx>

resultado utilizando `python3 busca_servimed.py 511082` exemplo abaixo


## Exemplo 

![enter image description here](https://i.imgur.com/7CPJls9.png)


