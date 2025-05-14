# Dicionário de Dados

O dicionário de dados descreve detalhadamente cada tabela e coluna do banco, incluindo nomes, tipos, tamanhos, restrições e descrições. É uma referência essencial para quem for implementar ou manter o banco de dados.

## Versão Final

### Fantasma  
**Descrição:** Armazena cada fantasma que pode ser controlado e a que sala está localizado  
**Observações:** Chave primária Nome, relaciona-se a Controlar e Localizado_Fantasma  

| Nome  | Descrição                                         | Tipo de dado | Tamanho | Restrições de domínio   |
|-------|---------------------------------------------------|--------------|---------|-------------------------|
| Nome  | Identificador do fantasma                         | VARCHAR      | 255     | PK / Not Null           |
| Tasks | Tarefas que o fantasma pode executar              | TEXT         |         |                         |
| Dano  | Quantidade de dano causado pelo fantasma          | INT          |         | Not Null                |

---

### Controlar  
**Descrição:** Define quais fantasmas um personagem controla  
**Observações:** Entidade associativa entre Personagem e Fantasma  

| Nome               | Descrição                          | Tipo de dado | Tamanho | Restrições de domínio   |
|--------------------|------------------------------------|--------------|---------|-------------------------|
| fk_Fantasma_Nome   | Referência a Fantasma(Nome)        | VARCHAR      | 255     | FK / PK / Not Null      |
| fk_Personagem_Nome | Referência a Personagem(Nome)      | VARCHAR      | 255     | FK / PK / Not Null      |

---

### Localizado_Fantasma  
**Descrição:** Posiciona cada fantasma em uma sala específica  
**Observações:** Relaciona Fantasma e Sala  

| Nome             | Descrição                     | Tipo de dado | Tamanho | Restrições de domínio   |
|------------------|-------------------------------|--------------|---------|-------------------------|
| fk_Fantasma_Nome | Referência a Fantasma(Nome)   | VARCHAR      | 255     | FK / PK / Not Null      |
| fk_Sala_ID       | Referência a Sala(ID)         | INT          |         | FK / PK / Not Null      |

---

### Sala  
**Descrição:** Ambientes do jogo onde ocorrem encontros e eventos  
**Observações:** PK gerada automaticamente  

| Nome    | Descrição             | Tipo de dado | Tamanho | Restrições de domínio       |
|---------|-----------------------|--------------|---------|-----------------------------|
| Sala_ID | Identificador da sala | INT          |         | PK / Identity / Not Null    |

---

### Conectado  
**Descrição:** Registra em que sala cada personagem está  
**Observações:** Entidade associativa entre Personagem e Sala  

| Nome                | Descrição                          | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------------|------------------------------------|--------------|---------|-----------------------------|
| fk_Personagem_Nome  | Referência a Personagem(Nome)      | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_Sala_ID          | Referência a Sala(ID)              | INT          |         | FK / PK / Not Null          |

---

### Especies  
**Descrição:** Define espécies (subtipos) de personagens, com atributos próprios  
**Observações:** Relaciona-se a Personagem via “Esta” e possui subtabelas  

| Nome            | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio       |
|-----------------|------------------------------------------|--------------|---------|-----------------------------|
| Especies_TIPO   | Identificador da espécie                 | INT          |         | PK / Identity / Not Null    |
| Qtd_Fantasmas   | Nº máximo de fantasmas controláveis      | INT          |         | Not Null                    |
| Qtd_Bracos      | Nº de braços da espécie                  | INT          |         | Not Null                    |

---

### Zoiudo  
**Descrição:** Subtipo de Especies, herda atributos de Especies  
**Observações:** Tabela filha de Especies  

| Nome             | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|-----------------------------------|--------------|---------|-----------------------------|
| fk_Especies_TIPO | Referência a Especies             | INT          |         | FK / PK / Not Null          |
| Qtd_Fantasmas    | Quantidade de fantasmas permitida | INT          |         | Not Null                    |

---

### Titan  
**Descrição:** Subtipo de Especies com atributo próprio  
**Observações:** Tabela filha de Especies  

| Nome             | Descrição            | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|----------------------|--------------|---------|-----------------------------|
| fk_Especies_TIPO | Referência a Especies| INT          |         | FK / PK / Not Null          |
| Qtd_Bracos       | Quantidade de braços | INT          |         | Not Null                    |

---

### Espiritualista  
**Descrição:** Subtipo de Especies com mana  
**Observações:** Tabela filha de Especies  

