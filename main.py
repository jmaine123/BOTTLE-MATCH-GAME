import pygame, sys, random
import numpy as np
from random import shuffle

# import pickle


#Game Settings
FPS = 60
pygame.init()
pygame.mixer.init
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
PURPLE = (51, 0, 204)
LAVENDER = (105, 0, 196)
TRANSPARENT_PURPLE = (86, 76, 125, 120)
DARK_PURPLE = (86, 76, 125)
LIGHT_BLUE = (67, 217, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 223, 0)
ORANGE = (255, 165, 0)
RED = (255,0,0)
FONT_SIZE = 36
SMALL_FONT_SIZE = 25
SUPER_SMALL_FONT = 20
BIG_FONT_SIZE = 50
BOTTLE_WIDTH = 120
BOTTLE_HEIGHT = 160
IMAGE_SIZE = (BOTTLE_WIDTH, BOTTLE_HEIGHT)
SHELF_GAP = 10
BOTTLE_GAP = 15
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 50



#game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Bottle Match Game")
game_music = pygame.mixer.Sound("./assets/Sky Track.mp3")
font = pygame.font.SysFont("Comic Sans", 32)
menu_font = pygame.font.SysFont("Comic Sans", 26)
title_font = pygame.font.SysFont("Comic Sans", 62)
game_font = pygame.font.SysFont("Comic Sans", 42)
menu_sound = pygame.mixer.Sound("./assets/button-chime.wav")
bottle_sound = pygame.mixer.Sound("./assets/Bottle-placement.wav")
bottle_switch_sound = pygame.mixer.Sound("./assets/switch-bottle.wav")
winning_sound = pygame.mixer.Sound("./assets/Win-the-game.mp3")
selected = None
number_of_bottles = 6
matching = ''
matching_msg = ''
count_sound_arr = []
bottles_rects = []
bottle_images = []
bottle_frames = []
inner_bottles = []
shuffled_inner_bottles = []
bottle_paths = ['./assets/joan-tran-reEySFadyJQ-unsplash.jpg', './assets/Yellow Bottle.jpg', './assets/coffee.jpg', './assets/karl-kohler-dGIEMeN2MV8-unsplash.jpg', './assets/orange-juice.jpg', './assets/Coca-cola.jpg']
count_sounds = []
past_times = []
difficulty =''
pause = False
main_screen = True
frames_full = False
hints_shown = 0


#Load number sounds
for i in range(0,7):
    sound = pygame.mixer.Sound(f'./assets/number-{i}.wav')
    count_sound_arr.append(sound)




class BottleBox():
    def __init__(self, color, pos, width, height) -> None:
        self.width = width
        self.height = height
        self.bottle_number = None
        self.pos = pos
        self.box = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.color = color
        self.occupied = False

    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(screen, self.color, self.box, border_radius=15)


class Button:
    def __init__(self, surf, font, txt, color, pos, width, height):
        self.surf = surf
        self.font = font
        self.text = txt
        self.text_surf = self.font.render(self.text, True, PURPLE)
        self.color = color
        self.pos = pos
        self.height = height
        self.width = width
        self.button = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.text_rect = self.text_surf.get_rect(center = self.button.center)
        self.border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        self.clicked = False
        
    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(self.surf, PURPLE, self.border_rect, border_radius=15)
        pygame.draw.rect(self.surf, self.color, self.button, border_radius=15)
        self.surf.blit(self.text_surf, self.text_rect)
    
    def checkClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button.collidepoint(mouse_pos):
            if mouse_click[0] == 1 and self.clicked == False:
                # print("click")
                menu_sound.play()
                self.clicked = True
                return True
        if mouse_click[0] == 0:
            self.clicked = False

    
            
    
            
            


def config_game():
    global matching
    matching = ''
    bottle_frames.clear()
    bottle_images.clear()
    bottles_rects.clear()
    inner_bottles.clear()
    shuffled_inner_bottles.clear()
    append_bottles()
    shuffle_bottles()
    



def set_difficulty():
    global number_of_bottles
    if difficulty == "Easy":
        number_of_bottles = 4
    if difficulty == "Normal":
        number_of_bottles = 5
    if difficulty == "Hard":
        number_of_bottles = 6
            
 
 
            
