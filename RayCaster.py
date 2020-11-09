import pygame
import pygame_menu
from gl import *


isRunning = True
pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

r = Raycaster(screen)
r.load_map('map2.txt')



def draw_background():
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image, (r.width, r.height))
    screen.blit(background_image, (0,0))



def game():
    isRunning = True
    sound = pygame.mixer.Sound('./music.wav')
    pygame.mixer.Sound.play(sound)

    while isRunning:


        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                pygame.mixer.stop()

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e:
                    r.player['angle'] += 5


                i = int(newX / r.blocksize)
                j = int(newY / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY

        screen.fill(pygame.Color("gray")) #Fondo

        #Techo
        screen.fill(pygame.Color("black"), (int(r.width / 2), 0, int(r.width / 2),int(r.height / 2)))
        
        #Piso
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2),int(r.height / 2)))

        r.render()
        
        # FPS
        screen.fill(pygame.Color("black"), (0,0,30,30))
        screen.blit(updateFPS(), (0,0))
        clock.tick(30)  
        
        pygame.display.update()





menu = pygame_menu.Menu(300, 400, 'EGYPT MAZE',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_button('Play', game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen, bgfun= draw_background)

pygame.quit()
