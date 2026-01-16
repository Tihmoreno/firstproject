# Sistema de Integracao e Analise de Produtos Automotivos

Projeto em Python desenvolvido para integrar dados de produtos de customizacao automotiva
entre um arquivo Excel e um banco de dados MySQL, aplicando validacoes, controle de duplicidade
e sincronizacao automatica de preco e estoque.

Alem da integracao de dados, o projeto tambem contempla a analise das informacoes por meio
de dashboards no Power BI, conectados diretamente ao banco de dados MySQL.

---

##  Arquitetura do Projeto

Excel (origem dos dados)
↓
Python (ETL: validacao, regras de negocio, sincronizacao)
↓
MySQL (base oficial de dados)
↓
Power BI (visualizacao e analise)

---

##  Funcionalidades

- Leitura de produtos a partir de arquivo Excel
- Validacao e limpeza de dados
- Remocao de duplicidades
- Insercao automatica de novos produtos
- Atualizacao de preco e estoque de produtos existentes
- Logs detalhados do processo de sincronizacao
- Integracao do banco MySQL com Power BI
- Criacao de dashboards analiticos

---

##  Tecnologias Utilizadas

- Python 3
- Pandas
- SQLAlchemy
- MySQL (XAMPP)
- Excel
- Power BI
- Git / GitHub

---

##  Como Executar o Projeto

### Pre-requisitos
- Python instalado
- MySQL rodando (XAMPP)
- Power BI Desktop instalado
- Bibliotecas Python:

```bash
pip install pandas sqlalchemy mysql-connector-python