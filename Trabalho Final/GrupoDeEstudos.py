import sqlite3

conn = sqlite3.connect("grupos.db")
cursor = conn.cursor()

def login():
    email = input("Email: ")
    senha = input("Senha: ")
    cursor.execute("SELECT * FROM Usuario WHERE email_institucional=? AND senha=?", (email, senha))
    usuario = cursor.fetchone()
    if usuario:
        print(f"Bem-vindo {usuario[1]}!")
    else:
        print("Usuário ou senha inválidos.")

def criar_grupo():
    nome = input("Nome do grupo: ")
    id_adm = input("ID do administrador: ")
    descricao = input("Descrição: ")
    status = input("Status: ")
    qtd = input("Qtd participantes: ")
    disciplina = input("Disciplina: ")
    cursor.execute("INSERT INTO Grupo (nome_grupo, id_adm, descricao, status, qtd_participantes, nomes_disciplinas) VALUES (?, ?, ?, ?, ?, ?)",
                   (nome, id_adm, descricao, status, qtd, disciplina))
    conn.commit()
    print("Grupo criado com sucesso!")

def reservar_sala():
    solicitante = input("Nome do solicitante: ")
    data = input("Data (AAAA-MM-DD): ")
    id_sala = input("ID da sala: ")
    id_grupo = input("ID do grupo (opcional): ")
    cursor.execute("INSERT INTO Reserva (solicitante, data_reserva, id_sala, id_grupo) VALUES (?, ?, ?, ?)",
                   (solicitante, data, id_sala, id_grupo if id_grupo else None))
    conn.commit()
    print("Sala reservada com sucesso!")

# Menu
while True:
    print("\n--- MENU ---")
    print("1 - Login")
    print("2 - Criar Grupo")
    print("3 - Reservar Sala")
    print("0 - Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        login()
    elif opcao == "2":
        criar_grupo()
    elif opcao == "3":
        reservar_sala()
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")