def main_menu():
    global difficulty
    global pause
    pause = False 
    running = True
    while running:
        global number_of_bottles
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(LAVENDER)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if main_screen:
            title_surface = title_font.render("MATCH THAT BOTTLE", True, YELLOW)
            screen.blit(title_surface, (SCREEN_WIDTH //2 - title_surface.get_width()//2, 100))
            
            
            #MAIN MENU BUTTON LOGIC
            
            menu_x = SCREEN_WIDTH//2 - BUTTON_WIDTH//2
            menu_y = SCREEN_HEIGHT//2
            
            easy_btn = Button(screen, menu_font, "EASY", GREEN, (menu_x, menu_y), 175, 50)
            easy_btn.draw()
            
            normal_btn = Button(screen, menu_font, "NORMAL", GREEN, (menu_x, menu_y + 70), 175, 50)
            normal_btn.draw()
            
            hard_btn = Button(screen, menu_font, "HARD", GREEN, (menu_x, menu_y + 140), 175, 50)
            hard_btn.draw()
            
            # new_game = Button("NEW GAME", GREEN, (menu_x, menu_y), 175, 50)
            # new_game.draw()
            
            
            exit_btn = Button(screen, menu_font, "QUIT", RED, (menu_x, menu_y + 210), 175, 50)
            exit_btn.draw()

            pygame.display.update()
            
            # if new_game.checkClicked():
            #     config_game()
            #     # number_of_bottles = 4
            #     play_game()
            
            if easy_btn.checkClicked():
                difficulty = "Easy"
                set_difficulty()
                config_game()
                play_game()
            if normal_btn.checkClicked():
                difficulty = "Normal"
                set_difficulty()
                config_game()
                play_game()
            if hard_btn.checkClicked():
                difficulty = "Hard"
                set_difficulty()
                config_game()
                play_game()
                
                
            if exit_btn.checkClicked():
                running = False
                pygame.quit()
                sys.exit()



        

def shuffle_bottles():
    global shuffled_inner_bottles
    all_nums = [num for num in range(0, number_of_bottles)]
    # rand_nums = random.sample(all_nums, len(all_nums))
    shuffle(all_nums)
    # print(rand_nums)
    
    # for num in rand_nums: --> old way of shuffling
    for num in all_nums:
        shuffled_inner_bottles.append(inner_bottles[num])
    
    print(shuffled_inner_bottles)
    # print(all_nums)

        
        
  

def append_bottles():
    frame_x = 200
    frame_y = 300
    
    bottle_x = 50
    bottle_y = 100
    
    for i in range(0, number_of_bottles):
        gap = BOTTLE_GAP
        path = bottle_paths[i]
        cup_image = pygame.image.load(path).convert_alpha()
        cup_scaled = pygame.transform.scale(cup_image, IMAGE_SIZE)
        img_box = cup_scaled.get_rect()
        
        img_box.x += bottle_x
        img_box.y = bottle_y
        bottles_rects.append([img_box, i, False])
        bottle_images.append(cup_scaled)
        
        dupe_image = pygame.image.load(path).convert_alpha()
        dupe_scaled = pygame.transform.scale(dupe_image, IMAGE_SIZE)
        
        bottle_frame = BottleBox(YELLOW, (frame_x, frame_y), BOTTLE_WIDTH, BOTTLE_HEIGHT)
        bottle_frames.append(bottle_frame)
        
        inner_bottles.append([dupe_scaled, i])

        frame_x+=bottle_frame.width + gap
        bottle_x+= img_box.width + gap
        
        
def selected_bottle(frame_bottle_number):
    for bottle in bottles_rects:
        if bottle[1] == frame_bottle_number:
            return bottle

def selected_bottle_frame(bottle_number):
    for i, frame in enumerate(bottle_frames):
        if frame.bottle_number == bottle_number:
            return i
        
        
    
      
        
def drop_bottle(bottle, prev_center):
    old_bottle_num = selected_bottle_frame(bottle[1])
    print(old_bottle_num)
    for bottle_frame in bottle_frames:
        if bottle_frame.bottle_number == None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num == None:
            print("place bottle")
            bottle[0].center = bottle_frame.box.center
            bottle_frame.bottle_number = bottle[1]
            bottle_frame.occupied = True
            bottle[2] = True
            bottle_sound.play()
        elif bottle_frame.bottle_number == None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num != None:
            print("place new location")
            bottle[0].center = bottle_frame.box.center
            old_frame = bottle_frames[old_bottle_num]
            bottle_frame.bottle_number = bottle[1]
            old_frame.bottle_number = None
            bottle_frame.occupied = True
            bottle[2] = True 
            bottle_switch_sound.play()    
        elif bottle_frame.bottle_number != None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num != None:
            print("swap bottles")
            old_frame = bottle_frames[old_bottle_num]
            current_bottle = selected_bottle(bottle_frame.bottle_number)
            current_bottle[0].center = old_frame.box.center
            old_frame.bottle_number = current_bottle[1]
            bottle[0].center = bottle_frame.box.center
            bottle_frame.bottle_number = bottle[1]
            bottle_switch_sound.play()
        elif bottle_frame.bottle_number != None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num == None:
            print("swap and put back")
            current_bottle = selected_bottle(bottle_frame.bottle_number)
            current_bottle[0].center = prev_center
            bottle[0].center = bottle_frame.box.center
            bottle_frame.bottle_number = bottle[1]
            bottle_frame.occupied = True
            bottle_switch_sound.play()
                                  
        pygame.display.update()
        
        
        
def place_bottle(bottle_obj, prev_center):
    frame_list = [frame.box for frame in bottle_frames]
    rect = bottle_obj[0]
    # print(rect)
    if rect.collideobjects(frame_list) == None and bottle_obj[2] == False:
        # print(rect.collideobjects(frame_list))
        # print("No collide")
        bottle_obj[2] = False
        rect.center = prev_center
    elif rect.collideobjects(frame_list) == None and bottle_obj[2] == True:
        # print("still no collide")
        old_bottle_num = selected_bottle_frame(bottle_obj[1])
        if old_bottle_num != None:
            old_bottle_frame = bottle_frames[old_bottle_num]
            rect.center = old_bottle_frame.box.center
    else:
        # print("collide")
        drop_bottle(bottle_obj, prev_center)
        
        

def frames_all_full(top_nums):
    global frames_full
    arr = np.array(top_nums)
    
    if np.all(arr != None):
        frames_full = True
        return True
    else:
        return False



def update_match_count():
    global matching
    global matching_msg

    #array of the top bottle frames numbers
    bottom_nums = [inner[1] for inner in shuffled_inner_bottles]
    #array of the bottom bottles numbers
    top_nums = [frame.bottle_number for frame in bottle_frames]
    
    # print(top_nums)
    # print(bottom_nums)
    

    if frames_all_full(top_nums):
        count = 0
        for i, num in enumerate(bottom_nums):
            if num == top_nums[i]:
                count+= 1
        matching = str(count)
        matching_msg = f' BOTTLES MATCHED: {matching}'
        return count
    

def draw_pause():
    pause_width = 300
    pause_height = 500
    center_x = SCREEN_WIDTH//2 - pause_width//2
    center_y = SCREEN_HEIGHT//2 - pause_height//2
    pygame.draw.rect(surface,TRANSPARENT_PURPLE, [0,0, SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.draw.rect(surface, PURPLE, [center_x - 10, center_y - 10, pause_width + 20, pause_height + 20], 0, 10)
    pygame.draw.rect(surface, LAVENDER, [center_x, center_y, pause_width, pause_height], 0, 10)
    
    main_btn = Button(surface, menu_font, "MAIN MENU", WHITE, (center_x + 65, center_y + 80), BUTTON_WIDTH, BUTTON_HEIGHT)
    resume = Button(surface, menu_font, "RESUME", WHITE, (center_x + 65, center_y + 160), BUTTON_WIDTH, BUTTON_HEIGHT)
    restart = Button(surface, menu_font, "RESTART", WHITE, (center_x + 65, center_y + 240), BUTTON_WIDTH, BUTTON_HEIGHT)
    leave = Button(surface, menu_font, "QUIT", RED, (center_x + 65, center_y + 320), BUTTON_WIDTH, BUTTON_HEIGHT)
    
    main_btn.draw()
    resume.draw()
    restart.draw()
    leave.draw()
    screen.blit(surface, (0,0))
    
    return main_btn, restart, resume, leave


# def draw_hints():
#     hint_msg = 'SHOW HINT'
#     pause_text = font.render(hint_msg, True, WHITE)
#     pause_rect = pause_text.get_rect()
#     pause_rect.bottomleft = (10,SCREEN_HEIGHT - 10)
#     screen.blit(pause_text, pause_rect)
    
        






def play_game():
    global main_screen
    global pause
    global selected
    global matching
    global frames_full
    global hints_shown
    
    minutes = 0
    seconds = 0
    milliseconds = 0
    
    pause = False
    main_screen = False
    frames_full = False
    hints_shown = 0
    clock = pygame.time.Clock()
    # game_clock = pygame.time.Clock()
    running = True
    
    while running:   
        clock.tick(FPS)
        
        screen.fill(LAVENDER)
        
        #Update Game Clock
        
        #Draw top bottle frames where bottles images will be placed
        for frame in bottle_frames:
            frame.draw()
        
        
        #Handle button being pressed
        for event in pygame.event.get():
            # quit game by click exit on window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                print(pause)
            if not pause:
                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    if event.button == 1 and matching != str(number_of_bottles):
                        for num, bottle in enumerate(bottles_rects):   
                            if bottle[0].collidepoint(event.pos):
                                original_loc = bottle[0].center
                                selected = num
                if event.type == pygame.MOUSEBUTTONDOWN and pause:
                    print('unpause')
                    if resume.checkClicked():
                        pause = False
                        

                if event.type == pygame.MOUSEMOTION:
                    if selected != None:
                        bottles_rects[selected][0].move_ip(event.rel)
                if event.type == pygame.MOUSEBUTTONUP:
                    if selected != None:
                        # old_frame_num = selected_bottle_frame(selected)
                        place_bottle(bottles_rects[selected], original_loc)
                        
                    # for frame in bottle_frames:
                    #     print(frame.bottle_number)
                        selected = None
                        update_match_count()
                        index = update_match_count()
                        if index:
                            count_sound_arr[index].play()
                        center = ''
                        if matching == str(number_of_bottles):
                            winning_sound.play()
            
                
        #Draw moveable bottles at the top of the screen in their rects
        for i, image in enumerate(bottle_images):
            screen.blit(image, bottles_rects[i][0])
        
        #Draw Pause message
        pause_msg = 'PRESS "SPACEBAR" TO PAUSE'
        pause_text = font.render(pause_msg, True, WHITE)
        pause_rect = pause_text.get_rect()
        pause_rect.bottomleft = (10,SCREEN_HEIGHT - 10)
        screen.blit(pause_text, pause_rect)
        
        
        #Draw Hints Button
        hint_btn = Button(screen, font, "SHOW HINT",  LIGHT_BLUE, (SCREEN_WIDTH//2 - 100,700), 210, 50)
        if hints_shown < 2 and matching != str(number_of_bottles):
            hint_btn.draw()
        
        
        if hint_btn.checkClicked() and not pause and hints_shown < 2:
            hints_shown+=1
        
        
        
        

        
        #Display match count to player
        matching_text = game_font.render(matching_msg, True, WHITE)
        matching_rect = matching_text.get_rect()
        matching_rect.center= (SCREEN_WIDTH//2, SCREEN_HEIGHT//4)
        if matching != '':
            screen.blit(matching_text, matching_rect)
        
        #Display bottom Bottles
        for i, inner in enumerate(shuffled_inner_bottles):
            
            if matching != str(number_of_bottles):
                cover_border = pygame.rect.Rect(bottle_frames[i].pos[0] - 3.5, bottle_frames[i].pos[1] - 3.5 + BOTTLE_HEIGHT + SHELF_GAP, BOTTLE_WIDTH + 5, BOTTLE_HEIGHT + 5)
                cover = pygame.rect.Rect(bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP, BOTTLE_WIDTH, BOTTLE_HEIGHT)
                pygame.draw.rect(screen, DARK_PURPLE, cover_border, border_radius=10)
                pygame.draw.rect(screen, BLACK, cover, border_radius=10)
                question_image = pygame.image.load('./assets/neon-blue-question-mark-ikon-ikon-images.jpg').convert_alpha()
                question_scaled = pygame.transform.scale(question_image, IMAGE_SIZE)
                screen.blit(question_scaled, (bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP))
            else:
                screen.blit(inner[0], (bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP))
                restart = Button(screen, menu_font, "RESTART", GREEN, (10, 400), 175, 50)
                restart.draw()
                if restart.checkClicked() and pause == False:
                    config_game()
                    play_game()
            
            #SHOW HINTS
            for i in range(0, hints_shown):
                screen.blit(shuffled_inner_bottles[i][0], (bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP))
                

            #Pause Menu  button click logic
            if pause:
                main, res, resume, leave = draw_pause()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and pause:
                        print('unpause')
                        if main.checkClicked():
                            pause = False
                            running = False
                            main_screen = True
                            main_menu()
                        if resume.checkClicked():
                            pause = False
                        if res.checkClicked():
                            config_game()
                            play_game()
                        if leave.checkClicked():
                            running = False
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if pause:
                                pause = False
                            else:
                                pause = True                              
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                                
                                
                                
            #Update Game Clock
            if matching != str(number_of_bottles) and not pause:
                if milliseconds > 1000:
                    seconds += 1
                    milliseconds -= 1000
                if seconds > 60:
                    minutes += 1
                    seconds -= 60
                milliseconds += clock.tick_busy_loop(60)
            
            if minutes < 10 and seconds < 10:
                timetxt = game_font.render(f"0{minutes}:0{seconds}", True, WHITE)
            elif minutes < 10 and seconds >= 10:
                timetxt = game_font.render(f"0{minutes}:{seconds}", True, WHITE)
            elif minutes >= 10 and seconds < 10:
                timetxt = game_font.render(f"{minutes}:0{seconds}", True, WHITE)
            else:
                timetxt = game_font.render(f"{minutes}:{seconds}", True, WHITE)
            
            screen.blit(timetxt, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))
            
            if matching != str(number_of_bottles):
                past_times.append(timetxt)
            
                # print(past_times)
                            

                            
                
        
        
        
                     
        
        pygame.display.update()
        


if __name__ == "__main__":
    game_music.play(-1)
    main_menu()


