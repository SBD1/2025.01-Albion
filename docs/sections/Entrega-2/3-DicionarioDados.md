## Estrutura da Tabela USUARIO

| Campo         | Tipo        | Obrigatório | Chave  | Valor Padrão         | Unicidade | Descrição                                                                 |
|---------------|-------------|-------------|--------|----------------------|-----------|---------------------------------------------------------------------------|
| `id_usuario`  | SERIAL      | Sim         | PK     | Auto-incremento      | Sim       | Identificador único automático do usuário                                 |
| `username`    | VARCHAR(30) | Sim         | -      | -                    | Sim (UK)  | Nome de usuário para login (único no sistema)                             |
| `password`    | VARCHAR(30) | Sim         | -      | -                    | Não       | Senha de acesso (armazenamento em texto puro - recomendado usar hash)    |
| `data_criacao`| TIMESTAMP   | Não         | -      | CURRENT_TIMESTAMP    | Não       | Registro automático da data/hora de criação do usuário



## Estrutura da Tabela SALA

### Descrição
Tabela que armazena as salas do ambiente virtual e suas interconexões (representando um mapa/grid)

| Campo            | Tipo         | Obrigatório | Chave  | Valor Padrão | Descrição                                                                 |
|------------------|--------------|-------------|--------|--------------|---------------------------------------------------------------------------|
| `id_sala`       | SERIAL       | Sim         | PK     | Auto-incremento | Identificador único automático da sala                                   |
| `nome`          | VARCHAR(50)  | Sim         | -      | -            | Nome descritivo da sala (ex: "Hall Principal", "Dungeon Secreto")        |
| `descricao`     | TEXT         | Não         | -      | -            | Descrição detalhada do ambiente (aparece quando o jogador entra na sala) |
| `conexao_norte` | INTEGER      | Não         | FK     | -            | Referência à sala conectada ao norte (`id_sala` da sala vizinha)         |
| `conexao_sul`   | INTEGER      | Não         | FK     | -            | Referência à sala conectada ao sul                                       |
| `conexao_leste` | INTEGER      | Não         | FK     | -            | Referência à sala conectada ao leste                                     |
| `conexao_oeste` | INTEGER      | Não         | FK     | -            | Referência à sala conectada ao oeste




## Estrutura da Tabela ITEM

### Descrição
Tabela que armazena os itens disponíveis no jogo, com sua categorização básica e propriedades
| Campo         | Tipo         | Obrigatório | Chave  | Valor Padrão | Valores Permitidos               | Descrição                                                                 |
|---------------|--------------|-------------|--------|--------------|----------------------------------|---------------------------------------------------------------------------|
| `id_item`    | SERIAL       | Sim         | PK     | Auto-incremento | -                              | Identificador único automático do item                                   |
| `nome`       | VARCHAR(50)  | Sim         | -      | -            | -                              | Nome do item (ex: "Espada Longa", "Poção de Cura")                       |
| `descricao`  | TEXT         | Não         | -      | -            | -                              | Descrição detalhada do item (aparece no inventário)                      |
| `nivel`      | INTEGER      | Sim         | -      | -            | Números inteiros positivos      | Nível do item (indica poder/raridade)                                   |
| `tipo_item`  | VARCHAR(50)  | Sim         | -      | -            | 'Equipavel', 'Nao-Equipavel'   | Categoria principal que define se o item pode ser equipado              |



## Estrutura da Tabela EQUIPAVEL

### Descrição
Tabela especializada que armazena atributos específicos de itens equipáveis, herda a relação básica da tabela ITEM


| Campo                 | Tipo         | Obrigatório | Chave         | Valor Padrão | Valores Permitidos               | Descrição                                                                 |
|-----------------------|--------------|-------------|---------------|--------------|----------------------------------|---------------------------------------------------------------------------|
| `id_item`            | INTEGER      | Sim         | PK, FK        | -            | -                              | Chave estrangeira que referencia o item geral (herança)                 |
| `durabilidade_maxima`| INTEGER      | Sim         | -             | -            | Valores positivos              | Durabilidade máxima do equipamento antes de quebrar                     |
| `tipo_equipavel`     | VARCHAR(50)  | Sim         | -             | -            | 'Arma', 'Armadura', 'Artefato' | Especialização do tipo de equipamento                                   |




