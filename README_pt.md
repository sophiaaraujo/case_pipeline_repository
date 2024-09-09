# Brewery Data Pipeline

Este projeto implementa um pipeline de dados para consumir dados da API Open Brewery DB, transformá-los e carregá-los em um data lake usando a arquitetura Medallion.

## Objetivo

O objetivo é criar um pipeline de dados que consome dados de uma API, transforma eles e os persiste em um data lake com três camadas: bronze, siver e gold.

## Estrutura do Projeto

- `dags/`: Contém o arquivo `brewery_dag.py` para o pipeline de dados no Airflow.
- `scripts/`: Contém os scripts Python para extração, transformação e carga de dados.
- `docker-compose.yml`: Arquivo para configurar e iniciar os containers Docker.
- `Dockerfile`: Define a imagem Docker personalizada para o Airflow.

## Design e Decisões

### Arquitetura Medalhão (dentro do diretório data_lake)

1. **Camada Bronze**: Armazena os dados brutos extraídos da API em formato JSON.
2. **Camada Silver**: Transforma os dados em um formato columnar (Parquet) e particiona por localização.
3. **Camada Gold**: Cria uma visão agregada com a quantidade de cervejarias por tipo e localização, armazenada em formato CSV.

### Ferramentas e Tecnologias

- **Apache Airflow**: Orquestração do pipeline de dados.
- **PostgreSQL**: Armazenamento do Airflow.
- **Docker**: Containerização do ambiente Airflow e do PostgreSQL.
- **Python**: Linguagem para scripts de ETL.
- **Pandas e PyArrow**: Bibliotecas para transformação de dados.

### Decisões e Trade-offs

- **Escolha do Airflow**: Usado por sua robustez na orquestração de workflows e flexibilidade em lidar com diferentes fontes de dados, além de seu suporte a tarefas agendadas, incluindo retries automáticos e paralelismo. O uso do LocalExecutor no Airflow permite que as tarefas sejam executadas de forma eficiente em um ambiente local, e o PostgreSQL foi usado para armazenar o estado do Airflow.
- **Formato Parquet**: Utilizado na camada Silver por ser eficiente para armazenamento e consultas.
- **Containerização com Docker**: Facilita a configuração e o isolamento do ambiente, garantindo consistência entre ambientes de desenvolvimento e produção.

## Monitoramento e Alertas

Para garantir o funcionamento contínuo e a qualidade dos dados no pipeline, implementamos os seguintes mecanismos de monitoramento e alerta:

1. **Monitoramento do Airflow**:
   - **Logs**: Airflow registra logs detalhados para cada tarefa no DAG. Esses logs ajudam a diagnosticar problemas e falhas.
   - **Interface Web**: O Airflow fornece uma interface web para monitoramento em tempo real dos DAGs e suas execuções.
   - Para um monitoramento mais avançado, você pode integrar o Airflow com o Prometheus e usar o Grafana para criar dashboards de monitoramento em tempo real. Isso pode ser útil para visualizar a performance e o comportamento do pipeline de forma contínua.
   - Também é possível configurar perfis diferentes no docker-compose.yml para desenvolvimento e produção. Isso permite ajustar parâmetros (como o nível de logging ou as configurações de retry no Airflow) com base no ambiente.

2. **Alertas de Falhas**:
   - **Emails**: Configure o Airflow para enviar notificações por e-mail em caso de falhas em tarefas. Isso pode ser feito ajustando as configurações de e-mail no arquivo `airflow.cfg`.
   - **Alertas via Slack**: Para uma solução mais avançada, é possível configurar alertas via Slack usando hooks e sensores personalizados no Airflow.

3. **Qualidade dos Dados**:
   - **Validação de Dados**: O pipeline pode incluir verificações automáticas de qualidade, como verificar se os dados contêm todas as colunas esperadas ou se existem valores nulos em campos críticos.

4. **Logs e Métricas**:
   - **Logs de Execução**: Certifique-se de que os logs estejam sendo corretamente capturados e armazenados para análise posterior.
   - **Métricas de Performance**: Monitore as métricas de desempenho do Airflow e do PostgreSQL para identificar possíveis gargalos.

5. **Pipeline CI/CD**:
   - **Automação de Deploy**: Se o projeto crescer ou passar a ser mantido por uma equipe, adicionar pipelines de CI/CD (Continuous Integration/Continuous Deployment) pode agilizar testes e deploys automáticos. Ferramentas como GitHub Actions podem ser usadas para garantir que, ao fazer push no repositório, os testes são executados e, se passarem, o deploy em um ambiente de produção ou staging é feito automaticamente.

## Instruções para Executar

Certifique-se de ter as seguintes ferramentas instaladas:

Docker (versão 20.10 ou superior)
Docker Compose (versão 1.29 ou superior)
Para verificar, execute:
```bash
docker --version
docker-compose --version 
```

1. **Clone o Repositório**

   Clone o repositório e navegue até o diretório do projeto:

   ```bash
   git clone https://github.com/sophiaaraujo/case_pipeline_repository.git
   cd case_pipeline
   ```

2. **Iniciar os Serviços com Docker**

   O projeto utiliza Docker Compose para orquestrar os serviços. Para inicializar o Airflow, o PostgreSQL e demais componentes, execute o comando abaixo:
   ```bash
   docker-compose up -d
   ```
   Este comando irá baixar as imagens necessárias e iniciar os containers em segundo plano.

3. ***Acesse a Interface do Airflow***

   Uma vez que os containers estiverem rodando, você poderá acessar a interface do Airflow no navegador:
   http://localhost:8080   (Usuário: airflow; Senha: airflow)

4. ***Ativar e Executar a DAG***

   Dentro da interface do Airflow:

   Vá até a aba "DAGs" para visualizar a lista de DAGs disponíveis.
   Localize a DAG brewery_dag e ative-a clicando no botão de "liga/desliga" ao lado do nome.
   Para iniciar a DAG manualmente, clique no ícone de "play" (executar).

5. ***Verificação dos Dados no Data Lake***

   Os dados serão salvos no diretório data_lake montado no container do Airflow:

   Bronze Layer: Dados brutos no formato JSON.
   Silver Layer: Dados transformados no formato Parquet, particionados por localização.
   Gold Layer: Agregação da quantidade de cervejarias por tipo e localização, armazenados em CSV.

   Esses arquivos podem ser encontrados na pasta data_lake dentro do container ou no diretório local mapeado.

6. ***Parar os Containers***

   Quando terminar de usar o pipeline, pare todos os containers com o comando:
   ```bash
   docker-compose down
   ```