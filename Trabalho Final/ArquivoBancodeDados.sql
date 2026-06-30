--- Tabelas Base

create table Usuario (
    id_usuario serial primary key,
    nome_completo varchar(255) not null,
    frequencia boolean not null default true,
    email_institucional varchar(100) unique not null, 
    senha varchar(20) not null,
    data_nascimento date not null,
    matricula varchar(10) unique not null,
    curso varchar(100) null
);

create table Disciplina (
    id_disciplina serial primary key,
    nome_disciplina varchar(150) unique not null, 
    qtd_turmas int not null default 1,
    qtd_alunos int not null default 0
);

create table Comunidade (
    id_comunidade serial primary key,
    nome_comunidade varchar(100) unique not null,
    qtd_participantes int not null default 0,
    mensagem varchar(255) null,
    midia varchar(255) null 
);

create table Sala (
    id_sala serial primary key,
    localizacao varchar(100) unique not null, 
    descricao varchar(150) not null,          
    capacidade int not null
);

--- Dependentes de Usuario

create table Adiministrador (
    id_usuario int primary key, 
    gc_grupo int not null default 0,
    gc_encontros int not null default 0,
    qtd_frequencias_feitas int not null default 0,
    foreign key (id_usuario) references Usuario(id_usuario) on delete cascade
) inherits (Usuario);

create table Monitor (
    id_usuario int primary key,
    disponibilidade_dia_semana varchar(50) not null,
    disponibilidade_horario_inicio time not null, 
    disponibilidade_horario_fim time not null,    
    mn_disciplina int not null, 
    foreign key (id_usuario) references Usuario(id_usuario) on delete cascade,
    foreign key (mn_disciplina) references Disciplina(id_disciplina)
) inherits (Usuario);

---

create table Grupo (
    id_grupo serial primary key,
    nome_grupo varchar(150) not null,
    id_adm int not null,
    id_monitor int null, 
    descricao text not null,
    status varchar(50) not null default 'ativo', 
    qtd_participantes int not null default 1,
    foreign key (id_adm) references Usuario(id_usuario),
    foreign key (id_monitor) references Usuario(id_usuario)
);

create table Inscricao (
    id_inscricao serial primary key,
    data_inscricao date not null default current_date,
    id_usuario int not null,
    foreign key (id_usuario) references Usuario(id_usuario)
);

create table Encontros (
    id_encontros serial primary key,
    data_encontro date not null,
    status boolean not null default true,
    id_grupo int not null,
    foreign key (id_grupo) references Grupo(id_grupo)
);

create table Data_Hora_Encontro (
    id_encontros int not null,
    inicio_ time not null,
    fim time not null,
    primary key (id_encontros, inicio_),
    foreign key (id_encontros) references Encontros(id_encontros)
);

create table Presencial (
    id_encontros int primary key,
    id_sala int not null,
    foreign key (id_encontros) references Encontros(id_encontros),
    foreign key (id_sala) references Sala(id_sala)
);

create table Local (
    id_encontros int primary key,
    bloco varchar(50) not null,
    sala_nome varchar(50) not null,
    foreign key (id_encontros) references Presencial(id_encontros)
);

create table Virtual (
    id_encontros int primary key,
    link_chamada varchar(255) not null,
    foreign key (id_encontros) references Encontros(id_encontros)
);

create table Chamada (
    id_encontros int primary key,
    video boolean not null default true,
    voz boolean not null default true,
    foreign key (id_encontros) references Virtual(id_encontros)
);

create table Avisos (
    id_aviso serial primary key,
    titulo varchar(100) not null,
    descricao text null,
    id_usuario int not null,
    id_grupo int not null,
    data_publicacao timestamp not null default current_timestamp,
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_grupo) references Grupo(id_grupo)
);

create table Material (
    id_material serial primary key,
    titulo varchar(150) not null,
    tipo_de_arquivo varchar(50) not null, 
    data_upload date not null default current_date
);

