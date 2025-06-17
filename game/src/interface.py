from colorama import init, Fore, Back, Style
import os
from typing import List, Optional

# Inicializa o colorama
init(autoreset=True)

class Interface:
    # Cores e estilos
    CORES = {
        'titulo': Fore.CYAN + Style.BRIGHT,
        'menu': Fore.YELLOW,
        'sucesso': Fore.GREEN,
        'erro': Fore.RED,
        'info': Fore.BLUE,
        'destaque': Fore.MAGENTA,
        'normal': Fore.WHITE,
        'fundo': Back.BLACK
    }

    @staticmethod
    def limpar_tela():
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def criar_titulo(texto: str, largura: int = 60) -> str:
        """Cria um título formatado com bordas."""
        borda = '═' * largura
        espaco = ' ' * ((largura - len(texto) - 2) // 2)
        return f"\n{Interface.CORES['titulo']}{borda}\n{espaco}{texto}{espaco}\n{borda}\n"

    @staticmethod
    def criar_menu(titulo: str, opcoes: List[str], largura: int = 60) -> str:
        """Cria um menu formatado com opções numeradas."""
        menu = [Interface.criar_titulo(titulo, largura)]
        for i, opcao in enumerate(opcoes, 1):
            menu.append(f"{Interface.CORES['menu']}{i}. {opcao}")
        menu.append(f"\n{Interface.CORES['normal']}Escolha uma opção: ")
        return '\n'.join(menu)

    @staticmethod
    def criar_borda(texto: str, largura: int = 60) -> str:
        """Cria uma borda decorativa ao redor do texto."""
        borda = '═' * largura
        espaco = ' ' * ((largura - len(texto) - 2) // 2)
        return f"\n{Interface.CORES['destaque']}{borda}\n{espaco}{texto}{espaco}\n{borda}\n"

    @staticmethod
    def criar_elemento(texto: str, tipo: str = 'normal') -> str:
        """Cria um elemento decorativo com cor específica."""
        return f"{Interface.CORES[tipo]}{texto}"

    @staticmethod
    def mostrar_mensagem(texto: str, tipo: str = 'normal') -> None:
        """Mostra uma mensagem formatada."""
        print(f"{Interface.CORES[tipo]}{texto}")

    @staticmethod
    def mostrar_erro(texto: str) -> None:
        """Mostra uma mensagem de erro."""
        print(f"{Interface.CORES['erro']}❌ {texto}")

    @staticmethod
    def mostrar_sucesso(texto: str) -> None:
        """Mostra uma mensagem de sucesso."""
        print(f"{Interface.CORES['sucesso']}✅ {texto}")

    @staticmethod
    def mostrar_info(texto: str) -> None:
        """Mostra uma mensagem informativa."""
        print(f"{Interface.CORES['info']}ℹ️ {texto}")

    @staticmethod
    def criar_mapa(sala_atual: dict, largura: int = 60) -> str:
        """Cria uma representação visual do mapa da sala atual."""
        mapa = []
        mapa.append(Interface.criar_titulo(f"Sala: {sala_atual['nome']}", largura))
        
        # Descrição da sala
        mapa.append(f"{Interface.CORES['info']}Descrição: {sala_atual['descricao']}")
        
        # Saídas disponíveis
        mapa.append(f"\n{Interface.CORES['destaque']}Saídas disponíveis:")
        for direcao, sala in sala_atual['saidas'].items():
            mapa.append(f"{Interface.CORES['menu']}→ {direcao}: {sala}")
        
        return '\n'.join(mapa)

    @staticmethod
    def mostrar_personagem(personagem: dict) -> None:
        """Mostra as informações do personagem de forma formatada."""
        print(Interface.criar_titulo("Informações do Personagem"))
        print(f"{Interface.CORES['destaque']}Nome: {personagem['nome']}")
        print(f"{Interface.CORES['info']}Raça: {personagem['raca']}")
        print(f"{Interface.CORES['menu']}Nível: {personagem['nivel']}")
        print(f"{Interface.CORES['sucesso']}Vida: {personagem['vida']}/{personagem['vida_maxima']}")
        print(f"{Interface.CORES['erro']}Força: {personagem['forca']}")
        print(f"{Interface.CORES['info']}Defesa: {personagem['defesa']}") 