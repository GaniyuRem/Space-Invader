import random
import pygame as pg
import sys

pg.init()
WIDTH = 1000
HEIGTH = 700

GAME_OVER = True
players = []


def main():
    player1 = input("Player 1: Enter you name >>>> ")
    player2 = input("Player 2: Enter you name >>>> ")
    if player1.isdigit() or player2.isdigit():
        raise ValueError("Input must not be an integer")
    else:
        players.append(player1)
        players.append(player2)
        game = Screen()
        game.start()


class Alien(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.sprite.Sprite()
        self.load_img = pg.image.load("Image/main_alien.png")
        self.rotate_image = pg.transform.rotate(self.load_img, -90)
        self.image = pg.transform.scale(self.rotate_image, (70, 70))
        self.rect = self.image.get_rect(
            center=(random.randint(20, 900), random.randint(0, 120)))
        self.location = self.rect
        self.alien_bullet_sprite = pg.sprite.Group()
        self.set_fire_trigger = UnitFire()

    def update(self):
        self.rect.y += 1

    def shoot(self):
        self.set_fire_trigger.set_fire_time(1300)
        if self.set_fire_trigger.fire():
            self.alien_bullet_sprite.add(
                Alien_Bullet(self.rect.x + 35, self.rect.y + 65))

    def get_alien_bullet(self):
        return self.alien_bullet_sprite


class UnitFire():
    def __init__(self):
        self.last = pg.time.get_ticks()
        self.cooldown = 0

    def fire(self):
        # fire gun, only if cooldown has been .3 seconds since last
        now = pg.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            return True

    def set_fire_time(self, cooldown):
        self.cooldown = cooldown


class Bullet(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pg.Surface((5, 10))
        self.rect = self.image.get_rect()
        self.bullet_color = ("red", "blue", "green")
        self.bullet_rand = random.randint(0, 2)
        self.image.fill(self.bullet_color[self.bullet_rand])
        self.rect.center = (x_pos, y_pos)

    def kill(self):
        if self.rect.y > 270:
            return True


class Player_Bullet(Bullet):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)

    def update(self):
        self.rect.y -= 20


class Alien_Bullet(Bullet):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)

    def update(self):
        self.rect.y += 20


