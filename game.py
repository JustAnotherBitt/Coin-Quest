import random
import pgzrun
from pgzero.keyboard import keys
from levels import LEVELS

# Constantes do jogo
WIDTH = 550
HEIGHT = 700
TITLE = '---=== Coin Quest ===---'
PADDING = 10

HERO_X_SPEED = 5
HERO_Y_SPEED = 5
HERO_LIVES = 3

# Cenas do jogo
MENU_SCENE = 0
PLAY_SCENE = 1
GAME_OVER_SCENE = 2
WIN_SCENE = 3

menu_buttons = {
    'start': Rect(175, 250, 200, 50),
    'sound': Rect(175, 320, 200, 50),
    'exit': Rect(175, 390, 200, 50)
}

# Controle global de som/música
sound_enabled = True
music_initialized = False

def init_music():
    global music_initialized
    if not music_initialized and sound_enabled:
        music.play("bg_music")  
        music.set_volume(0.5)
        music_initialized = True


# -------- Controle de entrada --------
keys_state = set()

def was_pressed(key):
    global keys_state
    pressed = False
    if keyboard[key] and key not in keys_state:
        pressed = True
    if keyboard[key]:
        keys_state.add(key)
    else:
        keys_state.discard(key)
    return pressed

# Wrapper para tocar sons respeitando sound_enabled
def play_sound(snd):
    if sound_enabled:
        snd.play()


# --------- Classes ---------
class Hero(Actor):
    def __init__(self, position):
        super(Hero, self).__init__("hero1", position)
        self.horizontal_speed = HERO_X_SPEED
        self.vertical_speed = HERO_Y_SPEED
        self.sprites = ["hero1", "hero2"]
        self.collect_coin = "hero_collect_coin"
        self.current_sprite = 0
        self.animation_counter = 0
        self.animating = True
        self.collecting = False
        self.coins = 0
        self.lives = HERO_LIVES
        self.old_y = self.y

    def update_animation(self):
        if self.collecting:
            self.image = self.collect_coin
            return
        self.animation_counter += 1
        if self.animation_counter % 20 == 0:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]

    def collect(self):
        self.coins += 1
        self.collecting = True
        play_sound(sounds.coin)
        self.image = "hero_collect_coin"
        clock.schedule_unique(self.stop_collect, 0.5)

    def stop_collect(self):
        self.collecting = False

    def take_damage(self, enemy):
        self.lives -= 1
        play_sound(sounds.hit)
        self.image = "hero_pain"
        clock.schedule_unique(self.reset_sprite, 0.5)
        if self.x < enemy.x:
            self.x -= 40
        else:
            self.x += 40
        self.y -= 20

    def reset_sprite(self):
        self.image = self.sprites[self.current_sprite]

    # Movimentos do herói com verificação de bordas
    def move_right(self):
        self.x += self.horizontal_speed
        if self.right >= WIDTH - PADDING:
            self.right = WIDTH - PADDING

    def move_left(self):
        self.x -= self.horizontal_speed
        if self.left <= PADDING:
            self.left = PADDING

    def move_up(self):
        self.y -= self.vertical_speed
        if self.top <= PADDING:
            self.top = PADDING

    def move_down(self):
        self.y += self.vertical_speed
        if self.bottom >= HEIGHT - PADDING:
            self.bottom = HEIGHT - PADDING


class Enemy(Actor):
    def __init__(self, sprite, platform):
        super(Enemy, self).__init__(sprite, (0, 0))
        self.sprites = ["enemy1", "enemy2"]
        self.current_sprite = 0
        self.animation_counter = 0
        self.animating = True
        self.platform = platform

        half_w = self.width // 2
        left_limit = platform.left + half_w + 5
        right_limit = platform.right - half_w - 5

        if left_limit > right_limit:
            spawn_x = (platform.left + platform.right) // 2
            self.speed = 0
        else:
            spawn_x = random.randint(int(left_limit), int(right_limit))
            self.speed = random.choice([-2, 2])

        spawn_y = platform.top - (self.height // 2) - 1
        self.pos = (spawn_x, spawn_y)

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter % 15 == 0:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]

    def move(self):
        if self.speed == 0:
            return
        self.x += self.speed

        half_w = self.width // 2
        left_bound = self.platform.left + half_w
        right_bound = self.platform.right - half_w

        if self.left <= left_bound:
            self.left = left_bound
            self.speed *= -1
        elif self.right >= right_bound:
            self.right = right_bound
            self.speed *= -1


