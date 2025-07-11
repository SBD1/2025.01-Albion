-- USUÁRIO

CREATE OR REPLACE FUNCTION f_get_usuario_por_id(p_id_usuario INT)
RETURNS TABLE(id_usuario INT, username VARCHAR, data_criacao TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT id_usuario, username, data_criacao
    FROM USUARIO
    WHERE id_usuario = p_id_usuario;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_get_usuario_por_username(p_username VARCHAR)
RETURNS TABLE(id_usuario INT, username VARCHAR, data_criacao TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT id_usuario, username, data_criacao
    FROM USUARIO
    WHERE username = p_username;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_conta_usuarios()
RETURNS INT AS $$
DECLARE
    v_total INT;
BEGIN
    SELECT COUNT(*) INTO v_total FROM USUARIO;
    RETURN v_total;
END;
$$ LANGUAGE plpgsql;

-- SALA

CREATE OR REPLACE FUNCTION f_get_sala_por_id(p_id_sala INTEGER)
RETURNS TABLE (
    id_sala       INTEGER,
    nome          VARCHAR,
    descricao     TEXT,
    conexao_norte INTEGER,
    conexao_sul   INTEGER,
    conexao_leste INTEGER,
    conexao_oeste INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM sala
    WHERE id_sala = p_id_sala;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_listar_salas()
RETURNS TABLE (
    id_sala       INTEGER,
    nome          VARCHAR,
    descricao     TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT id_sala, nome, descricao
    FROM sala;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_obter_conexoes(p_id_sala INTEGER)
RETURNS TABLE (
    direcao VARCHAR,
    id_conectado INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'norte', conexao_norte FROM sala WHERE id_sala = p_id_sala
    UNION ALL
    SELECT 'sul', conexao_sul FROM sala WHERE id_sala = p_id_sala
    UNION ALL
    SELECT 'leste', conexao_leste FROM sala WHERE id_sala = p_id_sala
    UNION ALL
    SELECT 'oeste', conexao_oeste FROM sala WHERE id_sala = p_id_sala;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_salas_conectadas(p_id_sala INTEGER)
RETURNS TABLE (
    id_sala INTEGER,
    nome    VARCHAR,
    direcao VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT s.id_sala, s.nome, 'norte'
    FROM sala s
    WHERE s.id_sala = (SELECT conexao_norte FROM sala WHERE id_sala = p_id_sala)
    
    UNION ALL

    SELECT s.id_sala, s.nome, 'sul'
    FROM sala s
    WHERE s.id_sala = (SELECT conexao_sul FROM sala WHERE id_sala = p_id_sala)

    UNION ALL

    SELECT s.id_sala, s.nome, 'leste'
    FROM sala s
    WHERE s.id_sala = (SELECT conexao_leste FROM sala WHERE id_sala = p_id_sala)

    UNION ALL

    SELECT s.id_sala, s.nome, 'oeste'
    FROM sala s
    WHERE s.id_sala = (SELECT conexao_oeste FROM sala WHERE id_sala = p_id_sala);
END;
$$ LANGUAGE plpgsql;

-- ITEM

CREATE OR REPLACE FUNCTION f_info_item_por_id(p_id_item INTEGER)
RETURNS TABLE (
    id_item INTEGER,
    nome VARCHAR,
    descricao TEXT,
    nivel INTEGER,
    tipo_item VARCHAR,
    subtipo VARCHAR,
    info_extra TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id_item,
        i.nome,
        i.descricao,
        i.nivel,
        i.tipo_item,
        
        COALESCE(
            a.tipo_equipavel,
            ne.tipo_nequipavel,
            'Desconhecido'
        ) AS subtipo,
        
        CASE 
            WHEN ar.id_item IS NOT NULL THEN 
                'Aumento Ataque Físico: ' || ar.aumento_ataque_fisico
            WHEN rm.id_item IS NOT NULL THEN 
                'Defesa Física: ' || rm.aumento_defesa_fisica ||
                ', Defesa Mágica: ' || rm.aumento_defesa_magica ||
                ', Vida Máxima: ' || rm.aumento_vida_maxima
            WHEN af.id_item IS NOT NULL THEN 
                'Ataque Mágico: ' || af.aumento_ataque_magico ||
                ', Mana Máxima: ' || af.mana_maxima
            WHEN cm.id_item IS NOT NULL THEN 
                'Vida Atual: ' || cm.aumento_vida_atual ||
                ', Stamina Atual: ' || cm.aumento_stamina_atual
            WHEN pc.id_item IS NOT NULL THEN 
                'Mana Atual: ' || pc.aumento_mana_atual
            ELSE 'Nenhuma informação extra'
        END AS info_extra
        
    FROM item i
    LEFT JOIN equipavel a ON i.id_item = a.id_item
    LEFT JOIN arma ar ON i.id_item = ar.id_item
    LEFT JOIN armadura rm ON i.id_item = rm.id_item
    LEFT JOIN artefato af ON i.id_item = af.id_item
    LEFT JOIN nequipavel ne ON i.id_item = ne.id_item
    LEFT JOIN comida cm ON i.id_item = cm.id_item
    LEFT JOIN pocao pc ON i.id_item = pc.id_item
    WHERE i.id_item = p_id_item;
END;
$$ LANGUAGE plpgsql;

-- PERSONAGEM

CREATE OR REPLACE FUNCTION fn_lista_personagens_por_usuario(p_id_usuario INTEGER)
RETURNS TABLE (
    id_personagem INTEGER,
    nome VARCHAR,
    nivel INTEGER,
    qtd_ouro INTEGER,
    nome_sala VARCHAR,
    especie VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id_personagem,
        p.nome, 
        p.nivel, 
        p.qtd_ouro, 
        s.nome AS nome_sala,
        CASE 
            WHEN z.id_personagem IS NOT NULL THEN 'Zoiudo'
            WHEN e.id_personagem IS NOT NULL THEN 'Espiritualista'
            WHEN d.id_personagem IS NOT NULL THEN 'Draconico'
            WHEN t.id_personagem IS NOT NULL THEN 'Titan'
            ELSE 'Desconhecido'
        END AS especie
    FROM public.personagem p
    LEFT JOIN public.zoiudo z ON p.id_personagem = z.id_personagem
    LEFT JOIN public.espiritualista e ON p.id_personagem = e.id_personagem
    LEFT JOIN public.draconico d ON p.id_personagem = d.id_personagem
    LEFT JOIN public.titan t ON p.id_personagem = t.id_personagem
    JOIN public.sala s ON p.id_sala = s.id_sala
    WHERE p.id_usuario = p_id_usuario
    ORDER BY p.nivel;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_consulta_inventario(p_id_personagem INTEGER)
RETURNS TABLE (
    id_instancia INTEGER,
    nome_item VARCHAR,
    descricao TEXT,
    quantidade INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ii.id_instancia,
        i.nome AS nome_item,
        i.descricao,
        ii.quantidade
    FROM 
        public.INVENTARIO_ITENS inv
    JOIN 
        public.INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
    JOIN 
        public.ITEM i ON ii.id_item = i.id_item
    WHERE 
        inv.id_personagem = p_id_personagem
    ORDER BY 
        i.nome;
END;
$$ LANGUAGE plpgsql;