create table Chat (
    id_mensagem serial primary key,
    id_usuario int not null,        
    id_grupo int not null,
    msg_assunto varchar(150) null,
    data_mensagem timestamp not null default current_timestamp,
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_grupo) references Grupo(id_grupo)
);

create table Reserva (
    id_reserva serial primary key,
    data_reserva date not null,
    horario_reserva time not null default '00:00:00',
    id_sala int not null,
    id_grupo int null,
    foreign key (id_sala) references Sala(id_sala), 
    foreign key (id_grupo) references Grupo(id_grupo)
);

create table Solicitante (
    id_reserva int primary key,
    monitor_solicitante int null,
    adm_solicitante int null,
    foreign key (id_reserva) references Reserva(id_reserva) on delete cascade,
    foreign key (monitor_solicitante) references Monitor(id_usuario),
    foreign key (adm_solicitante) references Adiministrador(id_usuario)
);

create table Registra (
    id_inscricao int not null,
    id_grupo int not null,
    participantes int not null default 1,
    primary key (id_inscricao, id_grupo),
    foreign key (id_inscricao) references Inscricao(id_inscricao),
    foreign key (id_grupo) references Grupo(id_grupo) 
);

create table Possui_Disciplina (
    id_usuario int not null,
    id_disciplina int not null,
    primary key (id_usuario, id_disciplina),
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_disciplina) references Disciplina(id_disciplina) 
);

create table Grupo_Disciplina (
    id_grupo int not null,
    id_disciplina int not null,
    primary key (id_grupo, id_disciplina),
    foreign key (id_grupo) references Grupo(id_grupo),
    foreign key (id_disciplina) references Disciplina(id_disciplina) 
);

create table Comunidade_Usuario (
    id_comunidade int not null,
    id_usuario int not null,
    primary key (id_comunidade, id_usuario),
    foreign key (id_comunidade) references Comunidade(id_comunidade),
    foreign key (id_usuario) references Usuario(id_usuario)
);

create table Participa (
    id_inscricao_participa serial,
    id_usuario int not null,
    id_grupo int not null,
    data_inscricao date not null default current_date,
    primary key (id_usuario, id_grupo),
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_grupo) references Grupo(id_grupo) 
);

create table Participa_Encontros (
    id_usuario int not null,
    id_encontros int not null,
    primary key (id_usuario, id_encontros),
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_encontros) references Encontros(id_encontros)
);

create table Adiciona_Materiais (
    id_grupo int not null,
    id_material int not null,
    primary key (id_grupo, id_material),
    foreign key (id_grupo) references Grupo(id_grupo),
    foreign key (id_material) references Material(id_material)
);

create table Tem_Materiais (
    id_material int not null,
    id_disciplina int not null,
    primary key (id_material, id_disciplina),
    foreign key (id_material) references Material(id_material),
    foreign key (id_disciplina) references Disciplina(id_disciplina)
);

create table Envia_Mensagens (
    id_usuario int not null,
    id_mensagem int not null,
    data_envio timestamp not null default current_timestamp,
    primary key (id_usuario, id_mensagem),
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_mensagem) references Chat(id_mensagem)
);

create table Recebe_Mensagens (
    id_usuario int not null,
    id_mensagem int not null,
    primary key (id_usuario, id_mensagem),
    foreign key (id_usuario) references Usuario(id_usuario),
    foreign key (id_mensagem) references Chat(id_mensagem)
);


insert into Disciplina (nome_disciplina, qtd_turmas, qtd_alunos) values
	('Algoritmos e programação', 4, 120),
	('Cálculo diferencial', 3, 90),
	('Banco de dados i', 2, 65),
	('Estrutura de dados', 2, 50),
	('Engenharia de requisitos', 1, 35),
	('Redes de computadores', 2, 55),
	('Sistemas operacionais', 2, 48),
	('Programação web', 3, 85),
	('Álgebra linear', 3, 100),
	('Inteligência artificial', 1, 25);

