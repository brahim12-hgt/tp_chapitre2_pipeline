from dagster import job, op
import os

@op
def ingest():
    if os.system("python pipeline/ingest.py") != 0:
        raise Exception("L'ingestion a échoué.")

@op
def validate(infra_in=None):
    if os.system("python pipeline/validate.py") != 0:
        raise Exception("La validation a échoué.")

@op
def transform(infra_in=None):
    if os.system("cd dbt_pipeline && dbt run --profiles-dir .") != 0:
        raise Exception("La transformation dbt a échoué.")

@op
def test_data(infra_in=None):
    if os.system("cd dbt_pipeline && dbt test --profiles-dir .") != 0:
        raise Exception("Les tests dbt ont échoué.")

@job
def ventes_pipeline():
    test_data(transform(validate(ingest())))