## Estrutura da Tabela ARMA
### Descrição
Tabela especializada que armazena atributos específicos de itens do tipo arma, herda da hierarquia EQUIPAVEL → ITEM
| Campo                     | Tipo    | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------------|---------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_item`                | INTEGER | Sim         | PK, FK        | -            | Chave estrangeira que referencia o item equipável                        |
| `aumento_ataque_fisico`  | INTEGER | Sim         | -             | -            | Valor adicional de ataque físico proporcionado pela arma                 |


## Estrutura da Tabela ARMADURA

### Descrição
Tabela especializada que armazena atributos de defesa para itens do tipo armadura, completando a hierarquia EQUIPAVEL → ITEM



| Campo                     | Tipo    | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------------|---------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_item`                | INTEGER | Sim         | PK, FK        | -            | Chave estrangeira que referencia o item equipável                        |
| `aumento_defesa_fisica`  | INTEGER | Sim         | -             | 0            | Bônus de defesa contra ataques físicos                                   |
| `aumento_defesa_magica`  | INTEGER | Sim         | -             | 0            | Bônus de defesa contra ataques mágicos                                   |
| `aumento_vida_maxima`    | INTEGER | Sim         | -             | 0            | Aumento adicional nos pontos de vida máxima do personagem 




## Estrutura da Tabela ARTEFATO

### Descrição
Tabela especializada para itens mágicos/artefatos que fornecem benefícios mágicos, completando a hierarquia EQUIPAVEL → ITEM

| Campo                     | Tipo    | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------------|---------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_item`                | INTEGER | Sim         | PK, FK        | -            | Chave estrangeira que referencia o item equipável                        |
| `aumento_ataque_magico`  | INTEGER | Sim         | -             | -            | Bônus de ataque mágico proporcionado pelo artefato                       |
| `mana_maxima`            | INTEGER | Sim         | -             | -            | Aumento na capacidade máxima de mana do personagem                       |






## Estrutura da Tabela NEQUIPAVEL

### Descrição
Tabela especializada para itens não equipáveis, completando a hierarquia de tipos de itens do sistema

| Campo               | Tipo          | Obrigatório | Chave         | Valor Padrão | Valores Permitidos   | Descrição                                                                 |
|---------------------|---------------|-------------|---------------|--------------|----------------------|---------------------------------------------------------------------------|
| `id_item`          | INTEGER       | Sim         | PK, FK        | -            | -                    | Chave estrangeira que referencia o item base                             |
| `tipo_nequipavel`  | VARCHAR(100)  | Sim         | -             | -            | 'Comida', 'Pocao'    | Categoria de item não equipável                                          |



## Estrutura da Tabela COMIDA

### Descrição
Tabela especializada para itens de comida que restauram atributos do personagem, completando a hierarquia NEQUIPAVEL → ITEM

| Campo                     | Tipo    | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------------|---------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_item`                | INTEGER | Sim         | PK, FK        | -            | Chave estrangeira que referencia o item não equipável                    |
| `aumento_vida_atual`     | INTEGER | Sim         | -             | -            | Quantidade de vida restaurada ao consumir                                |
| `aumento_stamina_atual`  | INTEGER | Sim         | -             | -            | Quantidade de stamina restaurada ao consumir        





## Estrutura da Tabela POCAO

## Descrição
Tabela especializada para itens do tipo poção que restauram/manipulam atributos mágicos, completando a hierarquia NEQUIPAVEL → ITEM


