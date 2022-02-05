import pygame
import random
 
# === CONSTANS ===
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
MAIN_THEME = (246, 197, 233)
BLUE  = (  0,   0, 255)
 
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600

TILESIZE = 30
TILE_MARGIN = 1

LETTER_SCORE = {
    'A': 1,
    'B': 9,
    'C': 1,
    'D': 2,
    'E': 1,
    'F': 8,
    'G': 9,
    'H': 10,
    'I': 1,
    'J': 10,
    'L': 1,
    'M': 4,
    'N': 1,
    'O': 1,
    'P': 2,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 8,
    'X': 10,
    ':)': 0
}

LETTER_COUNT = {
    'A': 11,
    'B': 2,
    'C': 5,
    'D': 4,
    'E': 9,
    'F': 2,
    'G': 2,
    'H': 1,
    'I': 10,
    'J': 1,
    'L': 4,
    'M': 3,
    'N': 6,
    'O': 5,
    'P': 4,
    'R': 7,
    'S': 5,
    'T': 7,
    'U': 6,
    'V': 2,
    'X': 1,
    ':)': 2
}

BOARD_POS = (10, 10)

PLAYER_BOARD_POS = (10, 500)

# === CLASSES ===
   
# === FUNCTIONS ===

def create_board_surf():
    board_surf = pygame.Surface((TILESIZE*15, TILESIZE*15))
    for y in range(15):
        for x in range(15):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, MAIN_THEME, rect)
    return board_surf

def create_board():
    board = []
    for y in range(15):
        board.append([])
        for x in range(15):
            board[y].append(None)
    return board

# Creates a surface for an empty board with 8 tiles
def create_player_board_surf():
    player_pieces_surf = pygame.Surface((TILESIZE*8, TILESIZE))
    for x in range(8):
        rect = pygame.Rect(x*TILESIZE, 0, TILESIZE, TILESIZE)
        pygame.draw.rect(player_pieces_surf, MAIN_THEME, rect)
    return player_pieces_surf

# Creates the initial pieces for a player
def create_player_board(shuffled_letters: list):
    player_board = [None] * 8
    for x in range(7):
        player_board[x] = shuffled_letters.pop()
    return player_board

# Shuffle letters in random order and return a list from which to take letters
def shuffle_letters():
    letters = []
    for letter in LETTER_COUNT.keys():
        for i in range(LETTER_COUNT[letter]):
            letters.append(letter)
    random.shuffle(letters)
    # print ('Shuffled letters are:', letters)
    return letters

def draw_player_pieces(screen, player_board, font):
    for x in range(8): 
        letter = player_board[x]
        if letter is not None:
            print (f'Position {x}: letter: {letter}')
            letter_render = font.render(letter, True, BLACK)   # Letter
            letter_rect = pygame.Rect(PLAYER_BOARD_POS[0] + x*TILESIZE+TILE_MARGIN, PLAYER_BOARD_POS[1]+TILE_MARGIN, TILESIZE-TILE_MARGIN*2, TILESIZE-TILE_MARGIN*2)
            pygame.draw.rect(screen, WHITE, letter_rect)
            screen.blit(letter_render, letter_render.get_rect(center=letter_rect.center))

# === MAIN === 

# --- (global) variables ---

# --- init ---
 
pygame.init()
letter_font = pygame.font.SysFont('', 32)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
board_surf = create_board_surf()

shuffled_letters = shuffle_letters()
player_board_surf = create_player_board_surf()
player_board = create_player_board(shuffled_letters)

# --- objects ---

selected = None
   
# --- mainloop ---
 
clock = pygame.time.Clock()
is_running = True
 
while is_running:
 
    # --- events ---
   
    for event in pygame.event.get():
 
        # --- global events ---
       
        if event.type == pygame.QUIT:
            is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
        
 
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         for i, r in enumerate(pieces):
        #             if r.collidepoint(event.pos):
        #                 selected = i
        #                 selected_offset_x = r.x - event.pos[0]
        #                 selected_offset_y = r.y - event.pos[1]
               
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 1:
        #         selected = None
               
        # elif event.type == pygame.MOUSEMOTION:
        #     if selected is not None: # selected can be `0` so `is not None` is required
        #         # move object
        #         pieces[selected].x = event.pos[0] + selected_offset_x
        #         pieces[selected].y = event.pos[1] + selected_offset_y
               
        # --- objects events ---
       
    # --- updates ---
 
       
    # --- draws ---
   
    screen.fill(WHITE)
    screen.blit(board_surf, BOARD_POS)
    screen.blit(player_board_surf, PLAYER_BOARD_POS)
   
    # draw pieces
    draw_player_pieces(screen, player_board, letter_font)
       
    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(60)
 
# --- the end ---
   
pygame.quit()