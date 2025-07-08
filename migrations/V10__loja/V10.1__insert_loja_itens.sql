INSERT INTO public.LOJA_ITENS (id_item, preco, quantidade_disponivel)
VALUES 
-- Armas
((SELECT id_item FROM public.ITEM WHERE nome = 'Espada de Madeira'), 50, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Espada de Ferro'), 100, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Espada de Mithril'), 200, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Espada de Adamantium'), 400, 10),

-- Peitorais
((SELECT id_item FROM public.ITEM WHERE nome = 'Peitoral de Madeira'), 50, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Peitoral de Ferro'), 100, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Peitoral de Mithril'), 200, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Peitoral de Adamantium'), 400, 10),

-- Capacetes
((SELECT id_item FROM public.ITEM WHERE nome = 'Capacete de Madeira'), 40, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Capacete de Ferro'), 80, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Capacete de Mithril'), 160, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Capacete de Adamantium'), 320, 10),

-- Escudos
((SELECT id_item FROM public.ITEM WHERE nome = 'Escudo de Madeira'), 40, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Escudo de Ferro'), 90, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Escudo de Mithril'), 180, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Escudo de Adamantium'), 350, 10),

-- Artefatos
((SELECT id_item FROM public.ITEM WHERE nome = 'Colar da Serenidade'), 60, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Coroa do Imperador'), 120, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Orbe do Destino'), 240, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Grimório Arcano'), 480, 10),

-- Comidas
((SELECT id_item FROM public.ITEM WHERE nome = 'Fruta Silvestre'), 10, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Pão de Centeio'), 20, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Carne de Caça'), 50, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Banquete Épico'), 100, 10),

-- Poções
((SELECT id_item FROM public.ITEM WHERE nome = 'Poção de Mana Fraca'), 15, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Poção de Mana Média'), 30, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Poção de Mana Forte'), 60, 10),
((SELECT id_item FROM public.ITEM WHERE nome = 'Elixir Arcano'), 120, 10);