class Platform(Rect):
    def __init__(self, x, y, w=120, h=20):
        super().__init__(x, y, w, h)

    def draw(self):
        screen.draw.filled_rect(self, "brown")


class Coin(Actor):
    def __init__(self, position):
        super(Coin, self).__init__("coin", position)


# --------- Cenas ---------
class MenuScene: 
    def __init__(self, game):
        self.game = game
        self.options = ["start", "sound", "exit"]
        self.selected_index = 0

    def init(self):
        init_music()

    # --- MenuScene ---
    def update(self):
        global sound_enabled, music_initialized, current_level

        # Navegação no menu 
        if was_pressed(keys.UP):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif was_pressed(keys.DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.options)

        # Seleção com Enter
        if was_pressed(keys.RETURN):
            choice = self.options[self.selected_index]
            if choice == "start":
                current_level = 0  # resetar fase apenas ao iniciar novo jogo
                self.game.change_scene(PLAY_SCENE)
            elif choice == "sound":
                sound_enabled = not sound_enabled
                if sound_enabled:
                    init_music()
                else:
                    try:
                        music.stop()
                        music_initialized = False
                    except:
                        pass
            elif choice == "exit":
                exit()

    def draw(self):
        screen.clear()
        screen.draw.text("=== Coin Quest ===", center=(WIDTH//2, 100), fontname="arcade",fontsize=35, color="white") 
        for i, name in enumerate(self.options):
            rect = menu_buttons[name]
            # Se for a opção selecionada → destaque
            if i == self.selected_index:
                color = (200, 200, 50)  # amarelo para destaque
            else:
                color = (100, 150, 100) if name != 'exit' else (150, 100, 100)
            screen.draw.filled_rect(rect, color)

            texts = {
                'start': 'Iniciar Jogo',
                'sound': f'Som: {"ON" if sound_enabled else "OFF"}',
                'exit': 'Sair'
            }
            screen.draw.text(texts[name], center=rect.center, fontsize=15, fontname="arcade", color="white")
        screen.draw.text("Use setas e ENTER", center=(WIDTH//2, HEIGHT-50), fontsize=15, fontname="arcade", color="white")


class PlayScene:
    def __init__(self, game):
        self.game = game

    def init(self):
        global current_level, hero
        current_level = 0
        hero = Hero((WIDTH // 2, HEIGHT - 100))  # herói novo, vidas resetadas
        load_level(current_level)

    def update(self):
        update_play_scene(self.game)

    def draw(self):
        draw_play_scene()
        

class GameOverScene:
    def __init__(self, game):
        self.game = game

    def init(self):
        pass

    def update(self):
        if was_pressed(keys.RETURN):
            self.game.change_scene(MENU_SCENE)

    def draw(self):
        screen.clear()
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2-50), fontsize=70, fontname="arcade", color="red")
        screen.draw.text("Pressione ENTER para retornar ao Menu", center=(WIDTH//2, HEIGHT//2+50), fontsize=15, fontname="arcade", color="white")


class WinScene:
    def __init__(self, game):
        self.game = game

    def init(self):
        pass

    def update(self):
        if was_pressed(keys.RETURN):
            self.game.change_scene(MENU_SCENE)

    def draw(self):
        screen.clear()
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2-50), fontsize=70, fontname="arcade", color="green")
        screen.draw.text("Pressione ENTER para retornar ao Menu", center=(WIDTH//2, HEIGHT//2+50), fontsize=15, fontname="arcade", color="white")


# -------- Organizador de cenas --------
class Game:
    def __init__(self):
        self.current_scene = None

    def change_scene(self, new_scene_id):
        if new_scene_id == MENU_SCENE:
            self.current_scene = MenuScene(self)
        elif new_scene_id == PLAY_SCENE:
            self.current_scene = PlayScene(self)
        elif new_scene_id == GAME_OVER_SCENE:
            self.current_scene = GameOverScene(self)
        elif new_scene_id == WIN_SCENE:
            self.current_scene = WinScene(self)
        self.current_scene.init()
        
        
# Variáveis globais
current_level = 0
hero = None
platforms = []
enemies = []
coins = []


def load_level(level_index):
    global hero, platforms, enemies, coins
    data = LEVELS[level_index]

    if hero is None:
        hero = Hero((WIDTH // 2, HEIGHT - 100))
    else:
        hero.pos = (WIDTH // 2, HEIGHT - 100)

    platforms = [Platform(*p) for p in data["platforms"]]
    coins = [Coin(pos) for pos in data["coins"]]
    enemies = [Enemy(sprite, platforms[i]) for sprite, i in data["enemies"]]

    for coin in coins:
        for enemy in enemies:
            attempts = 0
            while coin.colliderect(enemy) and attempts < 8:
                coin.y -= (coin.height + 5)
                attempts += 1
            if coin.colliderect(enemy):
                coin.x += (enemy.width + 10)
                if coin.left <= 0 or coin.right >= WIDTH:
                    coin.x -= 2 * (enemy.width + 10)
            if coin.top < 5:
                coin.top = 5
            if coin.left < 5:
                coin.left = 5
            if coin.right > WIDTH - 5:
                coin.right = WIDTH - 5


# -------- Funções específicas do PlayScene --------
def update_play_scene(game):
    global current_level

    hero.old_y = hero.y
    hero.update_animation()

    # Movimentação
    if keyboard[keys.LEFT]:
        hero.move_left()
    if keyboard[keys.RIGHT]:
        hero.move_right()
    if keyboard[keys.UP]:
        hero.move_up()
    if keyboard[keys.DOWN]:
        hero.move_down()

    # Colisão com plataformas
    for p in platforms:
        if hero.colliderect(p):
            if hero.bottom >= p.top and hero.old_y <= p.top:
                hero.bottom = p.top
            elif hero.top <= p.bottom and hero.old_y >= p.bottom:
                hero.top = p.bottom

    # Movimentação e colisão com inimigos
    for enemy in enemies:
        enemy.update_animation()
        enemy.move()
        if hero.colliderect(enemy):
            hero.take_damage(enemy)

    # Coleta de moedas
    for coin in coins[:]:
        if hero.colliderect(coin):
            hero.collect()
            coins.remove(coin)

    # Checagem de fim de fase
    if not coins:
        if current_level < len(LEVELS) - 1:
            current_level += 1
            load_level(current_level)
        else:
            game.change_scene(WIN_SCENE)

    # Fim do jogo por perda de vida
    if hero.lives <= 0 or hero.bottom >= HEIGHT: 
        game.change_scene(GAME_OVER_SCENE)


def draw_play_scene():
    screen.clear()
    for p in platforms:
        p.draw()
    for coin in coins:
        coin.draw()
    for enemy in enemies:
        enemy.draw()
    hero.draw()
    screen.draw.text(f"Vidas: {hero.lives}", (10, 10), fontname="arcade", fontsize=15, color="white")
    screen.draw.text(f"Moedas: {hero.coins}", (10, 40), fontname="arcade", fontsize=15, color="yellow")
    screen.draw.text(f"Fase: {current_level+1}", (10, 70), fontname="arcade", fontsize=15, color="cyan")


# -------- Setup inicial --------
game = Game()
game.change_scene(MENU_SCENE)


def update():
    if game.current_scene:
        game.current_scene.update()


def draw():
    if game.current_scene:
        game.current_scene.draw()
        
        
pgzrun.go()