insert into Usuario (id_usuario, nome_completo, frequencia, email_institucional, senha, data_nascimento, matricula, curso) VALUES
	(1, 'Ana Silva', true, 'ana.silva@ufc.br', 'senha123', '2001-05-15', '100051', 'Ciência da Computação'),
	(2, 'Bruno Costa', true, 'bruno.costa@ufc.br', 'abcd456', '2002-03-22', '100052', 'Engenharia de Software'),
	(3, 'Carlos Souza', false, 'carlos.souza@ufc.br', 'qwerty', '2000-11-02', '100003', 'Sistemas de Informação'),
	(4, 'Diana Mendes', true, 'diana.mendes@ufc.br', 'diana789', '2003-07-19', '100004', 'Ciência da Computação'),
	(5, 'Eduardo Rocha', true, 'eduardo.rocha@ufc.br', 'edurock', '2005-08-12', '100005', 'Sistemas de Informação'),
	(6, 'Fernanda Lima', false, 'fernanda.lima@ufc.br', 'fer1234', '2001-01-30', '100066', 'Engenharia de Software'),
	(7, 'Gabriel Jesus', true, 'gabriel.j@ufc.br', 'gabi99', '2002-12-25', '100067', 'Redes de Computadores'),
	(8, 'Helena Ramos', true, 'helena.r@ufc.br', 'helen432', '2000-04-10', '100068', 'Sistemas de Informação'),
	(9, 'Jose Oliveira', false, 'jo.o@ufc.br', 'jose777', '2003-09-05', '100069', 'Ciência da Computação'),
	(10, 'Julia Martins', true, 'julia.m@ufc.br', 'juju88', '2002-06-14', '100070', 'Engenharia de Software'),
	(11, 'Vitor Alves', true, 'vitor.al@ufc.br', 'vkal66', '2006-01-01', '100056', 'Ciencia da Computação'),
	(12, 'Antoni Viana', true, 'antoni.viana@ufc.br', 'toni77', '2006-02-02', '100057', 'Sistemas de Informação'),
	(13, 'Nayara Almeida', true, 'naih.almeida@ufc.br', 'naih88', '2007-03-03', '100058', 'Redes de Computadores'),
	(14, 'Morgam Vale', true, 'morgs.vale@ufc.br', 'morgs99', '2005-04-04', '100059', 'Design Digital'),
	(15, 'Laticia Coelho', true, 'lehleh@ufc.br', 'lehleh11', '2005-06-05', '100060', 'Engenharia de Software'),
	(16, 'Mateus Oliveira', true, 'mateus.al@ufc.br', 'mat9876', '2002-04-12', '100061', 'Ciência da Computação'),  
	(17, 'Beatriz Sousa', true, 'beatriz.r@ufc.br', 'bia_2026', '2003-09-22', '100062', 'Engenharia de Software'), 
	(18, 'Thiago Medeiros', false, 'thiago.f@ufc.br', 'tff771', '2001-01-15', '100063', 'Sistemas de Informação'), 
	(19, 'Larissa Mendes', true, 'larissa.m@ufc.br', 'lari_gyn05', '2004-03-05', '100064', 'Ciência da Computação'),
	(20, 'Rodrigo Sousa', true, 'rodrigo.p@ufc.br', 'rod_99x', '2000-07-19', '100065', 'Redes de Computadores');


insert into Adiministrador (nome_completo, frequencia, email_institucional, senha, data_nascimento, matricula, curso, gc_grupo, gc_encontros, qtd_frequencias_feitas) values
	('Ana Silva', true, 'ana.silva@ufc.br', 'senha123', '2001-05-15', '100051', 'Ciência da Computação', 1, 5, 10),
	('Bruno Costa', true, 'bruno.costa@ufc.br', 'abcd456', '2002-03-22', '100052', 'Engenharia de Software', 1, 4, 8),
	('Carlos Souza', false, 'carlos.souza@ufc.br', 'qwerty', '2000-11-02', '100003', 'Sistemas de Informação', 2, 2, 4),
	('Diana Mendes', true, 'diana.mendes@ufc.br', 'diana789', '2003-07-19', '100004', 'Ciência da Computação', 0, 1, 2),
	('Eduardo Rocha', true, 'eduardo.rocha@ufc.br', 'edurock', '2005-08-12', '100005', 'Sistemas de Informação', 3, 6, 12),
	('Fernanda Lima', false, 'fernanda.lima@ufc.br', 'fer1234', '2001-01-30', '100066', 'Engenharia de Software', 1, 2, 3),
	('Gabriel Jesus', true, 'gabriel.j@ufc.br', 'gabi99', '2002-12-25', '100067', 'Redes de Computadores', 0, 0, 1),
	('Helena Ramos', true, 'helena.r@ufc.br', 'helen432', '2000-04-10', '100068', 'Sistemas de Informação', 2, 4, 5),
	('Jose Oliveira', false, 'jo.o@ufc.br', 'jose777', '2003-09-05', '100069', 'Ciência da Computação', 1, 1, 2),
	('Julia Martins', true, 'julia.m@ufc.br', 'juju88', '2002-06-14', '100070', 'Engenharia de Software', 4, 8, 15);