| Campo                 | Tipo    | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|-----------------------|---------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_item`            | INTEGER | Sim         | PK, FK        | -            | Chave estrangeira que referencia o item não equipável                    |
| `aumento_mana_atual` | INTEGER | Sim         | -             | -            | Quantidade de mana restaurada ao consumir a poção                        |




## Estrutura da Tabela INSTANCIA_ITEM

### Descrição
Tabela que gerencia as instâncias concretas dos itens no jogo, incluindo seu estado atual (durabilidade, quantidade) e vinculação ao template base (ITEM)



| Campo                | Tipo     | Obrigatório | Chave  | Valor Padrão | Restrições                     | Descrição                                                                 |
|----------------------|----------|-------------|--------|--------------|--------------------------------|---------------------------------------------------------------------------|
| `id_instancia`      | SERIAL   | Sim         | PK     | Auto-incremento | -                            | Identificador único da instância do item                                 |
| `id_item`          | INTEGER  | Sim         | FK     | -            | REFERENCES ITEM(id_item)      | Referência ao template base do item                                      |
| `durabilidade_atual`| INTEGER  | Não         | -      | -            | -                            | Estado atual de durabilidade (apenas para itens equipáveis)             |
| `quantidade`       | INTEGER  | Sim         | -      | 1            | CHECK (quantidade >= 1)      | Quantidade de itens nesta instância (para stackables) 




## Estrutura da Tabela PERSONAGEM

### Descrição
Tabela central que armazena todos os atributos dos personagens jogáveis, incluindo progressão, estatísticas e localização atual


| Campo               | Tipo         | Obrigatório | Chave  | Valor Padrão | Referência                     | Descrição                                                                 |
|---------------------|--------------|-------------|--------|--------------|--------------------------------|---------------------------------------------------------------------------|
| `id_personagem`    | SERIAL       | Sim         | PK     | Auto-incremento | -                            | Identificador único do personagem                                        |
| `id_usuario`      | INTEGER      | Sim         | FK     | -            | REFERENCES USUARIO(id_usuario) | Dono do personagem                                                       |
| `id_sala`         | INTEGER      | Não         | FK     | 1            | REFERENCES SALA(id_sala) ON DELETE SET DEFAULT | Localização atual no mapa                                               |
| `nome`            | VARCHAR(50)  | Sim         | UK     | -            | -                            | Nome do personagem (único no servidor)                                   |
| `nivel`           | INTEGER      | Não         | -      | 1            | -                            | Nível atual de progressão                                               |
| `qtd_ouro`       | INTEGER      | Não         | -      | 0            | -                            | Quantidade de moedas de ouro possuídas                                  |
| `exp_maxima`     | INTEGER      | Não         | -      | 100          | -                            | Experiência necessária para próximo nível                               |
| `exp_atual`      | INTEGER      | Não         | -      | 0            | -                            | Experiência acumulada no nível atual                                    |
| `vida_atual`     | INTEGER      | Não         | -      | 100          | -                            | Pontos de vida atuais                                                   |
| `vida_maxima`    | INTEGER      | Não         | -      | 100          | -                            | Pontos de vida máximos                                                  |
| `stamina_atual`  | INTEGER      | Não         | -      | 100          | -                            | Energia atual para ações                                                |
| `stamina_maxima` | INTEGER      | Não         | -      | 100          | -                            | Energia máxima                                                          |
| `ataque_fisico`  | INTEGER      | Não         | -      | 10           | -                            | Poder de ataque físico                                                  |
| `defesa_fisica`  | INTEGER      | Não         | -      | 20           | -                            | Resistência a dano físico                                               |
| `defesa_magica`  | INTEGER      | Não         | -      | 20           | -                            | Resistência a dano mágico                                               |




## Estrutura da Tabela FANTASMA

### Descrição
Tabela que armazena os atributos dos fantasmas (NPCs ou inimigos) no jogo, incluindo suas capacidades de combate e progressão

| Campo               | Tipo         | Obrigatório | Chave  | Valor Padrão | Descrição                                                                 |
|---------------------|--------------|-------------|--------|--------------|---------------------------------------------------------------------------|
| `id_fantasma`      | SERIAL       | Sim         | PK     | Auto-incremento | Identificador único do fantasma                                         |
| `nome`             | VARCHAR(20)  | Não         | -      | NULL         | Nome ou tipo do fantasma (ex: "Assombração", "Espectro")                |
| `nivel`            | INTEGER      | Não         | -      | 1            | Nível de poder do fantasma                                              |
| `exp_maxima`       | INTEGER      | Não         | -      | 100          | Experiência máxima no nível atual                                       |
| `exp_atual`        | INTEGER      | Não         | -      | 0            | Experiência acumulada                                                   |
| `ataque_fisico`    | INTEGER      | Não         | -      | 1            | Dano físico causado pelo fantasma                                       |
| `ataque_magico`    | INTEGER      | Não         | -      | 10           | Dano mágico causado pelo fantasma                                       |
| `defesa_fisica`    | INTEGER      | Não         | -      | 10           | Resistência a ataques físicos                                           |
| `defesa_magica`    | INTEGER      | Não         | -      | 10           | Resistência a ataques mágicos                                           |



## Estrutura da Tabela ZOIUDO

### Descrição
Tabela de associação que estabelece uma relação única entre personagens jogáveis e fantasmas, possivelmente para representar um sistema de posse, companheiro ou transformação



| Campo               | Tipo         | Obrigatório | Chave         | Valor Padrão | Referência                              | Descrição                                                                 |
|---------------------|--------------|-------------|---------------|--------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_zoiudo`        | SERIAL       | Sim         | PK            | Auto-incremento | -                                     | Identificador único da relação                                          |
| `id_personagem`    | INTEGER      | Sim         | FK, UK        | -            | REFERENCES PERSONAGEM(id_personagem) ON DELETE CASCADE | Personagem associado (relação 1:1)                                      |
| `id_fantasma`      | INTEGER      | Não         | FK, UK        | -            | REFERENCES FANTASMA(id_fantasma)       | Fantasma associado (opcional, mas único)                                |



