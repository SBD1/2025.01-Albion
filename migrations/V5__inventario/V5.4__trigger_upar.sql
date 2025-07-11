CREATE OR REPLACE FUNCTION f_atualizar_atributos_por_nivel()
RETURNS TRIGGER AS $$
DECLARE
    niveis_ganhos INTEGER;
BEGIN
    IF OLD.nivel != NEW.nivel THEN
        niveis_ganhos := NEW.nivel - OLD.nivel;
        
        IF niveis_ganhos > 0 THEN
            NEW.ataque_fisico := OLD.ataque_fisico + (niveis_ganhos * 10);
            NEW.defesa_fisica := OLD.defesa_fisica + (niveis_ganhos * 10);
            NEW.defesa_magica := OLD.defesa_magica + (niveis_ganhos * 10);
            NEW.vida_maxima := OLD.vida_maxima + (niveis_ganhos * 20);
            NEW.stamina_maxima := OLD.stamina_maxima + (niveis_ganhos * 10);
            NEW.exp_maxima := OLD.exp_maxima + (niveis_ganhos * 50);

            NEW.vida_atual := NEW.vida_maxima;
            NEW.stamina_atual := NEW.stamina_maxima;
            
            IF EXISTS (SELECT 1 FROM public.ESPIRITUALISTA WHERE id_personagem = NEW.id_personagem) THEN
                UPDATE public.ESPIRITUALISTA 
                SET mana_atual = mana_total 
                WHERE id_personagem = NEW.id_personagem;
            END IF;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_atualizar_atributos_nivel ON public.PERSONAGEM;

CREATE TRIGGER trigger_atualizar_atributos_nivel
    BEFORE UPDATE ON public.PERSONAGEM
    FOR EACH ROW
    EXECUTE FUNCTION f_atualizar_atributos_por_nivel();

CREATE OR REPLACE FUNCTION f_atualizar_atributos_fantasma_por_nivel()
RETURNS TRIGGER AS $$
DECLARE
    niveis_ganhos INTEGER;
BEGIN
    IF OLD.nivel != NEW.nivel THEN
        niveis_ganhos := NEW.nivel - OLD.nivel;
        
        IF niveis_ganhos > 0 THEN
            NEW.ataque_fisico := OLD.ataque_fisico + (niveis_ganhos * 10);
            NEW.ataque_magico := OLD.ataque_magico + (niveis_ganhos * 10);
            NEW.defesa_fisica := OLD.defesa_fisica + (niveis_ganhos * 10);
            NEW.defesa_magica := OLD.defesa_magica + (niveis_ganhos * 10);
            NEW.vida_maxima := OLD.vida_maxima + (niveis_ganhos * 15);
            NEW.exp_maxima := OLD.exp_maxima + (niveis_ganhos * 50);
            NEW.vida_atual := NEW.vida_maxima;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_atualizar_atributos_fantasma_nivel ON public.FANTASMA;

CREATE TRIGGER trigger_atualizar_atributos_fantasma_nivel
    BEFORE UPDATE ON public.FANTASMA
    FOR EACH ROW
    EXECUTE FUNCTION f_atualizar_atributos_fantasma_por_nivel();