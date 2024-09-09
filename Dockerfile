# Dockerfile

# Imagem do Airflow
FROM apache/airflow:2.7.2

# Instalando pacotes do python
USER root
RUN pip install psycopg2-binary pandas pyarrow

# Retornando user Airflow
USER airflow

# Copiando dags e os scripts para o container
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

# Opção Utilizando o requirements.txt:
#COPY requirements.txt .
#RUN pip install -r requirements.txt