## Estrutura da Tabela ESPIRITUALISTA

## Descrição
Tabela especializada que estende os atributos de personagens para aqueles com habilidades mágicas/espirituais, incluindo gerenciamento de mana e equipamento mágico



| Campo                 | Tipo     | Obrigatório | Chave         | Valor Padrão | Referência                              | Descrição                                                                 |
|-----------------------|----------|-------------|---------------|--------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_espiritualista`  | SERIAL   | Sim         | PK            | Auto-incremento | -                                     | Identificador único do espiritualista                                   |
| `id_personagem`      | INTEGER  | Sim         | FK, UK        | -            | REFERENCES PERSONAGEM(id_personagem) ON DELETE CASCADE | Referência ao personagem base (relação 1:1)                             |
| `mana_total`         | INTEGER  | Não         | -             | 100          | -                                     | Capacidade máxima de mana                                               |
| `mana_atual`         | INTEGER  | Não         | -             | 100          | -                                     | Mana disponível no momento                                              |
| `ataque_magico`      | INTEGER  | Não         | -             | 10           | -                                     | Poder de ataque mágico base                                             |
| `slot_artefato`      | INTEGER  | Não         | FK, UK        | -            | REFERENCES INSTANCIA_ITEM(id_instancia) | Artefato mágico equipado (opcional)                                     |




## Estrutura da Tabela DRACONICO

## Descrição
Tabela especializada para personagens com habilidades de transformação dragônica, gerenciando os atributos e limitações desta forma poderosa


| Campo                     | Tipo     | Obrigatório | Chave         | Valor Padrão | Referência                              | Descrição                                                                 |
|---------------------------|----------|-------------|---------------|--------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_draconico`           | SERIAL   | Sim         | PK            | Auto-incremento | -                                     | Identificador único da especialização draconica                         |
| `id_personagem`          | INTEGER  | Sim         | FK, UK        | -            | REFERENCES PERSONAGEM(id_personagem) ON DELETE CASCADE | Referência ao personagem base (relação 1:1)                             |
| `turnos_maximo_dragao`   | INTEGER  | Não         | -             | 3            | -                                     | Duração máxima da transformação em turnos                               |
| `turnos_recarga`         | INTEGER  | Não         | -             | 5            | -                                     | Turnos necessários para recarregar a habilidade                         |
| `custo_stamina`          | INTEGER  | Não         | -             | 50           | -                                     | Custo em stamina para ativar a transformação                            |
| `aumento_vida_atual`     | INTEGER  | Não         | -             | 20           | -                                     | Bônus de vida ao transformar                                            |
| `aumento_ataque_fisico`  | INTEGER  | Não         | -             | 20           | -                        
             | Bônus de ataque físico ao transformar
             
             
             


## Estrutura da Tabela TITAN

### Descrição
Tabela especializada para personagens com habilidades titânicas, permitindo equipamento de múltiplas armas 
simultaneamente e representando guerreiros de grande porte


