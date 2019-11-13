import pygame
import random
import time


# Colors to be used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (182, 116, 232)
GREEN = (43, 255, 0)
RED = (255, 0, 0)
YELLOW = (213, 242, 68)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

class Player(pygame.sprite.Sprite):

    def __init__(self):
        #call parent's init functions
        super().__init__()

        
        #must be named image to get to move w/ drawing sprites
        self.image = pygame.image.load("../assets/moose.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)

    def update(self):
        if self.rect.x < 0:
            self.rect.x += 5
        elif self.rect.x > 925:
            self.rect.x += -5

    def move_left(self):
        self.rect.x += -25

    def move_right(self):
        self.rect.x += 25

    def stop(self):
        self.rect.x += 0

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        #play with changing self.image/self.rect commands to see if pygame still responds
        self.image = pygame.image.load("../assets/frog.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)

    
class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 25

# Good etiquette to ensure script does not run automatically
def main():
    # Get pygames running
    pygame.init()

    #set up new window
    size = [SCREEN_WIDTH, SCREEN_HEIGHT] 
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Giliga: THE GAME")

    #actual game logic and sprite dimensions
    
    bullet_list = pygame.sprite.Group()

    enemy_list = pygame.sprite.Group()

    movingsprites = pygame.sprite.Group()

    player = Player()
    
    movingsprites.add(player)
    

    change_in_location = 0
    num_enemies = 0
    for enemy in range(10):
        #why doesn't range (1,3) work??? Or (1,5)????!??!?!!? #SOLVED (think -1 * -1 versus -1 * -1 * -1)
        for rows in range(1,5):
            enemy = Enemy()
            movingsprites.add(enemy)
            enemy_list.add(enemy)
            #set initial coordinates and shift slightly every new creation
            enemy.rect.y = 50 * rows
            enemy.rect.x = 150 + (55 * change_in_location)
            num_enemies += 1
        change_in_location += 1
        

   
    #don't want bullets drawn until middle of game


    #throw enemies in list to pull from when hit
    #enemy_list.add(enemy_far_left)
    #enemy_list.add(enemy_middle)
    #enemy_list.add(enemy_far_right)

    #initial coordinates of player
    player.rect.x = 250
    player.rect.y = 550
    
    font = pygame.font.SysFont("Calibri", 25, True, False)
    

    #allow while loop to run until window is exited
    done = False

    #control FPS
    clock = pygame.time.Clock()

    #set a value for enemy movement (same as update for player but unsure of how to include into method)
    enemy_movement = 3

    score = 0

    game_over = False
    while not done:
    #allows user to exit window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            elif not game_over:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                    elif event.key == pygame.K_SPACE:
                    #deal with bullet spam
                        if len(bullet_list) < 1:
                            bullet = Bullet()
                            bullet.rect.x = player.rect.x + (random.randint(0,1) * 65)
                            bullet.rect.y = player.rect.y + 10
                            movingsprites.add(bullet)
                            bullet_list.add(bullet)
                    
                            
    

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.stop()

        # because of -1 if rows are even will just push through
        #for each value in enemy list set it so if x is less than 0 or greater than 960, SWITCH, checks for first instance essentially no continuation to cause (-1 * -1)
        #for thing in enemy_list:
        if any (thing.rect.x < 0 or thing.rect.x > 960 for thing in enemy_list):
                enemy_movement = enemy_movement * -1
                
        for hit in bullet_list:
            enemy_hit_list = pygame.sprite.spritecollide(hit, enemy_list, True)
            for target in enemy_hit_list:
                bullet_list.remove(hit)
                movingsprites.remove(hit)
                score += 1
            if bullet.rect.y < 0:
                bullet_list.remove(hit)
                movingsprites.remove(hit)
            
        #set each rect.x value of each element in group to move by 4 pixels
        for movement in enemy_list:
            movement.rect.x += enemy_movement
        #enemy_far_left.rect.x += enemy_movement
        #enemy_middle.rect.x += enemy_movement
        #enemy_far_right.rect.x += enemy_movement


        
        if not game_over:
            time_passed = pygame.time.get_ticks()
        #god forsaken frankenstein version of displaying the time after dealing with milliseconds
            if time_passed < 60000:
                time_work = str(time_passed)
                if time_passed < 10000:
                    time_final = time_work[0] + " seconds"
                    game_over_time = time_final
                else:
                    time_final = time_work[0:2] + " seconds"
                    game_over_time = time_final
            elif time_passed < 120000:
                time_work = str(time_passed/60)
                time_sec = str(float(time_work[1:3])/1000*60)
                if float(time_sec) < 1:
                    time_final = time_work[0] + " minute and " + time_sec[2] + " seconds"
                    game_over_time = time_final
                else:
                    time_final = time_work[0] + " minute and " + time_sec[0] + time_sec[2] + " seconds"
                    game_over_time = time_final      
            else:
                time_work = str(time_passed/60)
                time_sec = str(float(time_work[1:3])/1000*60)
                if float(time_sec) < 1:
                    time_final = time_work[0] + " minutes and " + time_sec[2] + " seconds"
                    game_over_time = time_final
                else:
                    time_final = time_work[0] + " minutes and " + time_sec[0] + time_sec[2] + " seconds"
                    game_over_time = time_final
                


        
        movingsprites.update()
        
        text = font.render("Score: " + str(score), True, WHITE)
        time_text = font.render("Time: " + str(time_final), True, WHITE)
        end_game = font.render("GAME OVER", True, WHITE)
        end_time = font.render("Time: " + str(game_over_time), True, WHITE)

            
        
        screen.fill(BLACK)


        
        movingsprites.draw(screen)
        screen.blit(text, [375, 20])
        if not game_over:
            screen.blit(time_text, [500, 20])
        else:
            screen.blit(end_time, [500, 20])
        if time_passed > 250000 or score == num_enemies:
            screen.blit(end_game, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
            game_over = True
            


        

        
        
        #use to pause and then simulaniously display Game Over + retry key. Awesome. Need start screen + background stars (random per line)
            
       

        
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()

        
if __name__ == "__main__":
    main()

    