class Player(pg.sprite.Sprite):
    def __init__(self, x_position, player, x_pos_score):
        super().__init__()
        self.reset(x_position, player, x_pos_score)
        self.player = player

    def reset_score(self):
        self.score = 0

    def get_player(self):
        return self.player

    def player_position(self):
        self.rect.center = pg.Vector2((self.player_x_cor / 2, HEIGTH / 1.10))

    def respawn_hit(self):
        self.player_position()

    def respawn_off_screen(self):
        if self.rect.y <= -90:
            self.player_position()

    def set_increase_score(self):
        self.score += 1

    @ property
    def get_increase_score(self):
        return self.score

    @ property
    def get_decrease_score(self):
        if self.score == 0:
            self.score = 0
        else:
            self.score -= 1

    def update(self):
        self.rect.y -= 4
        if self.rect.y < 0:
            self.rect.y = 0
        return self.rect.y

    def back(self):
        self.rect.y += 4
        if self.rect.y > HEIGTH - self.rect.height:
            self.rect.y = HEIGTH - self.rect.height
        return self.rect.y

    def move_left(self):
        self.rect.x -= 8
        if self.rect.x < 0:
            self.rect.x = 0
        return self.rect.x

    def move_right(self):
        self.rect.x += 8
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

        return self.rect.x

    def collide_alien_player(self, alien):
        if pg.sprite.spritecollide(sprite=self, group=alien, dokill=True):
            return True

    def collide_alien_bullet_player(self, alien_bullet):
        if pg.sprite.spritecollide(sprite=self, group=alien_bullet, dokill=True):
            # self.get_decrease_score
            return True

    def shoot(self):
        self.set_fire_trigger.set_fire_time(500)
        if self.set_fire_trigger.fire():
            self.sprite_bullet.add(Player_Bullet(
                self.rect.x + 40, self.rect.y))

    def get_bullet(self):
        return self.sprite_bullet

    def player_score(self, screen):
        font = pg.font.Font('freesansbold.ttf', 32)
        scoretext = font.render(
            f'{self.player} = ' + str(self.score), True, "white")
        scoretextRect = scoretext.get_rect()
        scoretextRect.center = (
            self.x_pos_score, HEIGTH // 9)
        screen.blit(scoretext, scoretextRect)

    def reset(self, x_position, player, x_pos_score):
        self.x_pos_score = x_pos_score
        self.set_fire_trigger = UnitFire()
        self.sprite_bullet = pg.sprite.Group()

        self.controller = Control()

        # Creating a sprite player object from sprite class
        self.pressed = pg.key.get_pressed()
        self.default_width = 8
        self.bg_color = "BLACK"

        self.image = pg.sprite.Sprite()
        # loading image from pygame
        self.load_img = pg.image.load("Image/plane.png")
        self.rotate_image = pg.transform.rotate(self.load_img, 90)
        # scaling the image
        self.image = pg.transform.scale(
            self.rotate_image, (80, 110))
        # getting image position and crreating a rectange box aroung the image
        self.rect = self.image.get_rect()
        self.player_x_cor = x_position
        # Default player position
        self.score = 0
        self.player_position()


class Control:
    def control(self, m_forward=None, m_back=None, m_left=None, m_right=None, shoot=None, player=None):
        self.pressed = pg.key.get_pressed()
        if self.pressed[m_forward]:
            player.update()
        # player.respawn_off_screen()
        if self.pressed[m_left]:
            player.move_left()
        if self.pressed[m_right]:
            player.move_right()
        if self.pressed[m_back]:
            player.back()
        if self.pressed[shoot]:
            player.shoot()


class SpaceInavder:
    def __init__(self):
        self.aliens_sprites = pg.sprite.Group()
        self.player_sprites = pg.sprite.Group()

        self.load_player_pos = int((200 / 2))
        self.add_players()
        self.bg_color = "BLACK"

    def create_font(self, t, s=72, c=(255, 255, 0), b=False, i=False):
        font = pg.font.SysFont("Arial", s, bold=b, italic=i)
        text = font.render(t, True, c)
        return text

    def alien_Collide_with_Bullet(self):
        for i in self.player_sprites.sprites():
            if pg.sprite.groupcollide(groupa=self.aliens_sprites, groupb=i.get_bullet(), dokilla=True, dokillb=True):
                return True, i
        return [False, i]

    def collison_score(self):
        value = self.alien_Collide_with_Bullet()
        if value[0]:
            value[1].set_increase_score()

    def alien_bullet_Collide_with_player(self) -> str:
        for i in self.player_sprites.sprites():
            for j in self.aliens_sprites.sprites():
                if i.collide_alien_bullet_player(j.get_alien_bullet()):
                    i.get_decrease_score
                    # print(j.get_alien_bullet())

    def add_aliens(self):
        random_alien = random.randint(1, 1)
        for i in range(random_alien):
            self.aliens_sprites.add(Alien())

    def add_new_aliens(self):
        # print(len(self.aliens_sprites))
        if len(self.aliens_sprites.sprites()) == 0:
            self.add_aliens()
        for alien in self.aliens_sprites.sprites():
            if self.aliens_sprites.sprites()[-1].rect.y > 170:
                self.add_aliens()
            if alien.rect.y > 670:
                alien.kill()
        pg.display.update()

    def add_players(self):
        for i in range(2):
            self.load_player_pos += 600
            if i == 0:
                self.player_sprites.add(
                    Player(self.load_player_pos, players[i], 140))
            elif i == 1:
                self.player_sprites.add(
                    Player(self.load_player_pos, players[i], 850))

    def handle_event(self):
        if GAME_OVER:
            self.player_sprites.sprites()[0].controller.control(
                m_forward=pg.K_w, m_back=pg.K_s, m_left=pg.K_a, m_right=pg.K_d, shoot=pg.K_SPACE,
                player=self.player_sprites.sprites()[0])
            self.player_sprites.sprites()[1].controller.control(
                m_forward=pg.K_UP, m_back=pg.K_DOWN, m_left=pg.K_LEFT, m_right=pg.K_RIGHT, shoot=pg.K_RSHIFT,
                player=self.player_sprites.sprites()[1])
        else:
            pressed = pg.K_SPACE
            self.m_pressd = pg.key.get_pressed()
            if self.m_pressd[pressed]:
                self.reset()

    def collide_alien_player(self):
        for i in self.player_sprites.sprites():
            if i.collide_alien_player(self.aliens_sprites):
                i.respawn_hit()
                i.get_decrease_score
                # print("get ya bitch")

    def draw_player_bullets(self, screen):
        for i in self.player_sprites.sprites():
            i.sprite_bullet.draw(screen)
            i.sprite_bullet.update()
            pg.display.update()

    def draw_aliens_bullets(self, screen):
        for i in self.aliens_sprites.sprites():
            i.alien_bullet_sprite.draw(screen)
            i.alien_bullet_sprite.update()

    def win_player(self, screen):
        for i in self.player_sprites.sprites():
            if i.get_increase_score == 2:
                game_over = self.create_font("GAME OVER")
                restart = self.create_font(
                    "Press Space to restart", 36, (9, 0, 180))
                winner = self.create_font(
                    f"{i.get_player()} wins", 60, (9, 180, 20))
                # # # print(i.get_player(), "WINS")
                screen.blit(game_over, (300, 150))
                screen.blit(winner, (330, 250))
                screen.blit(restart, (320, 350))

                global GAME_OVER
                GAME_OVER = False

    def alien_shot(self):
        for i in self.aliens_sprites.sprites():
            i.shoot()

    def update_score_display(self, screen):
        for i in self.player_sprites.sprites():
            i.player_score(screen)

    def reset(self):
        global GAME_OVER
        if GAME_OVER == False:
            for i in self.player_sprites.sprites():
                i.reset_score()
                i.player_position()
            GAME_OVER = True
            pg.display.update()


class Screen:
    def __init__(self):
        self.game_over = True
        self.space = SpaceInavder()
        self.bg_color = "black"
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        self.screen.fill(self.bg_color)
        self.flip = pg.display.flip
        self.running = True
        self.font = pg.font.Font(pg.font.get_default_font(), 32)
        self.text_score = self.font.render('Score', True, 'white')
        # create a rectangular object for the
        # text surface object
        self.text_score_Rect = self.text_score.get_rect()
        # set the center of the rectangular object.
        self.text_score_Rect.center = (WIDTH // 2, HEIGTH // 9)

    def start(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break

            self.space.handle_event()
            if GAME_OVER:
                self.space.alien_shot()
                self.space.collison_score()
                self.screen.fill(self.bg_color)
                self.space.update_score_display(self.screen)

                self.space.win_player(self.screen)
                self.space.aliens_sprites.draw(self.screen)
                self.space.player_sprites.draw(self.screen)
                self.space.draw_player_bullets(self.screen)
                self.space.draw_aliens_bullets(self.screen)

                self.space.collide_alien_player()
                self.space.alien_bullet_Collide_with_player()
                self.space.add_new_aliens()
                self.space.aliens_sprites.update()
                self.flip()
                pg.display.update()