| Nome             | Descrição               | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|-------------------------|--------------|---------|-----------------------------|
| fk_Especies_TIPO | Referência a Especies   | INT          |         | FK / PK / Not Null          |
| Mana             | Quantidade de mana inicial | INT       |         | Not Null                    |

---

### Draconico  
**Descrição:** Subtipo de Especies ligado a habilidades  
**Observações:** Tabela filha de Especies  

| Nome                      | Descrição                | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------------------|--------------------------|--------------|---------|-----------------------------|
| fk_Especies_TIPO          | Referência a Especies    | INT          |         | FK / PK / Not Null          |
| fk_Habilidades_Habilidade | Referência a Habilidades | INT          |         | FK / Not Null               |

---

### Esta  
**Descrição:** Vincula Personagem à sua Espécie  
**Observações:** Entidade associativa Personagem – Especies  

| Nome                | Descrição                       | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------------|---------------------------------|--------------|---------|-----------------------------|
| fk_Personagem_Nome  | Referência a Personagem(Nome)   | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_Especies_TIPO    | Referência a Especies           | INT          |         | FK / PK / Not Null          |

---

### Habilidades  
**Descrição:** Lista de habilidades disponíveis para espécies  
**Observações:** PK Identity  

| Nome           | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|----------------|-----------------------------|--------------|---------|-----------------------------|
| Habilidades_PK | Identificador da habilidade | INT          |         | PK / Identity / Not Null    |
| Habilidades    | Descrição da habilidade     | VARCHAR      | 255     | Not Null                    |

---

### Personagem  
**Descrição:** Armazena jogadores e NPCs especiais  
**Observações:** Entidade central — conecta a quase tudo  

| Nome         | Descrição                        | Tipo de dado | Tamanho | Restrições de domínio       |
|--------------|----------------------------------|--------------|---------|-----------------------------|
| Nome         | Identificador do personagem      | VARCHAR      | 255     | PK / Not Null               |
| Vida         | Pontos de vida                   | INT          |         | Not Null                    |
| Estamina     | Pontos de estamina               | INT          |         | Not Null                    |
| Nivel        | Nível atual                      | INT          |         | Not Null                    |
| Forca        | Força física                     | INT          |         | Not Null                    |
| Inteligencia | Capacidade intelectual           | INT          |         | Not Null                    |
| Resistencia  | Resistência física               | INT          |         | Not Null                    |
| Gold         | Ouro carregado                   | INT          |         | Not Null                    |
| XP           | Pontos de experiência            | INT          |         | Not Null                    |
| Sexo         | Sexo do personagem               | VARCHAR      | 10      |                             |

---

### Possui  
**Descrição:** Define qual inventário pertence a cada personagem  
**Observações:** Entidade associativa Personagem – Inventario  

| Nome                | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------------|-----------------------------------|--------------|---------|-----------------------------|
| fk_Personagem_Nome  | Referência a Personagem(Nome)     | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_Inventario_ID    | Referência a Inventario(ID)       | INT          |         | FK / PK / Not Null          |

---

### Inventario  
**Descrição:** Inventários que guardam itens dos personagens  
**Observações:** PK Identity  

| Nome          | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------|-----------------------------|--------------|---------|-----------------------------|
| Inventario_ID | Identificador do inventário | INT          |         | PK / Identity / Not Null    |
| slots         | Número de slots disponíveis | INT          |         | Not Null                    |

---

### Guarda  
**Descrição:** Associa instâncias de item ao inventário  
**Observações:** Entidade associativa Inventario – Instancia  

| Nome             | Descrição                    | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|------------------------------|--------------|---------|-----------------------------|
| fk_Inventario_ID | Referência a Inventario(ID)  | INT          |         | FK / PK / Not Null          |
| fk_Instancia_ID  | Referência a Instancia(ID)   | INT          |         | FK / PK / Not Null          |

---

### Itens  
**Descrição:** Tipos gerais de itens (pai para equipáveis e não equipáveis)  
**Observações:** PK Nome  

| Nome | Descrição               | Tipo de dado | Tamanho | Restrições de domínio       |
|------|-------------------------|--------------|---------|-----------------------------|
| Nome | Identificador do item   | VARCHAR      | 255     | PK / Not Null               |

---

### Equipáveis  
**Descrição:** Itens que podem ser equipados  
**Observações:** Subtabela de Itens  

| Nome            | Descrição                     | Tipo de dado | Tamanho | Restrições de domínio       |
|-----------------|-------------------------------|--------------|---------|-----------------------------|
| fk_Itens_Nome   | Referência a Itens(Nome)      | VARCHAR      | 255     | FK / PK / Not Null          |
| durabilidade_maxima | Durabilidade total do item| INT          |         | Not Null                    |

