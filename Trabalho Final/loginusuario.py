import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 
import traceback  # Para nos mostrar o erro real no terminal se algo falhar

# --- CONFIGURAÇÃO DA CONEXÃO COM O POSTGRESQL ---
def obter_conexao():
    # Removidas as linhas antigas de register_type que causavam conflitos de codificação
    conn = psycopg2.connect(
        host="localhost",
        database="Sistemas_GE", 
        user="postgres",              
        password="senha123",        
        port="5432"                    
    )
    # Garante a comunicação em UTF8 após conectar
    conn.set_client_encoding('UTF8') 
    return conn

# --- FUNÇÃO DE AUTENTICAÇÃO ---
def login():
    email = email_entry.get().strip()
    senha = senha_entry.get().strip()
    
    # Validação simples para evitar idas desnecessárias au banco
    if not email or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        return
    
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        
        # Busca o usuário correspondente ao e-mail e senha digitados
        cursor.execute("SELECT * FROM Usuario WHERE email_institucional = %s AND senha = %s;", (email, senha))
        usuario = cursor.fetchone()
        
        if usuario:
            # usuario[1] representa a coluna 'nome_completo'
            messagebox.showinfo("Login Efetuado", f"Bem-vindo(a), {usuario[1]}!")
            # root.destroy() # Opcional: Descomente para fechar a janela após o login
        else:
            messagebox.showerror("Erro de Autenticação", "Usuário ou senha inválidos.")
            
    except Exception as e:
        # Se ainda der erro, isto vai imprimir o culpado real detalhadamente no seu terminal:
        print("\n--- DETALHES DO ERRO NO TERMINAL ---")
        traceback.print_exc()
        print("-------------------------------------\n")
        
        messagebox.showerror("Erro no Banco", f"Erro ao acessar o banco de dados: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()


# --- INTERFACE GRÁFICA (TKINTER) ---
root = tk.Tk()
root.title("Acesso ao Sistema")

# Centraliza a janela na tela
largura, altura = 350, 200
tela_largura = root.winfo_screenwidth()
tela_altura = root.winfo_screenheight()
x = (tela_largura // 2) - (largura // 2)
y = (tela_altura // 2) - (altura // 2)
root.geometry(f"{largura}x{altura}+{x}+{y}")
root.resizable(False, False)

# Container central para organizar os elementos com margens internas (padding)
frame_login = tk.Frame(root, padx=20, pady=20)
frame_login.pack(expand=True)

# Campo: E-mail
tk.Label(frame_login, text="E-mail Institucional:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
email_entry = tk.Entry(frame_login, width=30, font=("Arial", 10))
email_entry.grid(row=1, column=0, pady=5)
email_entry.insert(0, "ana.silva@ufc.br") # Valor padrão de exemplo

# Campo: Senha
tk.Label(frame_login, text="Senha:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
senha_entry = tk.Entry(frame_login, show="*", width=30, font=("Arial", 10))
senha_entry.grid(row=3, column=0, pady=5)
senha_entry.insert(0, "senha123") # Valor padrão de exemplo

# Botão de Entrada
btn_login = tk.Button(frame_login, text="Entrar", bg="#007bff", fg="white", width=15, font=("Arial", 10, "bold"), command=login)
btn_login.grid(row=4, column=0, pady=15)

root.mainloop()
