from game.src.operadores.Usuario.menu_usuario import menu_usuario
from game.src.operadores.Personagem.menu_personagens import menu_personagens
from game.src.operadores.Personagem.selecionar_personagem import selecionar_personagem
from game.src.operadores.Personagem.mover_personagem import mover_personagem
from game.src.operadores.Personagem.menu_acoes import menu_acoes
from game.src.operadores.Inventario.abrir_inventario import abrir_inventario
from game.src.operadores.Inventario.menu_acoes_item import menu_acoes_item

def main():
    while True:
        id_usuario, username = menu_usuario()
        
        if id_usuario is None:
            continue
        
        while True:
    
            resultado = menu_personagens(id_usuario, username)
            
            if resultado == "voltar":
                break
            
            id_personagem = selecionar_personagem(resultado, id_usuario, username)

            if not id_personagem:
                continue
            
            while True:
                acao = menu_acoes(id_personagem)

                if acao == "mover":
                    while True:
                        result_movimento = mover_personagem(id_personagem)

                        if result_movimento == "voltar":
                            break
            
                elif acao == "abrir inventário":
                    id_item = abrir_inventario(id_personagem)[0]
                    if id_item == -1:
                        continue 
                    else:
                        acao = menu_acoes_item(id_item)
                elif acao == "sair":
                    print("Saindo do jogo...")
                    break
    
if __name__ == "__main__":
    main()