# --- CRUD ----
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 

# --- conexão com o postgreSQL ---- 
def obtener_conexao():
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    
    conn = psycopg2.connect(
        host="localhost",
        database="Sistemas_GE", 
        user="postgres",              
        password="senha123",        
        port="5432"                    
    )
    conn.set_client_encoding('LATIN1') 
    return conn
