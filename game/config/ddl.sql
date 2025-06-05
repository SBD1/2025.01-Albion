CREATE DATABASE dbalbion;
USE dbalbion;

CREATE TABLE IF NOT EXISTS USUARIO(
    id_usuario   SERIAL PRIMARY KEY,
    username     VARCHAR(30) NOT NULL,
    senha        VARCHAR(30) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS RACA(
    id_raca            SERIAL PRIMARY KEY,
    nome_raca          VARCHAR(50) NOT NULL,
    mult_defesa        DECIMAL(5,2) NOT NULL,
    mult_ataque_fisico DECIMAL(5,2) NOT NULL,
    mult_ataque_magico DECIMAL(5,2) NOT NULL    
);

CREATE TABLE IF NOT EXISTS PERSONAGEM(
    id_personagem   SERIAL PRIMARY KEY,
    id_raca         INTEGER REFERENCES RACA(idRaca) ON DELETE SET NULL,
    id_sala         INTEGER REFERENCES SALA(idSala) ON DELETE SET NULL,
    nome_personagem VARCHAR(50) NOT NULL,
    nivel           INTEGER NOT NULL,
    experiencia     INTEGER NOT NULL,
    stamina_atual   INTEGER NOT NULL,
    vida_atual      INTEGER NOT NULL,
    stamina_total   INTEGER NOT NULL,
    vida_total      INTEGER NOT NULL,
    defesa          INTEGER NOT NULL,
    ataque_fisico   INTEGER NOT NULL,
    ataque_magico   INTEGER NOT NULL
);


create table fantasmas (
  nome varchar(255) primary key not null,
  task text not null,
  dano int not null
);


-- Correção na tabela habilidades
create table habilidades(
    habilidades_pk int primary key identity(1,1),
    habilidades varchar(255) not null
);

create table personagem(
    nome varchar(255) primary key not null,
    vida int not null,
    estamina int not null,
    nivel int not null,
    forca int not null,
    inteligencia int not null,
    resistencia int not null,
    gold int not null,
    xp int not null,
    sexo varchar(10),
);

-- Correção na tabela controlar
create table controlar(
    fk_fantasma_nome varchar(255) not null,
    fk_personagem_nome varchar(255) not null,
    primary key (fk_fantasma_nome, fk_personagem_nome),
    foreign key (fk_fantasma_nome) references fantasma(nome),
    foreign key (fk_personagem_nome) references personagem(nome)
);

create table sala(
    sala_id int primary key identify(1,1),
);

create table conectado(
    foreign key (fk_personagem_nome) references personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_sala_id) references sala(sala_id)
    int primary key not null,
);

-- Correção na tabela localizado_fantasma
create table localizado_fantasma(
    fk_fantasma_nome varchar(255) not null,
    fk_sala_id int not null,
    primary key (fk_fantasma_nome, fk_sala_id),
    foreign key (fk_fantasma_nome) references fantasma(nome),
    foreign key (fk_sala_id) references sala(sala_id)
);

create table especies(
    especies_tipo int primary key not null identify(1,1),
    qtd_fantasmas int not null,
    qtd_bracos int not null,
);

create table zoiudo(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    qtd_fantasmas int not null,

);

create table titan(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    qtd_bracos int not null,
);

create table espiritualista(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    mana int not null,
);

-- Correção na tabela draconico
create table draconico(
    fk_especie_tipo int not null,
    fk_habilidades_habilidade int not null,
    primary key (fk_especie_tipo),
    foreign key (fk_especie_tipo) references especies(especies_tipo),
    foreign key (fk_habilidades_habilidade) references habilidades(habilidades_pk)
);

create table esta(
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
);

create table inventario(
    inventario_id int primary key identify(1,1) not null,
    slots int not null,
);

create table possui(
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_inventario_id) REFERENCES inventario(inventario_id)
    int primary key not null,
)