| Campo                 | Tipo     | Obrigatório | Chave         | Valor Padrão | Referência                              | Descrição                                                                 |
|-----------------------|----------|-------------|---------------|--------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_titan`           | SERIAL   | Sim         | PK            | Auto-incremento | -                                     | Identificador único da especialização titânica                          |
| `id_personagem`      | INTEGER  | Sim         | FK, UK        | -            | REFERENCES PERSONAGEM(id_personagem) ON DELETE CASCADE | Referência ao personagem base (relação 1:1)                             |
| `slot_extra_arma_1`  | INTEGER  | Não         | FK, UK        | -            | REFERENCES INSTANCIA_ITEM(id_instancia) | Primeira arma adicional equipada (opcional)                             |
| `slot_extra_arma_2`  | INTEGER  | Não         | FK, UK        | -            | REFERENCES INSTANCIA_ITEM(id_instancia) | Segunda arma adicional equipada (opcional)                              |



## Estrutura da Tabela INVENTARIO

### Descrição
Tabela que gerencia a capacidade de armazenamento de itens dos personagens, estabelecendo os limites de seu inventário

| Campo               | Tipo     | Obrigatório | Chave         | Valor Padrão | Referência                              | Descrição                                                                 |
|---------------------|----------|-------------|---------------|--------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_personagem`    | INTEGER  | Sim         | PK, FK        | -            | REFERENCES PERSONAGEM(id_personagem)    | Identificador do personagem dono do inventário (relação 1:1)             |
| `capacidade`       | INTEGER  | Não         | -             | 10           | -                                     | Número máximo de slots no inventário 



## Estrutura da Tabela INVENTARIO_ITENS

### Descrição
Tabela associativa que gerencia os itens contidos nos inventários dos personagens, estabelecendo relações muitos-para-muitos entre personagens e instâncias de itens

| Campo               | Tipo     | Obrigatório | Chave         | Referência                              | Descrição                                                                 |
|---------------------|----------|-------------|---------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_personagem`    | INTEGER  | Sim         | PK, FK        | REFERENCES INVENTARIO(id_personagem)    | Identificador do personagem dono do item                                 |
| `id_instancia`     | INTEGER  | Sim         | PK, FK, UK    | REFERENCES INSTANCIA_ITEM(id_instancia) | Instância específica do item no inventário (única no sistema)           |





## Estrutura da Tabela INVENTARIO_EQUIPADOS

### Descrição
Tabela que gerencia os itens atualmente equipados pelos personagens, organizados por slots específicos de equipamento

| Campo                     | Tipo     | Obrigatório | Chave         | Referência                              | Descrição                                                                 |
|---------------------------|----------|-------------|---------------|-----------------------------------------|---------------------------------------------------------------------------|
| `id_personagem`          | INTEGER  | Sim         | PK, FK        | REFERENCES PERSONAGEM(id_personagem)    | Identificador do personagem (relação 1:1)                                |
| `slot_arma`             | INTEGER  | Não         | FK, UK        | REFERENCES INSTANCIA_ITEM(id_instancia) | Arma principal equipada                                                  |
| `slot_armadura_peitoral`| INTEGER  | Não         | FK, UK        | REFERENCES INSTANCIA_ITEM(id_instancia) | Armadura de torso equipada                                               |
| `slot_armadura_capacete`| INTEGER  | Não         | FK, UK        | REFERENCES INSTANCIA_ITEM(id_instancia) | Capacete ou proteção de cabeça equipada                                  |
| `slot_armadura_escudo`  | INTEGER  | Não         | FK, UK        | REFERENCES INSTANCIA_ITEM(id_instancia) | Escudo ou proteção secundária equipada




## Estrutura da Tabela NPC

### Descrição
Tabela que armazena os personagens não-jogáveis (NPCs) do jogo, com sua classificação e características básicas

| Campo       | Tipo         | Obrigatório | Chave  | Valor Padrão | Valores Permitidos       | Descrição                                                                 |
|-------------|--------------|-------------|--------|--------------|--------------------------|---------------------------------------------------------------------------|
| `id_npc`   | SERIAL       | Sim         | PK     | Auto-incremento | -                      | Identificador único do NPC                                              |
| `especie`  | VARCHAR(50)  | Sim         | -      | -            | -                      | Espécie ou raça do NPC (ex: "Humano", "Elfo", "Orc")                   |
| `nome`     | VARCHAR(50)  | Não         | UK     | -            | -                      | Nome único do NPC (para NPCs únicos)                                    |
| `tipo`     | VARCHAR(30)  | Sim         | -      | -            | 'UNICO', 'GENERICO'     | Classificação do NPC (únicos têm nome, genéricos são repetíveis)        |




## Estrutura da Tabela NPC_UNICO

## Descrição
Tabela especializada para NPCs únicos no jogo, com posicionamento fixo no mapa e classificação específica

| Campo        | Tipo     | Obrigatório | Chave         | Descrição                                                                 |
|--------------|----------|-------------|---------------|---------------------------------------------------------------------------|
| `id_npc`    | INTEGER  | Sim         | PK, FK        | Referência ao NPC base (deve ser do tipo 'UNICO')                        |
| `posicao_x` | INTEGER  | Sim         | UK (composta) | Coordenada X no mapa (sistema de grid)                                   |
| `posicao_y` | INTEGER  | Sim         | UK (composta) | Coordenada Y no mapa (sistema de grid)                                   |
| `tipo`      | VARCHAR(20) | Sim       | -             | Classificação do NPC único ('BOSS' ou 'AMIGAVEL')    






## Estrutura da Tabela NPC_BOSS

### Descrição
Tabela especializada para bosses do jogo, contendo atributos de combate avançados e recompensas de experiência

| Campo             | Tipo     | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|-------------------|----------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_npc`         | INTEGER  | Sim         | PK, FK        | -            | Referência ao NPC único (deve ser do tipo 'BOSS')                        |
| `xp`             | INTEGER  | Sim         | -             | -            | Experiência concedida ao derrotar o boss                                 |
| `vida_maxima`    | INTEGER  | Não         | -             | 100          | Pontos de vida máximos                                                   |
| `vida_atual`     | INTEGER  | Não         | -             | 100          | Pontos de vida atuais                                                    |
| `ataque_fisico`  | INTEGER  | Não         | -             | 0            | Dano físico causado                                                      |
| `ataque_magico`  | INTEGER  | Não         | -             | 0            | Dano mágico causado                                                      |
| `defesa_fisica`  | INTEGER  | Não         | -             | 0            | Resistência a dano físico                                                |
| `defesa_magica`  | INTEGER  | Não         | -             | 0            | Resistência a dano mágico                                                |

 


