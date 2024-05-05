import pygame, sys, random
import numpy as np

# import pickle


#Game Settings
FPS = 60
pygame.init()
pygame.mixer.init
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
PURPLE = (51, 0, 204)
LAVENDER = (105, 0, 196)
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
BOTTLE_WIDTH = 70
BOTTLE_HEIGHT = 90
IMAGE_SIZE = (BOTTLE_WIDTH, BOTTLE_HEIGHT)
SHELF_GAP = 10
BOTTLE_GAP = 15



#game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bottle Match Game")
game_music = pygame.mixer.Sound("./assets/Sky Track.mp3")
font = pygame.font.SysFont("Comic Sans", 26)
menu_font = pygame.font.SysFont("Comic Sans", 26)
title_font = pygame.font.SysFont("Comic Sans", 42)
menu_sound = pygame.mixer.Sound("assets/mixkit-light-spell-873.wav")
selected = None
number_of_bottles = 6
matching = ''
matching_msg = ''
bottles_rects = []
bottle_images = []
bottle_frames = []
inner_bottles = []
shuffled_inner_bottles = []
bottle_paths = ['assets/joan-tran-reEySFadyJQ-unsplash.jpg', 'assets/butterfly.webp', 'assets/coffee.jpg', 'assets/karl-kohler-dGIEMeN2MV8-unsplash.jpg', './assets/orange-juice.jpg', './assets/Coca-cola.jpg']
count_sounds = []
difficulty =''
pause = False

# cup_image = pygame.image.load('assets/martin-widenka-0rI80lQco18-unsplash.jpg').convert_alpha()
# cup_scaled = pygame.transform.scale(cup_image, IMAGE_SIZE)



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
    def __init__(self, txt, color, pos, width, height):
        self.text = txt
        self.text_surf = menu_font.render(self.text, True, PURPLE)
        self.color = color
        self.display_color = self.color
        self.hover_color = WHITE
        self.pos = pos
        self.height = height
        self.width = width
        self.button = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.text_rect = self.text_surf.get_rect(center = self.button.center)
        self.border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        self.clicked = False
        
    def draw(self):
        # border_rect = pygame.rect.Rect(self.pos[0] - 2, self.pos[1] - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(screen, PURPLE, self.border_rect, border_radius=15)
        pygame.draw.rect(screen, self.display_color, self.button, border_radius=15)
        screen.blit(self.text_surf, self.text_rect)
    
    def checkClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button.collidepoint(mouse_pos):
            self.display_color = self.hover_color
            if mouse_click[0] == 1 and self.clicked == False:
                # print("click")
                menu_sound.play()
                self.clicked = True
                return True
        if mouse_click[0] == 0:
            self.display_color = self.color
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
                
        
        title_surface = title_font.render("MATCH THAT BOTTLE", True, YELLOW)
        screen.blit(title_surface, (SCREEN_WIDTH //2 - title_surface.get_width()//2, 100))
        
        
        #MAIN MENU BUTTON LOGIC
        
        menu_x = 360
        menu_y = SCREEN_HEIGHT//2
        
        easy_btn = Button("EASY", GREEN, (menu_x, menu_y), 175, 50)
        easy_btn.draw()
        
        normal_btn = Button("NORMAL", GREEN, (menu_x, menu_y + 70), 175, 50)
        normal_btn.draw()
        
        hard_btn = Button("HARD", GREEN, (menu_x, menu_y + 140), 175, 50)
        hard_btn.draw()
        
        # new_game = Button("NEW GAME", GREEN, (menu_x, menu_y), 175, 50)
        # new_game.draw()
        
        
        exit_btn = Button("QUIT", RED, (menu_x, menu_y + 210), 175, 50)
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
    rand_nums = random.sample(all_nums, len(all_nums))
    # print(rand_nums)
    
    for num in rand_nums:
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
        elif bottle_frame.bottle_number == None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num != None:
            print("place new location")
            bottle[0].center = bottle_frame.box.center
            old_frame = bottle_frames[old_bottle_num]
            bottle_frame.bottle_number = bottle[1]
            old_frame.bottle_number = None
            bottle_frame.occupied = True
            bottle[2] = True     
        elif bottle_frame.bottle_number != None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num != None:
            print("swap bottles")
            old_frame = bottle_frames[old_bottle_num]
            current_bottle = selected_bottle(bottle_frame.bottle_number)
            current_bottle[0].center = old_frame.box.center
            old_frame.bottle_number = current_bottle[1]
            bottle[0].center = bottle_frame.box.center
            bottle_frame.bottle_number = bottle[1]
        elif bottle_frame.bottle_number != None and pygame.Rect.colliderect(bottle[0], bottle_frame.box) and old_bottle_num == None:
            print("swap and put back")
            current_bottle = selected_bottle(bottle_frame.bottle_number)
            current_bottle[0].center = prev_center
            bottle[0].center = bottle_frame.box.center
            bottle_frame.bottle_number = bottle[1]
            bottle_frame.occupied = True
                                  
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
    arr = np.array(top_nums)
    
    if np.all(arr != None):
        return True
    else:
        return False
    # for frame in bottle_frames:
    #     if frame.bottle_number == None:
    #         return False
    # return True


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
    matching_msg = f' Matching: {matching}'
        



    



def play_game():
    global guessed_letters
    clock = pygame.time.Clock()
    running = True
    global selected
    
    while running:   
        clock.tick(FPS)
        
        screen.fill(LAVENDER)
        
        for frame in bottle_frames:
            frame.draw()
        
        
        #Handle button being pressed
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and matching != str(number_of_bottles):
                    for num, bottle in enumerate(bottles_rects):   
                        if bottle[0].collidepoint(event.pos):
                            original_loc = bottle[0].center
                            selected = num

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
                    center = ''
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                    
            # quit game by click exit on window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
    
        for i, image in enumerate(bottle_images):
            screen.blit(image, bottles_rects[i][0])

        
        #Display match count to player
        matching_text = font.render(matching_msg, True, WHITE)
        matching_rect = matching_text.get_rect()
        matching_rect.center = (600, 50)
        screen.blit(matching_text, matching_rect)
        
        #Display bottom Bottles
        for i, inner in enumerate(shuffled_inner_bottles):
            
            if matching != str(number_of_bottles):
                cover_border = pygame.rect.Rect(bottle_frames[i].pos[0] - 2.5, bottle_frames[i].pos[1] - 2.5 + BOTTLE_HEIGHT + SHELF_GAP, BOTTLE_WIDTH + 5, BOTTLE_HEIGHT + 5)
                cover = pygame.rect.Rect(bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP, BOTTLE_WIDTH, BOTTLE_HEIGHT)
                pygame.draw.rect(screen, PURPLE, cover_border, border_radius=10)
                pygame.draw.rect(screen, LAVENDER, cover, border_radius=10)
                question_image = pygame.image.load('./assets/neon-blue-question-mark-ikon-ikon-images-Photoroom.png-Photoroom.png').convert_alpha()
                question_scaled = pygame.transform.scale(question_image, IMAGE_SIZE)
                # question_box = question_scaled.get_rect()
                screen.blit(question_scaled, (bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP))
            else:
                screen.blit(inner[0], (bottle_frames[i].pos[0], bottle_frames[i].pos[1] + BOTTLE_HEIGHT + SHELF_GAP))
                restart = Button("RESTART", GREEN, (50, 400), 175, 50)
                restart.draw()
                if restart.checkClicked():
                    config_game()
                    play_game()
                
        
        
        
                     
        
        pygame.display.update()
        


if __name__ == "__main__":
    game_music.play(-1)
    main_menu()