insert into Monitor (nome_completo, frequencia, email_institucional, senha, data_nascimento, matricula, curso, disponibilidade_dia_semana, disponibilidade_horario_inicio, disponibilidade_horario_fim, mn_disciplina) VALUES 
	('Vitor Alves', true, 'vitor.al@ufc.br', 'vkal66', '2006-01-01', '100056', 'Ciencia da Computação', 'segunda-feira', '08:00:00', '10:00:00', 1),
	('Antoni Viana', true, 'antoni.viana@ufc.br', 'toni77', '2006-02-02', '100057', 'Sistemas de Informação', 'terça-feira', '14:00:00', '16:00:00', 2),
	('Nayara Almeida', true, 'naih.almeida@ufc.br', 'naih88', '2007-03-03', '100058', 'Redes de Computadores', 'quarta-feira', '19:00:00', '21:00:00', 3),
	('Morgam Vale', true, 'morgs.vale@ufc.br', 'morgs99', '2005-04-04', '100059', 'Design Digital', 'quinta-feira', '09:30:00', '11:30:00', 4),
	('Laticia Coelho', true, 'lehleh@ufc.br', 'lehleh11', '2005-06-05', '100060', 'Engenharia de Software', 'sexta-feira', '15:30:00', '17:30:00', 5),
	('Mateus Oliveira', true, 'mateus.al@ufc.br', 'mat9876', '2002-04-12', '100061', 'Ciência da Computação', 'segunda-feira', '10:00:00', '12:00:00', 6),   
	('Beatriz Sousa', true, 'beatriz.r@ufc.br', 'bia_2026', '2003-09-22', '100062', 'Engenharia de Software', 'terça-feira', '16:00:00', '18:00:00', 7), 
	('Thiago Medeiros', false, 'thiago.f@ufc.br', 'tff771', '2001-01-15', '100063', 'Sistemas de Informação', 'quarta-feira', '08:00:00', '10:00:00', 8), 
	('Larissa Mendes', true, 'larissa.m@ufc.br', 'lari_gyn05', '2004-03-05', '100064', 'Ciência da Computação', 'quinta-feira', '14:00:00', '16:00:00', 9),
	('Rodrigo Sousa', true, 'rodrigo.p@ufc.br', 'rod_99x', '2000-07-19', '100065', 'Redes de Computadores', 'sexta-feira', '10:00:00', '12:00:00', 10);

insert into Grupo (nome_grupo, id_adm, id_monitor, descricao, status, qtd_participantes) values
	('madrugando com algoritimos', 1, 11, 'focado em lógica e estruturas básicas', 'ativo', 5),
	('se aventurando no cálculo', 2, 12, 'resolução de listas e atividades', 'ativo', 8),
	('mestres do sql', 3, 13, 'modelagem e scripts complexos', 'ativo', 12),
	('estruturas avançadas', 4, 14, 'árvores, grafos e ordenação', 'ativo', 6),
	('engenheiras unidas', 5, 15, 'análise de casos práticos e uml', 'inativo', 4),
	('hackers de redes', 6, 16, 'configuração de roteadores e sub-redes', 'ativo', 15),
	('pinguins do so', 7, 17, 'threads, processos e script', 'ativo', 9),
	('web devs front-end', 8, 18, 'html, css, javascript e react', 'ativo', 20),
	('vetores e matrizes', 9, 19, 'estudos para as provas de álgebra', 'inativo', 3),
	('compila e roda', 10, 20, 'aprendizado supervisionado', 'ativo', 7);

