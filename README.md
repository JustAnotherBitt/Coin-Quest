# Coin Quest

Este é um jogo 2D feito em Python com Pygame Zero.
O objetivo é coletar moedas, evitar inimigos e avançar por vários níveis até a vitória!

## Estrutura do Projeto

A estrutura do projeto é organizada para facilitar o desenvolvimento e a manutenção:

```
PROJECT
├── fonts/
├── images/
├── music/
├── sounds/
├── venv/ (Não incluído no controle de versão)
├── game.py
└── levels.py
```

- `fonts/`: Contém os arquivos de fontes utilizados no jogo.
- `images/`: Armazena todos os recursos visuais do jogo, incluindo os sprites animados do herói e dos inimigos.
- `music/`: Contém a trilhas sonora do jogo.
- `sounds/`: Armazena os efeitos sonoros do jogo.
- `venv/`: Ambiente virtual Python, não incluído no controle de versão. Deve ser criado e ativado localmente.
- `game.py`: O arquivo principal do jogo, onde a lógica e a interação são implementadas.
- `levels.py`: Define a estrutura de cada fase do jogo, incluindo plataformas, moedas e inimigos.

## Funcionalidades do Jogo

- **Sprites Animados**: Tanto o herói quanto os inimigos possuem sprites animados, proporcionando uma experiência visual mais rica e dinâmica.
- **Múltiplas Fases**: O jogo é composto por 5 fases distintas, cada uma com seu próprio layout de plataformas, moedas e desafios.
- **Coleta de Moedas**: O objetivo principal é coletar todas as moedas em cada fase.
- **Inimigos Desafiadores**: Evite os inimigos que patrulham as fases para sobreviver.

## Bibliotecas Utilizadas

O jogo foi desenvolvido utilizando a seguinte biblioteca:

- **Pygame Zero**: Uma biblioteca de jogos para iniciantes em Python, que simplifica a criação de jogos com uma API fácil de usar. É construída sobre o Pygame.

## Como Jogar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado em seu sistema.

### Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/JustAnotherBitt/Coin-Quest.git
   cd Coin-Quest
   ```

2. **Crie e ative um ambiente virtual**:
   É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto. Isso evita conflitos com outras instalações Python em seu sistema.

   ```bash
   python3 -m venv venv
   ```

   - No Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências**:
   Com o ambiente virtual ativado, instale a biblioteca `pgzero`:

   ```bash
   pip3 install pgzero
   ```

4. **Execute o jogo**:
   Após a instalação, você pode iniciar o jogo executando o arquivo `game.py`:

   ```bash
   pgzrun game.py
   ```

### Controles

- **Setas do teclado**: Mover o herói e os botões do menu.
- **Enter**: Selecionar.

## Créditos

Desenvolvido por Letícia De Patta Rodrigues :)


