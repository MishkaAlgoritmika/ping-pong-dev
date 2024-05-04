from pygame import *

'''Необходимые классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #вместе 55,55 - параметры
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

        #для уменьшения ракеток
        self.width = width
        self.height = height
        self.player_image = player_image
    
    def set_default(self, height):
        self.height = height
        self.image = transform.scale(image.load(self.player_image), (self.width, height))

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        
        #фикс ухода за нижнюю границу
        if keys[K_DOWN] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        
        #фикс ухода за нижнюю границу
        if keys[K_s] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed
    
    #для уменьшения ракеток
    def change_size(self):
        self.height *= 0.9
        self.image = transform.scale(image.load(self.player_image), (self.width, int(self.height)))

#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
win_width = 1200
win_height = 700
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

#создания мяча и ракетки 
racket_width = 50
racket_height = 150
ball_width = 50
ball_height = 50


racket1 = Player('redracket.png', 30, win_height / 2 - racket_height / 2, 4, racket_width, racket_height) 
racket2 = Player('greenracket.png', win_width - racket_width - 30, win_height / 2 - racket_height / 2, 4, racket_width, racket_height)
ball = GameSprite('tenis_ball.png', win_width / 2 - ball_width / 2, win_height / 2 - ball_height / 2, 4, ball_width, ball_height)

font.init()
font1 = font.Font(None, 35)
lose1 = font1.render('ПОБЕДА 2 ИГРОКА!', True, (180, 0, 0))
lose2 = font1.render('ПОБЕДА 1 ИГРОКА!', True, (180, 0, 0))
text_shift_x = 100

score_font = font.Font(None, 50)
score_text_color = (0, 0, 0)
score_text_shift_x = 35
score_text_shift_y = 25


speed_x = 3
speed_y = 3

win_score = 3
player1_score = 0
player2_score = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        #При касании мячом ракетки менять направление и скорость мяча
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1.2

            #будем уменьшать размеры ракеток
            if sprite.collide_rect(racket1, ball):
                racket1.change_size()
            else:
                racket2.change_size()
      
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height - ball_height or ball.rect.y < 0:
            speed_y *= -1

        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока, также возвращаем размер ракеток
        if ball.rect.x < 0:
            player2_score += 1
            ball.rect.x =  win_width / 2 - ball_width / 2
            ball.rect.y =  win_height / 2 - ball_height / 2
            speed_x = 3
            speed_x *= -1
            racket1.set_default(racket_height)
            racket2.set_default(racket_height)

        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока, также возвращаем размер ракеток
        if ball.rect.x > win_width:
            player1_score += 1
            ball.rect.x =  win_width / 2 - ball_width / 2
            ball.rect.y =  win_height / 2 - ball_height / 2
            speed_x *= -1
            racket1.set_default(racket_height)
            racket2.set_default(racket_height)


        score_text = score_font.render(str(player1_score) + " : " + str(player2_score), 1, score_text_color)
        window.blit(score_text, (win_width / 2 - score_text_shift_x, score_text_shift_y))

        if player1_score >= win_score or player2_score >= win_score:
            if player1_score >= win_score:
                window.blit(lose2, (win_width / 2 - text_shift_x, win_height / 2))
            elif player2_score >= win_score:
                window.blit(lose2, (win_width / 2 - text_shift_x, win_height / 2))
            
            ball.rect.x =  win_width / 2 - ball_width / 2
            ball.rect.y =  score_text_shift_y + ball_height + 25
            game_over = True
            finish = True

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