---

### Não_Equipáveis  
**Descrição:** Itens não equipáveis (ex.: ingredientes)  
**Observações:** Subtabela de Itens  

| Nome          | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------|-----------------------------|--------------|---------|-----------------------------|
| fk_Itens_Nome | Referência a Itens(Nome)    | VARCHAR      | 255     | FK / PK / Not Null          |

---

### Armadura  
**Descrição:** Armamentos defensivos  
**Observações:** Subtabela de Equipáveis  

| Nome               | Descrição                     | Tipo de dado | Tamanho | Restrições de domínio       |
|--------------------|-------------------------------|--------------|---------|-----------------------------|
| fk_Equipáveis_Nome | Referência a Equipáveis(Nome) | VARCHAR      | 255     | FK / PK / Not Null          |
| Resistencia        | Valor de resistência adicionada | INT        |         | Not Null                    |

---

### Arma  
**Descrição:** Itens ofensivos de curto ou longo alcance  
**Observações:** Subtabela de Equipáveis  

| Nome               | Descrição           | Tipo de dado | Tamanho | Restrições de domínio       |
|--------------------|---------------------|--------------|---------|-----------------------------|
| fk_Equipáveis_Nome | Referência a Equipáveis(Nome) | VARCHAR| 255   | FK / PK / Not Null          |
| Dano               | Valor de dano causado | INT        |         | Not Null                    |
| Forca              | Bônus de força exigido| INT        |         | Not Null                    |

---

### Artefatos  
**Descrição:** Itens mágicos com poderes especiais  
**Observações:** Subtabela de Equipáveis  

| Nome               | Descrição                  | Tipo de dado | Tamanho | Restrições de domínio       |
|--------------------|----------------------------|--------------|---------|-----------------------------|
| fk_Equipáveis_Nome | Referência a Equipáveis(Nome) | VARCHAR  | 255     | FK / PK / Not Null          |
| Poder_Magico       | Bônus de poder mágico      | INT          |         | Not Null                    |
| Mana               | Bônus de mana              | INT          |         | Not Null                    |

---

### Consumíveis  
**Descrição:** Itens que desaparecem ao usar  
**Observações:** Subtabela de Não_Equipáveis  

| Nome | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|------|-----------------------------|--------------|---------|-----------------------------|
| Nome | Identificador do consumível| VARCHAR      | 255     | PK / Not Null               |

---

### Não_Consumíveis  
**Descrição:** Itens não consumíveis (moedas, chaves, etc.)  
**Observações:** Subtabela de Não_Equipáveis  

| Nome | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|------|-----------------------------|--------------|---------|-----------------------------|
| Nome | Identificador do item       | VARCHAR      | 255     | PK / Not Null               |

---

### Instancia  
**Descrição:** Instâncias concretas de itens no inventário  
**Observações:** FKs para cada subtipo de item  

| Nome                 | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio       |
|----------------------|-------------------------------------------|--------------|---------|-----------------------------|
| ID                   | Identificador da instância                | INT          |         | PK / Identity / Not Null    |
| fk_Consumíveis_Nome  | Consumível usado (se houver)              | VARCHAR      | 255     | FK                          |
| fk_Equipáveis_Nome   | Equipável usado (se houver)               | VARCHAR      | 255     | FK                          |

---

### Dungeons  
**Descrição:** Zonas de desafio com inimigos  
**Observações:** PK Identity, subtabelas Azul e Vermelha  

| Nome           | Descrição                    | Tipo de dado | Tamanho | Restrições de domínio       |
|----------------|------------------------------|--------------|---------|-----------------------------|
| Dungeons_TIPO  | Identificador da dungeon     | INT          |         | PK / Identity / Not Null    |
| Nivel          | Nível de dificuldade         | INT          |         | Not Null                    |

---

### Azul  
**Descrição:** Subtabela de Dungeons (cor Azul)  
**Observações:** Herda PK de Dungeons  

| Nome              | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|-------------------|--------------------------------|--------------|---------|-----------------------------|
| fk_Dungeons_TIPO  | Referência a Dungeons          | INT          |         | FK / PK / Not Null          |

---

### Vermelha  
**Descrição:** Subtabela de Dungeons (cor Vermelha)  
**Observações:** Herda PK de Dungeons  

| Nome              | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|-------------------|--------------------------------|--------------|---------|-----------------------------|
| fk_Dungeons_TIPO  | Referência a Dungeons          | INT          |         | FK / PK / Not Null          |

---