insert into Inscricao (data_inscricao, id_usuario) values
	('2026-05-01', 1), ('2026-05-02', 2), ('2026-05-03', 3), ('2026-05-04', 4), ('2026-05-05', 5),
	('2026-05-06', 11), ('2026-05-07', 12), ('2026-05-08', 13), ('2026-05-09', 14), ('2026-05-10', 15);

insert into Encontros (data_encontro, status, id_grupo) values
	('2026-05-31', true, 1),   
	('2026-06-01', true, 2),   
	('2026-06-02', false, 3),  
	('2026-06-03', true, 4),   
	('2026-06-04', true, 5),   
	('2026-06-05', false, 6), 
	('2026-06-06', true, 7),   
	('2026-06-07', true, 8),   
	('2026-06-08', true, 9),   
	('2026-06-09', false, 10); 

insert into Sala (localizacao, descricao, capacidade) values
	('bloco a - sala 101', 'sala de aula padrão com projetor', 40),
	('bloco a - sala 102', 'sala de aula padrão com projetor', 40),
	('bloco b - lab 1', 'laboratório 01', 30),
	('bloco b - lab 2', 'laboratório 02', 30),
	('bloco c - sala 201', 'sala de conferências/reuniões', 20),
	('bloco c - auditório', 'auditório principal do campus', 120),
	('biblioteca - cabine 1', 'cabine de estudos individuais', 2),
	('biblioteca - cabine 2', 'cabine de estudos individuais', 2),
	('biblioteca - sala grupo a', 'sala de estudos em grupo', 8),
	('biblioteca - sala grupo b', 'sala de estudos em grupo', 8);

insert into Comunidade (nome_comunidade, qtd_participantes, mensagem) values
	('devs do campus', 150, 'bem-vindo ao grupo de desenvolvedores!'),
	('matemática sem dor', 85, 'dúvidas sobre cálculo? pergunte aqui.'),
	('banco de dados', 200, 'discussões sobre sql e nosql.'),
	('maratona de programação', 45, 'treinos aos sábados de manhã.'),
	('vagas e estágios ti', 310, 'compartilhamento de oportunidades.'),
	('usuarios de linux', 90, 'dicas de comandos, discos e kernel.'),
	('ui/ux designers', 60, 'fórum sobre design de interfaces.'),
	('grupo de python', 115, 'estudos focados em machine learning.'),
	('segurança da informação', 75, 'discussões sobre pentest e ctfs.'),
	('calouros 2026', 180, 'grupo de integração para novos alunos.');

insert into Material (titulo, tipo_de_arquivo, data_upload) values
	('apostila de python avançado', 'pdf', '2026-05-10'),
	('formulário de derivadas', 'pdf', '2026-05-11'),
	('script da aula 05', 'sql', '2026-05-12'),
	('implementação de listas', 'pptx', '2026-05-13'),
	('documentação sobre o trabalho final', 'docx', '2026-05-14'),
	('slide da aula 03', 'pptx', '2026-05-15'),
	('guia para instalação de vs code', 'pdf', '2026-05-16'),
	('aplicação modelo para trabalho final', 'zip', '2026-05-17'),
	('notas de aula de álgebra', 'pdf', '2026-05-18'),
	('apostila usada na ultima aula:', 'pdf', '2026-05-19');