create table guarda(
    foreign key (fk_inventario_id) REFERENCES inventario(inventario_id)
    int primary key not null
);

create table itens(
    nome varchar(255) primary key not null
);

create table equipaveis(
    foreign key (fk_itens_nome) REFERENCES itens(nome)
    varchar(255) primary key not null,
    durabilidade_maxima int not null
);

create table nao_equipaveis(
    foreign key (fk_itens_nome) REFERENCES itens(nome)
    varchar(255) primary key not null
);
-- foreing key de itens
create table armadura( 
    foreign key (fk_equipaveis_nome) REFERENCES equipaveis(fk_itens_nome) 
    varchar(255) primary key not null,
    resistencia int not null
);
-- foreing key de itens
create table arma(
    foreign key (fk_equipaveis_nome) REFERENCES equipaveis(fk_itens_nome) 
    varchar(255) primary key not null,
    dano int not null,
    forca int not null
);

create table artefatos(
    foreign key (fk_equipaveis_nome) REFERENCES equipaveis(fk_itens_nome) 
    varchar(255) primary key not null,
    poder_magico int not null,
    mana int not null
);

create table consumiveis(
    nome varchar(255) primary key not null
);

create table nao_consumiveis(
    nome varchar(255) primary key not null
);

-- Correção na tabela instancia
create table instancia(
    id int primary key identity(1,1) not null,
    fk_consumiveis_nome varchar(255),
    fk_equipaveis_nome varchar(255),
    foreign key (fk_consumiveis_nome) references consumiveis(nome),
    foreign key (fk_equipaveis_nome) references equipaveis(fk_itens_nome)
);

create table dungeons(
    dungeons_tipo int primary key identify(1,1) not null,
    nivel int not null
);

create table azul(
    foreign key (fk_dungeons_tipo) REFERENCES dungeons(dungeons_tipo) 
    int primary key not null
);

create table vermelha(
    foreign key (fk_dungeons_tipo) REFERENCES dungeons(dungeons_tipo) 
    int primary key not null
);

create table mapa(
    foreign key (fk_sala_id) REFERENCES sala(sala_id)
    int primary key not null,
    foreign key (fk_dungeons_tipo) REFERENCES dungeons(dungeons_tipo) 
    int primary key not null
);

create table npc(
    nome varchar(255) primary key not null,
    vida int not null,
    dano int not null,
    xp int not null,
    task text
);

create table amigavel(
    fk_npc_nome varchar(255) primary key not null,
    foreign key (fk_npc_nome) references npc(nome)
);

create table boss(
    fk_npc_nome varchar(255) primary key not null,
    foreign key (fk_npc_nome) references npc(nome)
);

create table nao_nomeados(
    fk_npc_nome varchar(255) primary key not null,
    foreign key (fk_npc_nome) references npc(nome)
);

create table localizado_amigavel(
    fk_amigavel_nome varchar(255) not null,
    fk_sala_id int not null,
    primary key (fk_amigavel_nome, fk_sala_id),
    foreign key (fk_amigavel_nome) references amigavel(fk_npc_nome),
    foreign key (fk_sala_id) references sala(sala_id)
);

create table localizado_boss(
    fk_boss_nome varchar(255) not null,
    fk_sala_id int not null,
    primary key (fk_boss_nome, fk_sala_id),
    foreign key (fk_boss_nome) references boss(fk_npc_nome),
    foreign key (fk_sala_id) references sala(sala_id)
);

create table instancia_inimigo(
    id int primary key identity(1,1) not null,
    fk_npc_nome varchar(255) not null,
    foreign key (fk_npc_nome) references npc(nome)
);

create table drop(
    fk_itens_nome varchar(255) not null,
    fk_npc_nome varchar(255) not null,
    primary key (fk_itens_nome, fk_npc_nome),
    foreign key (fk_itens_nome) references itens(nome),
    foreign key (fk_npc_nome) references npc(nome)
);