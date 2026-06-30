import os
from dotenv import load_model_env, load_dotenv

load_dotenv() # Carrega as variáveis do arquivo .env

def obter_conexao():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    