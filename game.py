import pygame,sys,time
from pygame.locals import *
import math
WINDOWWIDTH=640
WINDOWHEIGHT=480
BACKGROUNDCOLOR=(110,10,110)
BALL_COLOR = (130,110,225)
TEXT_COLOR=(255,255,255)
BALL_SIZE = 4


GAME_STATE_INIT        = 0
GAME_STATE_START_LEVEL = 1
GAME_STATE_RUN         = 2
GAME_STATE_GAMEOVER    = 3
GAME_STATE_SHUTDOWN    = 4
GAME_STATE_EXIT        = 5
GAME_STATE_WIN = 6


pygame.font.init()
game_over_font = pygame.font.SysFont(None,48)
text_font = pygame.font.SysFont(None,20)

u=0.7

game_state = GAME_STATE_INIT

pygame.init()
mainClock = pygame.time.Clock()

windowSurface=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
pygame.display.set_caption('开炮')


def DrawText(text,font,surface,x,y):
    text_obj = font.render(text,1,TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x,y)
    surface.blit(text_obj,text_rect)

# 游戏主循环
while True:
    # 事件监听
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    if game_state == GAME_STATE_INIT:
        # 初始化游戏
        ball_x  = 23
        ball_y  = 23
        #ball_dx = 2
        #ball_dy = 2
        angle=45
        velocity=20
        timestep=0.1
        g=9.8
        rec_width=20
        rec_high=5
        rec_x=100
        rec_y=395
        rec_dx=5
        pygame.draw.rect(windowSurface,[255,0,0],[0,400,6000,600],0)
        
        game_state = GAME_STATE_START_LEVEL
    elif game_state == GAME_STATE_START_LEVEL:
        # 新的一关
        if event.type == KEYDOWN:
            pygame.draw.rect(windowSurface,[255,0,0],[0,400,6000,600],0)
            if event.key == pygame.K_UP:
                angle=angle+5
            if event.key == pygame.K_DOWN:
                angle=angle-5        
            if event.key == pygame.K_SPACE:
                ball_dx = velocity * math.cos(angle*2*math.pi/360)
                ball_dy = velocity * math.sin(angle*2*math.pi/360)
                game_state = GAME_STATE_RUN
    elif game_state == GAME_STATE_RUN:
        # 游戏运行
        pygame.draw.rect(windowSurface,[255,0,0],[0,400,6000,600],0)
        pygame.draw.rect(windowSurface,[255,255,255],[400,300,10,100],0)
        ball_x += ball_dx*timestep;
        ball_y -= ball_dy*timestep;
        ball_dy -= g*timestep
        ball_x = int(ball_x)
        ball_y = int(ball_y)
        if ball_y >= 400:
            if ball_x>rec_x and ball_x<rec_x+rec_width:
                ball_y=399
                ball_dy=-ball_dy*u
                ball_dx=ball_dx*u*2
            else:
                ball_dx=0
                ball_dy=0 
                game_state=GAME_STATE_GAMEOVER
        if ball_x>=400 and ball_x<=410 and ball_y>=300:
            game_state=GAME_STATE_GAMEOVER
        if ball_x>410 and ball_y>400:
            game_state=GAME_STATE_WIN
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                rec_x-=rec_dx
            if event.key == pygame.K_RIGHT:
                rec_x+=rec_dx
        windowSurface.fill(BACKGROUNDCOLOR)
        pygame.draw.rect(windowSurface,[255,255,255],[rec_x,rec_y,rec_width,rec_high],0)
        pygame.draw.circle(windowSurface, BALL_COLOR, (ball_x, ball_y), BALL_SIZE, 0)
        pygame.draw.rect(windowSurface,[255,255,255],[400,300,10,100],0)
        pygame.draw.rect(windowSurface,[255,0,0],[0,400,6000,600],0)
    elif game_state ==  GAME_STATE_GAMEOVER:
        DrawText('GAME_OVER',game_over_font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3))
    elif game_state == GAME_STATE_WIN:
        DrawText('WIN',game_over_font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3))
    elif game_state == GAME_STATE_SHUTDOWN:
        game_state = GAME_STATE_EXIT
    
    pygame.display.update()
    mainClock.tick(30)