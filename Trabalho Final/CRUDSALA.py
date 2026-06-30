import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 

def obter_conexao():
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

#FUNÇÕES DO CRUD

def listar_reservas():
    for row in tabela.get_children():
        tabela.delete(row)
        
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_reserva, data_reserva, id_sala, id_grupo FROM Reserva ORDER BY id_reserva;")
        linhas = cursor.fetchall()
        
        for linha in linhas:
            tabela.insert("", tk.END, values=linha)
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar reservas: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def reservar_sala():
    data = reserva_data_entry.get().strip()
    id_sala = reserva_sala_entry.get().strip()
    id_grupo = reserva_grupo_entry.get().strip()
    
    if not data or not id_sala:
        messagebox.showwarning("Aviso", "Data e ID da Sala são obrigatórios!")
        return
    
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reserva (data_reserva, id_sala, id_grupo) 
            VALUES (%s, %s, %s);
        """, (data, id_sala, id_grupo if id_grupo else None))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Sala reservada com sucesso!")
        limpar_campos()
        listar_reservas() # Atualiza a tabela
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao reservar sala: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def editar_reserva():
    # Verifica se tem alguma linha selecionada
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma reserva na tabela para editar!")
        return
        
    id_reserva = tabela.item(item_selecionado)['values'][0]
    data = reserva_data_entry.get().strip()
    id_sala = reserva_sala_entry.get().strip()
    id_grupo = reserva_grupo_entry.get().strip()
    
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Reserva 
            SET data_reserva = %s, id_sala = %s, id_grupo = %s 
            WHERE id_reserva = %s;
        """, (data, id_sala, id_grupo if id_grupo else None, id_reserva))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Reserva atualizada com sucesso!")
        limpar_campos()
        listar_reservas()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def excluir_reserva():
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma reserva na tabela para excluir!")
        return
        
    id_reserva = tabela.item(item_selecionado)['values'][0]
    
    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a reserva ID {id_reserva}?"):
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Reserva WHERE id_reserva = %s;", (id_reserva,))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Reserva excluída com sucesso!")
            limpar_campos()
            listar_reservas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

def obter_linha_selecionada(event):
    item_selecionado = tabela.selection()
    if item_selecionado:
        valores = tabela.item(item_selecionado)['values']
        
        limpar_campos()
        reserva_data_entry.insert(0, valores[1])
        reserva_sala_entry.insert(0, valores[2])
        reserva_grupo_entry.insert(0, valores[3] if valores[3] != "None" and valores[3] is not None else "")

def limpar_campos():
    reserva_data_entry.delete(0, tk.END)
    reserva_sala_entry.delete(0, tk.END)
    reserva_grupo_entry.delete(0, tk.END)


# INTERFACE GRÁFICA
root = tk.Tk()
root.title("CRUD - Gerenciador de Reservas")
root.geometry("600x500")

# Formulário Entrada
frame_sala = ttk.LabelFrame(root, text=" Dados da Reserva ", padding=15)
frame_sala.pack(padx=15, pady=10, fill="x")

tk.Label(frame_sala, text="Data (AAAA-MM-DD):").grid(row=0, column=0, sticky="w", pady=5)
reserva_data_entry = tk.Entry(frame_sala, width=25)
reserva_data_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_sala, text="ID da Sala:").grid(row=1, column=0, sticky="w", pady=5)
reserva_sala_entry = tk.Entry(frame_sala, width=25)
reserva_sala_entry.grid(row=1, column=1, pady=5, padx=5)

tk.Label(frame_sala, text="ID do Grupo (Opcional):").grid(row=2, column=0, sticky="w", pady=5)
reserva_grupo_entry = tk.Entry(frame_sala, width=25)
reserva_grupo_entry.grid(row=2, column=1, pady=5, padx=5)

# Frame para os botões 
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

btn_salvar = tk.Button(frame_botoes, text="Inserir Novo", command=reservar_sala, bg="#6EB06E", fg="white", width=12)
btn_salvar.grid(row=0, column=0, padx=5)

btn_editar = tk.Button(frame_botoes, text="Salvar Edição", command=editar_reserva, bg="#568856", fg="white", width=12)
btn_editar.grid(row=0, column=1, padx=5)

btn_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir_reserva, bg="#3F613F", fg="white", width=12)
btn_excluir.grid(row=0, column=2, padx=5)

btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos, bg="#314E31", fg="white", width=12)
btn_limpar.grid(row=0, column=3, padx=5)

# Tabela de Listagem
frame_tabela = ttk.LabelFrame(root, text=" Reservas Cadastradas ", padding=10)
frame_tabela.pack(padx=15, pady=10, fill="both", expand=True)

colunas = ("id", "data", "sala", "grupo")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=8)

# Configurando cabeçalhos 
tabela.heading("id", text="ID Reserva")
tabela.heading("data", text="Data")
tabela.heading("sala", text="ID Sala")
tabela.heading("grupo", text="ID Grupo")

# Ajustando Colunas
tabela.column("id", width=80, anchor="center")
tabela.column("data", width=150, anchor="center")
tabela.column("sala", width=100, anchor="center")
tabela.column("grupo", width=100, anchor="center")

tabela.pack(fill="both", expand=True)

tabela.bind("<<TreeviewSelect>>", obter_linha_selecionada)

# Executa a listagem
listar_reservas()

root.mainloop()