## Estrutura da Tabela NPC_AMIGAVEL

### Descrição
Tabela especializada para NPCs únicos amigáveis, com informações sobre suas facções e alinhamentos


| Campo       | Tipo         | Obrigatório | Chave         | Valores Permitidos                     | Descrição                                                                 |
|-------------|--------------|-------------|---------------|----------------------------------------|---------------------------------------------------------------------------|
| `id_npc`   | INTEGER      | Sim         | PK, FK        | -                                      | Referência ao NPC único (deve ser do tipo 'AMIGAVEL')                    |
| `faccao`   | VARCHAR(50)  | Não         | -             | 'Culto das Sombras', 'Igreja da Luz'   | Facção a qual o NPC pertence (opcional)                                  |






## Estrutura da Tabela NPC_GENERICO

### Descrição
Tabela especializada para NPCs genéricos do jogo, contendo atributos básicos de combate e recompensas


| Campo             | Tipo     | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|-------------------|----------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_npc`         | INTEGER  | Sim         | PK, FK        | -            | Referência ao NPC base (deve ser do tipo 'GENERICO')                     |
| `xp`             | INTEGER  | Sim         | -             | -            | Experiência concedida ao derrotar o NPC                                  |
| `vida_maxima`    | INTEGER  | Não         | -             | 100          | Pontos de vida máximos                                                   |
| `ataque_fisico`  | INTEGER  | Não         | -             | 0            | Dano físico causado                                                      |
| `ataque_magico`  | INTEGER  | Não         | -             | 0            | Dano mágico causado                                                      |
| `defesa_fisica`  | INTEGER  | Não         | -             | 0            | Resistência a dano físico                                                |
| `defesa_magica`  | INTEGER  | Não         | -             | 0            | Resistência a dano mágico                                                |




## Estrutura da Tabela INSTANCIA_NPC_GENERICO

### Descrição
Tabela que gerencia as instâncias ativas de NPCs genéricos no mundo do jogo, incluindo seu estado atual e posicionamento

| Campo               | Tipo     | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------|----------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_instancia`     | SERIAL   | Sim         | PK            | Auto-incremento | Identificador único da instância                                        |
| `id_npc`          | INTEGER  | Sim         | FK            | -            | Referência ao template do NPC genérico                                   |
| `vida_atual`      | INTEGER  | sim         | -             | 100          | Pontos de vida atuais da instância                                       |
| `posicao_x`       | INTEGER  | Sim         | UK (composta) | -            | Coordenada X no mapa (sistema de grid)                                   |
| `posicao_y`       | INTEGER  | Sim         | UK (composta) | -            | Coordenada Y no mapa (sistema de grid)  





