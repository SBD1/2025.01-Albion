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



create table fantasma(
    nome varchar(255) primary key not null,
    task text not null,
    dano int not null
);

create table habilidades(
    habilidades_pk primary key int identify(1,1),
    habidades varchar(255) not null
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
    sexo varchar(10)
);

create table controlar(
    foreign key (fk_fantasma_nome) REFERENCES fantasma(nome) 
    varchar(255) primary key not null,
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null
);

create table sala(
    sala_id int primary key identify(1,1)
);

create table conectado(
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_sala_id) REFERENCES sala(sala_id)
    int primary key not null
);

create table localizado_fantasma(
    foreign key (fk_fantasma_nome) REFERENCES fantasma(nome)
    varchar(255) primary key not null,
    foreign key (fk_sala_id) REFERENCES sala(id) 
    int primary key not null
);

create table especies(
    especies_tipo int primary key not null identify(1,1),
    qtd_fantasmas int not null,
    qtd_bracos int not null
);

create table zoiudo(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    qtd_fantasmas int not null

);

create table titan(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    qtd_bracos int not null
);

create table espiritualista(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    mana int not null
);

create table draconico(
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null,
    foreign key (fk_habilidades_habilidade) REFERENCES habilidade(habilidades)
    int not null
);

create table esta(
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_especie_tipo) REFERENCES especies(especies_tipo)
    int primary key not null
);

create table inventario(
    inventario_id int primary key identify(1,1) not null,
    slots int not null
);

create table possui(
    foreign key (fk_personagem_nome) REFERENCES personagem(nome)
    varchar(255) primary key not null,
    foreign key (fk_inventario_id) REFERENCES inventario(inventario_id)
    int primary key not null
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

create table instancia(
    id int primary key identify(1,1) not null,
    foreign key (fk_consumiveis_nome) REFERENCES consumiveis(nome) 
    varchar(255) not null,
    foreign key (fk_equipaveis_nome) REFERENCES equipaveis(fk_itens_nome) 
    varchar(255) not null
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