### Mapa  
**Descrição:** Relaciona salas a dungeons  
**Observações:** Entidade associativa Sala – Dungeons  

| Nome               | Descrição                       | Tipo de dado | Tamanho | Restrições de domínio       |
|--------------------|---------------------------------|--------------|---------|-----------------------------|
| fk_Sala_ID         | Referência a Sala(ID)           | INT          |         | FK / PK / Not Null          |
| fk_Dungeons_TIPO   | Referência a Dungeons(ID)       | INT          |         | FK / PK / Not Null          |

---

### NPC  
**Descrição:** Personagens não-jogáveis (pai de Amigável e Inimigos)  
**Observações:** PK Nome  

| Nome  | Descrição                 | Tipo de dado | Tamanho | Restrições de domínio       |
|-------|---------------------------|--------------|---------|-----------------------------|
| Nome  | Identificador do NPC      | VARCHAR      | 255     | PK / Not Null               |
| Vida  | Pontos de vida            | INT          |         | Not Null                    |
| Dano  | Dano causado              | INT          |         | Not Null                    |
| XP    | Experiência concedida     | INT          |         | Not Null                    |
| Tasks | Tarefas/comportamentos    | TEXT         |         |                             |

---

### Amigavel  
**Descrição:** NPC que ajuda o jogador  
**Observações:** Subtabela de NPC  

| Nome             | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|--------------------------------|--------------|---------|-----------------------------|
| fk_NPC_Nome      | Referência a NPC(Nome)         | VARCHAR      | 255     | FK / PK / Not Null          |

---

### Boss  
**Descrição:** NPC chefe de incursões  
**Observações:** Subtabela de Inimigos  

| Nome             | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|--------------------------------|--------------|---------|-----------------------------|
| fk_NPC_Nome      | Referência a NPC(Nome)         | VARCHAR      | 255     | FK / PK / Not Null          |

---

### Não_Nomeados  
**Descrição:** Inimigos comuns (não chefes)  
**Observações:** Subtabela de Inimigos  

| Nome             | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|------------------|--------------------------------|--------------|---------|-----------------------------|
| fk_NPC_Nome      | Referência a NPC(Nome)         | VARCHAR      | 255     | FK / PK / Not Null          |

---

### Localizado_Amigavel  
**Descrição:** Posiciona NPCs amigáveis em salas  
**Observações:** Entidade associativa Amigavel – Sala  

| Nome                | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio       |
|---------------------|-----------------------------------|--------------|---------|-----------------------------|
| fk_Amigavel_Nome    | Referência a Amigavel(Nome)       | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_Sala_ID          | Referência a Sala(ID)             | INT          |         | FK / PK / Not Null          |

---

### Localizado_Boss  
**Descrição:** Posiciona Bosses em salas  
**Observações:** Entidade associativa Boss – Sala  

| Nome            | Descrição                   | Tipo de dado | Tamanho | Restrições de domínio       |
|-----------------|-----------------------------|--------------|---------|-----------------------------|
| fk_Boss_Nome    | Referência a Boss(Nome)     | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_Sala_ID      | Referência a Sala(ID)       | INT          |         | FK / PK / Not Null          |

---

### Instancia_Inimigo  
**Descrição:** Instâncias concretas de NPCs inimigos  
**Observações:** Relaciona Nao_Nomeados e Boss  

| Nome           | Descrição                      | Tipo de dado | Tamanho | Restrições de domínio       |
|----------------|--------------------------------|--------------|---------|-----------------------------|
| ID             | Identificador da instância     | INT          |         | PK / Identity / Not Null    |
| fk_NPC_Nome    | Referência a NPC(Nome)         | VARCHAR      | 255     | FK / Not Null               |

---

### Drop  
**Descrição:** Define que itens podem dropar de quais NPCs  
**Observações:** Entidade associativa Itens – NPC  

| Nome            | Descrição                         | Tipo de dado | Tamanho | Restrições de domínio       |
|-----------------|-----------------------------------|--------------|---------|-----------------------------|
| fk_Itens_Nome   | Referência a Itens(Nome)          | VARCHAR      | 255     | FK / PK / Not Null          |
| fk_NPC_Nome     | Referência a NPC(Nome)            | VARCHAR      | 255     | FK / PK / Not Null          |

Para maior liberdade de visualização, veja pela versão PDF. <br>
[Confira o PDF aqui](../../assets/dicionarioDadosV2.pdf)

## Versões Anteriores
- [Versão 1](../../assets/dicionarioDadosV1.pdf)
- [Versão 2 (Final)](../../assets/dicionarioDadosV2.pdf)