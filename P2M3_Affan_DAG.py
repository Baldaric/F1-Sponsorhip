'''
=================================================
Milestone 3

Name  : Affan Haidar Anitya
Batch : FTDS-024-HCK


This program is made to do an automatisation of extract, transform, and load from PostgreSQL to ElasticSearch.
The data that we will be using are a data of Formula 1 grand prix from 1998 through 2022.
=================================================
'''

# import libraries
import pandas as pd 
import numpy as np 

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

# default parameters
defaults_args = {
    'owner': 'Terra',
    'retry': None,
    'start_date': datetime(2014, 11, 2),
    'catchup': False
}

# extract function
def Extract (**context):
    
    '''
    this function is doing a data extraction from PostgreSQL, by first define the connection id,
    then put query of SQL that will put the separated tables into one big table. It then save it
    into a dags folder.
    '''
    
    # connection to database
    source_hook = PostgresHook(postgres_conn_id = "postgres_airflow")
    source_conn = source_hook.get_conn()
    
    # extract data
    data_raw = pd.read_sql("""SELECT 
    results.resultid,
    races.year AS year_season,
    races.round,
    circuits.name AS circuitname,
    circuits.country AS country_race,
    races.date,
    constructors.name AS constructorname, 
    constructor_standings.points AS constructor_points,
    constructor_standings.position AS constructor_rank,
    CONCAT(drivers.forename, ' ', drivers.surname) AS driver_name,
    drivers.code AS drivercode,
    driver_standings.points AS driver_points,
    driver_standings.position AS driver_rank,
    results.grid,
    results.position,
    results.points AS race_points,
    status.status
    FROM public.results
    JOIN races ON results.raceId = races.raceId
    JOIN driver_standings ON driver_standings.driverId = results.driverId 
        AND driver_standings.raceId = results.raceId
    JOIN drivers ON driver_standings.driverId = drivers.driverId
    JOIN constructor_standings ON constructor_standings.constructorId = results.constructorId 
        AND constructor_standings.raceId = results.raceId
    JOIN constructors ON constructor_standings.constructorId = constructors.constructorId
    JOIN circuits ON races.circuitId = circuits.circuitId
    JOIN status ON results.statusId = status.statusId
    ORDER BY resultid;""", source_conn)
    
    # save the data
    path = '/opt/airflow/dags/P2M3_Affan_data_raw.csv'
    data_raw.to_csv(path, index=False)
    
    # lempar konteks
    context['ti'].xcom_push(key='location_data', value=path)

# tranform function
def Transform(**context):
    '''
    This data is used to transform the table that have been queried by the extract function
    it will drop a missing values and duplicates, it then changes some column name.
    '''
    # get instance
    ti = context['ti']
    
    # get path
    data_path = ti.xcom_pull(task_ids = 'extract_data', key='location_data')
    
    # read as dataframe
    data_raw = pd.read_csv(data_path)
    
    # cleaning
    data_raw.dropna(inplace=True)
    data_raw.drop_duplicates(inplace=True)
    data_clean = data_raw.rename(columns={'raceid':'race_id', 
                                        'racename':'race_name',
                                        'fastestlap':'fastest_lap',
                                        'constructorname':'constructor_name',
                                        'circuitname': 'circuit_name',
                                        'drivercode': 'driver_code',
                                        'resultid': 'result_id'})
    
    # save data
    path = '/opt/airflow/dags/P2M3_Affan_data_clean.csv'
    data_clean.to_csv(path, index=False)    
    
    # lempar konteks
    context['ti'].xcom_push(key='location_data_clean', value=path)

# function untuk load data ke elastic
def Load(**context):
    '''
    This function will do a data loading to elasticsearch, it doing it by looping the data
    each row and put it to dictionary then upload each dictionary into the elasticsearch.
    '''
    #sama seperti di atas, ini untuk ambil hasil dari function transform. Jadi ambil file yang sudah bersih
    """ Load cleaned data to Elasticsearch """
    ti = context['ti']
    data_path = ti.xcom_pull(task_ids='transform_data', key='location_data_clean')

    #koneksi ke elasticsearch
    es = Elasticsearch(['http://elasticsearch:9200'])

    # load
    data_clean = pd.read_csv(data_path)

    # Indexing data
    index_name = "f1_clean"
    for _, row in data_clean.iterrows():
        doc = row.to_dict()
        es.index(index=index_name, body=doc)

    print(f"Data successfully loaded to Elasticsearch index '{index_name}'.")


# create object DAG
with DAG(
    'pipeline_cleaning',
    description = 'Data pipeline that will extract, transform, and load.',
    schedule_interval = '10,20,30 9 * * 6',
    default_args = defaults_args,
    catchup = False
) as dag :
    
    # task extract
    extract_data = PythonOperator(
        task_id = 'extract_data',
        python_callable = Extract,
        provide_context= True
    )
    
    transform_data = PythonOperator(
        task_id = 'transform_data',
        python_callable = Transform,
        provide_context = True
    )
    
    load_data = PythonOperator(
        task_id = 'load_data',
        python_callable = Load,
        provide_context = True
    )


# flow of process
extract_data >> transform_data >> load_data