insert into Chat (id_usuario, id_grupo, msg_assunto, data_mensagem) values
	(1, 1, 'alguém conseguiu resolver a questão 3?', '2026-04-25 10:00:00'),
	(2, 2, 'amanhã o encontro vai ser presencial?', '2026-05-28 11:15:00'),
	(3, 3, 'qual a versão do postgresql que estamos usando?', '2026-05-11 09:30:00'),
	(4, 4, 'tem alguma coisa para entregar amanhã?', '2026-05-19 14:22:00'),
	(5, 5, 'alguem conseguiu resolver a questão 10?', '2026-05-17 15:40:00'),
	(11, 6, 'alguém tem o email do professor de so?', '2026-05-12 18:01:00'),
	(12, 7, 'amanhã tem aula?', '2026-05-28 20:12:00'),
	(13, 8, 'achei uma playlist sobre listas em go!', '2026-05-28 21:00:00'),
	(14, 9, 'não sei resolver essa questão, alguém poderia me ajudar?', '2026-05-29 08:30:00'),
	(15, 10, 'os ônibus estão funcionando?', '2026-05-21 12:00:00');

insert into Avisos (titulo, descricao, id_usuario, id_grupo, data_publicacao) values
	('monitoria de sábado', 'teremos monitoria extra de algoritmos às 09h.', 1, 1, '2026-05-20 09:00:00'),
	('prazo do trabalho', 'não esqueçam de enviar o script até terça.', 2, 3, '2026-05-21 23:59:00'),
	('cancelamento de aula', 'o encontro de cálculo de hoje foi cancelado.', 3, 2, '2026-05-22 14:00:00'),
	('material novo', 'slides sobre grafos postados na pasta.', 4, 4, '2026-05-23 10:30:00'),
	('reunião de escopo', 'discussão sobre os requisitos do projeto final.', 5, 5, '2026-05-24 16:00:00'),
	('simulado preparatório', 'disponibilizado o simulado de redes.', 6, 6, '2026-05-25 11:00:00'),
	('instalação do linux', 'trazer pendrive para o laboratório amanhã.', 7, 7, '2026-05-26 08:00:00'),
	('desafio css', 'quem fizer o melhor layout ganha um ponto.', 8, 8, '2026-05-27 12:00:00'),
	('lista extra', 'exercícios de transformações lineares disponíveis.', 9, 9, '2026-05-28 17:15:00'),
	('palestra valendo h.c', 'cybersegurança', 10, 10, '2026-05-29 19:30:00');

insert into Reserva (data_reserva, horario_reserva, id_sala, id_grupo) values
	('2026-06-11', '08:00:00', 1, 1),
	('2026-06-12', '14:00:00', 2, 2),
	('2026-06-13', '18:30:00', 3, 3),
	('2026-06-14', '09:00:00', 4, 4),
	('2026-06-15', '16:00:00', 5, 5),
	('2026-06-16', '10:30:00', 6, 6),
	('2026-06-17', '19:00:00', 7, 7),
	('2026-06-18', '13:00:00', 8, 8),
	('2026-06-19', '07:30:00', 9, 9), 
	('2026-06-20', '15:00:00', 10, 10);

insert into Virtual (id_encontros, link_chamada) values 
	(1, 'meet.google.com/abc-defg-hij'), (2, 'meet.google.com/xyz-wdas-asd'),
	(3, 'meet.google.com/p03'), (4, 'teams.microsoft.com/r1'),
	(5, 'meet.google.com/p05'), (6, 'meet.google.com/qwe-rtyu-iop'),
	(7, 'meet.google.com/p07'), (8, 'teams.microsoft.com/r2'),
	(9, 'meet.google.com/p09'), (10, 'meet.google.com/zxc-vbnm-lkj');

insert into Chamada (id_encontros, video, voz) values
	(1, true, true), (2, true, true), (3, false, true), (4, true, false), (5, true, true),
	(6, false, true), (7, true, true), (8, true, true), (9, false, true), (10, true, true);