## Estrutura da Tabela QUEST

### Descrição
Tabela que armazena as missões disponíveis no jogo, vinculadas a NPCs amigáveis com requisitos e objetivos específicos


| Campo            | Tipo          | Obrigatório | Chave  | Valor Padrão | Descrição                                                                 |
|------------------|---------------|-------------|--------|--------------|---------------------------------------------------------------------------|
| `id_quest`      | SERIAL        | Sim         | PK     | Auto-incremento | Identificador único da missão                                           |
| `id_npc`       | INTEGER       | Sim         | FK     | -            | NPC que oferece a missão (deve ser amigável)                             |
| `objetivo`     | VARCHAR(250)  | Sim         | -      | -            | Descrição do objetivo da missão                                          |
| `nivel_minimo` | INTEGER       | sim         | -      | 1            | Nível mínimo necessário para aceitar a missão                           |





## Estrutura da Tabela INSTANCIA_QUEST

### Descrição
Tabela que gerencia o estado das missões para cada personagem, registrando quais estão ativas/completas

| Campo             | Tipo      | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|-------------------|-----------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_quest`       | INTEGER   | Sim         | PK, FK        | -            | Identificador da missão                                                  |
| `id_personagem`  | INTEGER   | Sim         | PK, FK        | -            | Identificador do personagem                                              |
| `quest_status`   | BOOLEAN   | Não         | -             | FALSE        | Status de conclusão (FALSE=em andamento, TRUE=completa)                  |




## Estrutura da Tabela RECOMPENSA_QUEST

### Descrição
Tabela que armazena as recompensas associadas a cada missão, incluindo itens e ouro

| Campo             | Tipo      | Obrigatório | Chave         | Valor Padrão | Referência                     | Descrição                                                                 |
|-------------------|-----------|-------------|---------------|--------------|--------------------------------|---------------------------------------------------------------------------|
| `id_recompensa`  | SERIAL    | Sim         | PK            | Auto-incremento | -                            | Identificador único da recompensa                                        |
| `id_quest`      | INTEGER   | Sim         | FK            | -            | REFERENCES QUEST(id_quest)     | Missão à qual a recompensa está associada                                |
| `item_recompensa`| INTEGER   | sim         | FK            | -            | REFERENCES ITEM(id_item)       | Item concedido como recompensa (opcional)                                |
| `quantidade`    | INTEGER   | sim         | -             | 0            | -                            | Quantidade do item concedido                                             |
| `gold`          | INTEGER   | Não         | -             | 0            | -                            | Quantidade de ouro concedido                                             |





## Estrutura da Tabela DROP_NPC

### Descrição
Tabela que define os itens e recursos que podem ser obtidos ao derrotar NPCs, incluindo probabilidades e variações de quantidade


| Campo               | Tipo         | Obrigatório | Chave         | Valor Padrão | Descrição                                                                 |
|---------------------|--------------|-------------|---------------|--------------|---------------------------------------------------------------------------|
| `id_drop`          | SERIAL       | Sim         | PK            | Auto-incremento | Identificador único do drop                                              |
| `id_npc`          | INTEGER      | Sim         | FK            | -            | NPC que pode dropar o item                                               |
| `tipo_npc`        | VARCHAR(20)  | Sim         | -             | -            | Tipo do NPC ('BOSS' ou 'GENERICO')                                       |
| `id_item`         | INTEGER      | Não         | FK            | -            | Item que pode ser dropado (opcional)                                      |
| `quantidade_min`  | INTEGER      | sim         | -             | 1            | Quantidade mínima do item dropado                                        |
| `quantidade_max`  | INTEGER      | sim         | -             | 1            | Quantidade máxima do item dropado                                        |
| `probabilidade`   | FLOAT        | Sim         | -             | -            | Chance de drop (0-1, onde 1=100%)                                        |
| `gold_min`        | INTEGER      | sim         | -             | 0            | Quantidade mínima de ouro dropada                                        |
| `gold_max`        | INTEGER      | sim         | -             | 0            | Quantidade máxima de ouro dropada                                        |
