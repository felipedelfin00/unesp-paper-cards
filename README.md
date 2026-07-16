# Cards de Trabalhos Acadêmicos da UNESP

Sistema para extração, enriquecimento e divulgação de trabalhos acadêmicos da UNESP por meio de inteligência artificial.



## Índice

* [Visão geral](#visão-geral)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Instalação](#instalação)
* [Execução](#execução)
* [Banco de dados](#banco-de-dados)
* [Pipeline de processamento](#pipeline-de-processamento)
* [Documentação](#documentação)
* [Autoria](#autoria)
* [Licença](#licença)



## Visão geral

O projeto automatiza a obtenção de trabalhos acadêmicos disponibilizados pelo repositório institucional da UNESP, processa seus metadados, enriquece as informações utilizando inteligência artificial e disponibiliza os resultados em uma interface web voltada ao público geral.

O objetivo é facilitar a divulgação científica, transformando resumos técnicos em descrições mais acessíveis e organizando as informações em cards de fácil visualização.

O processamento é dividido em quatro etapas independentes:

* Extração dos dados da API da UNESP;
* Transformação e normalização dos metadados;
* Busca dos e-mails institucionais dos pesquisadores;
* Enriquecimento das informações utilizando IA.

Após o processamento, os dados são disponibilizados através de uma API REST consumida pelo frontend.

<p align="center">
    <img src="https://i.imgur.com/udCbkJA.png" alt="Interface do sistema" width="800">
</p>



## Tecnologias utilizadas

* **Backend:** Python 3.11, FastAPI, Uvicorn e SQLite
* **Frontend:** HTML5, CSS3 e JavaScript
* **Inteligência Artificial:** OpenAI GPT OSS 120B (Groq)


## Instalação

* Clone o repositório;
* Crie um ambiente virtual e ative-o;
* Instale as dependências com `pip install -r requirements.txt`;
* Copie o arquivo `.env.example` para `.env` e configure a variável `GROQ\_API\_KEY`.



## Execução

* Execute a API com `uvicorn api.routes.cards:app --reload`;
* Execute o frontend com `python -m http.server 5500`;
* Alternativamente, os dois podem ser executados simultaneamente com o script `./run.sh`.
* Abra o navegador e acesse `http://localhost:5500` para visualizar a interface web.



## Banco de dados

O repositório inclui um banco de dados SQLite previamente populado com 1200 trabalhos acadêmicos do Instituto de Geociências e Ciências Exatas (IGCE) e do Instituto de Biociências (IB) da UNESP. Dessa forma, é possível executar o sistema imediatamente, sem necessidade de realizar a extração e o enriquecimento dos dados.

Caso seja necessário recriar o banco de dados, execute `python main.py --database` e utilize o pipeline de processamento descrito abaixo.



## Pipeline de processamento

O processamento dos trabalhos acadêmicos é dividido em etapas independentes, que podem ser executadas individualmente ou em sequência.

|Comando|Finalidade|
|-|-|
|`python main.py --extract`|Extrai novos trabalhos acadêmicos da API da UNESP.|
|`python main.py --transform`|Normaliza os dados extraídos e os armazena no banco de dados.|
|`python main.py --contacts`|Obtém os e-mails institucionais de autores e orientadores.|
|`python main.py --enrich`|Enriquece os trabalhos utilizando inteligência artificial.|
|`python main.py --process`|Executa todas as etapas do pipeline em sequência.|

O sistema foi desenvolvido de forma modular, permitindo a execução de apenas uma etapa sempre que necessário. Durante a extração, trabalhos já presentes no banco de dados são ignorados automaticamente, evitando duplicação de registros.



## Documentação

O relatório completo do projeto, com detalhes sobre a arquitetura e as decisões técnicas, está disponível em [docs/relatorio.pdf](docs/relatorio.pdf).



## Autoria

Projeto desenvolvido no âmbito do Programa de Extensão "Computação Aplicada e Ciência de Dados", da UNESP - Instituto de Geociências e Ciências Exatas (IGCE), campus de Rio Claro.

* **Autor:** Felipe Rovigatti Delfino
* **Orientador:** Prof. Dr. Denis Henrique Pinheiro Salvadeo



## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