insert into Presencial (id_encontros, id_sala) values 
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
	(6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

insert into Local (id_encontros, bloco, sala_nome) values
	(1, 'bloco a', 'sala 101'), (2, 'bloco a', 'sala 102'), (3, 'bloco b', 'lab 1'), (4, 'bloco b', 'lab 2'),
	(5, 'bloco c', 'sala 201'), (6, 'bloco c', 'auditório'), (7, 'biblioteca', 'cabine 1'),
	(8, 'biblioteca', 'cabine 2'), (9, 'biblioteca', 'sala grupo a'), (10, 'biblioteca', 'sala grupo b');

insert into Data_Hora_Encontro (id_encontros, inicio_, fim) values
	(1, '08:00:00', '10:00:00'), (2, '14:00:00', '16:00:00'), (3, '18:30:00', '20:30:00'),
	(4, '09:00:00', '11:00:00'), (5, '16:00:00', '18:00:00'), (6, '10:30:00', '12:30:00'),
	(7, '19:00:00', '21:00:00'), (8, '13:00:00', '15:00:00'), (9, '07:30:00', '09:30:00'),
	(10, '15:00:00', '17:00:00');

insert into Solicitante (id_reserva, monitor_solicitante, adm_solicitante) values
	(1, null, 1), (2, null, 2), (3, 11, null), (4, null, 3), (5, null, 4),
	(6, 12, null), (7, 13, null), (8, 14, null), (9, 15, null), (10, null, 5);

insert into Registra (id_inscricao, id_grupo, participantes) values
	(1, 1, 1), (2, 2, 1), (3, 3, 1), (4, 4, 1), (5, 5, 1), (6, 6, 1), (7, 7, 1), (8, 8, 1), (9, 9, 1), (10, 10, 1);

insert into Possui_Disciplina (id_usuario, id_disciplina) values
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

insert into Grupo_Disciplina (id_grupo, id_disciplina) values 
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

insert into Comunidade_Usuario (id_comunidade, id_usuario) values
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15);

insert into Participa (id_usuario, id_grupo, data_inscricao) values
	(1, 2, '2026-03-01'), (2, 1, '2026-02-23'), (3, 4, '2026-01-28'), (4, 3, '2026-05-11'), (5, 6, '2026-12-02'),
	(11, 5, '2026-09-06'), (12, 8, '2026-02-14'), (13, 7, '2026-08-22'), (14, 10, '2026-10-31'), (15, 9, '2026-04-17');

insert into Participa_Encontros (id_usuario, id_encontros) values
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (11, 6), (12, 7), (13, 8), (14, 9), (15, 10);

insert into Adiciona_Materiais (id_grupo, id_material) values
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

insert into Tem_Materiais (id_material, id_disciplina) values
	(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

insert into Envia_Mensagens (id_usuario, id_mensagem, data_envio) values
	(1, 1, '2026-04-25 10:00:00'), (2, 2, '2026-05-28 11:15:00'), (3, 3, '2026-05-11 09:30:00'),
	(4, 4, '2026-05-19 14:22:00'), (5, 5, '2026-05-17 15:40:00'), (11, 6, '2026-05-12 18:01:00'),
	(12, 7, '2026-05-28 20:12:00'), (13, 8, '2026-05-28 21:00:00'), (14, 9, '2026-05-29 08:30:00'),
	(15, 10, '2026-05-21 12:00:00');

insert into Recebe_Mensagens (id_usuario, id_mensagem) values
	(11, 1), (12, 2), (13, 3), (14, 4), (15, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10);


--- Tabelas Base 

	select * from Usuario;
	select * from Disciplina;
	select * from Adiministrador;
	select * from Monitor;
	select * from Grupo;
	select * from Inscricao;
	select * from Encontros;
	select * from Sala;
	select * from Comunidade;
	select * from Material;

--- Tabelas Pequenas

	select * from Chat;
	select * from Avisos;
	select * from Reserva;

--- Tabelas de Encontros

	select * from Virtual;
	select * from Chamada;
	select * from Presencial;
	select * from Local;
	select * from Data_Hora_Encontro;

--- Tabelas de Relacionamentos 

	select * from Solicitante;
	select * from Registra;
	select * from Possui_Disciplina;
	select * from Grupo_Disciplina;
	select * from Comunidade_Usuario;
	select * from Participa;
	select * from Participa_Encontros;
	select * from Adiciona_Materiais;
	select * from Tem_Materiais;
	select * from Envia_Mensagens;
	select * from Recebe_Mensagens;