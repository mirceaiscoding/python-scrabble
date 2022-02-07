from operator import le
import pygame
import random
 
# === CONSTANS ===
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

# MAIN_THEME = (246, 197, 233)
# X3_WORD_COLOR = (134, 87, 255)
# X2_WORD_COLOR = (140, 155, 194)

MAIN_THEME = (188, 197, 220)
X3_WORD_COLOR = (13, 112, 75)
X2_WORD_COLOR = (132, 214, 127)
X2_LETTER_COLOR = (134, 87, 255)
X3_LETTER_COLOR = (234, 207, 150)
START_COLOR = (246, 197, 233)

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

SUBMIT_BUTTON_POS = (300, 505)

X2_WORD_SPOTS = [(1, 1), (2, 2), (3, 3), (4, 4), (13, 1), (12, 2), (11, 3), (10, 4), (1, 13), (2, 12), (3, 11), (4, 10), (10, 10), (11, 11), (12, 12), (13, 13)]
X3_WORD_SPOTS = [(0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14)]
X2_LETTER_SPOTS = [(3, 0), (0, 3), (6, 2), (2, 6), (7, 3), (3, 7), (8, 2), (2, 8), (11, 0), (0, 11), (6, 6), (8, 8), (6, 8), (8, 6), (3, 14), (14, 3), (6, 12), (12, 6), (7, 11), (11, 7), (8, 12), (12, 8), (11, 14), (14, 11)]
X3_LETTER_SPOTS = [(5, 1), (1, 5), (1, 9), (9, 1), (5, 5), (9, 9), (5, 9), (9, 5), (13, 5), (5, 13), (9, 13), (13, 9)]
START_TILE = (7, 7)

# === CLASSES ===
   
buttons = []

class Button:
	def __init__(self,text,width,height,pos,elevation,font):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		self.font = font
 
		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'
 
		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'

		#text
		self.text = text
		self.text_surf = self.font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
		buttons.append(self)
 
	def change_text(self, newtext):
		self.text_surf = self.font.render(newtext, True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
 
	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 
 
		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
 
		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()
 
	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
				self.change_text(f"{self.text}")
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					print('click')
					self.pressed = False
					self.change_text(self.text)
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'

# === FUNCTIONS ===

# Creates the board surface
def create_board_surf(board):
    board_surf = pygame.Surface((TILESIZE*15, TILESIZE*15))
    for y in range(15):
        for x in range(15):
            rect = pygame.Rect(x*TILESIZE+TILE_MARGIN, y*TILESIZE+TILE_MARGIN, TILESIZE-TILE_MARGIN*2, TILESIZE-TILE_MARGIN*2)
            (tile_tipe, tile) = board[y][x]
            if (tile_tipe == 'X3Word'):
                pygame.draw.rect(board_surf, X3_WORD_COLOR, rect)
                continue
            if (tile_tipe == 'X2Word'):
                pygame.draw.rect(board_surf, X2_WORD_COLOR, rect)
                continue
            if (tile_tipe == 'X2Letter'):
                pygame.draw.rect(board_surf, X2_LETTER_COLOR, rect)
                continue
            if (tile_tipe == 'X3Letter'):
                pygame.draw.rect(board_surf, X3_LETTER_COLOR, rect)
                continue
            if (tile_tipe == 'Start'):
                pygame.draw.rect(board_surf, START_COLOR, rect)
                continue
            pygame.draw.rect(board_surf, MAIN_THEME, rect)
    return board_surf

# Creates an empty board with the right tile multipliers in place
def create_board():
    board = []
    for y in range(15):
        board.append([])
        for x in range(15):
            board[y].append(('Normal', None))

    for (x, y) in X2_WORD_SPOTS:
        board[y][x] = (('X2Word', None))
    
    for (x, y) in X3_WORD_SPOTS:
        board[y][x] = (('X3Word', None))

    for (x, y) in X2_LETTER_SPOTS:
        board[y][x] = (('X2Letter', None))

    for (x, y) in X3_LETTER_SPOTS:
        board[y][x] = (('X3Letter', None))

    (x, y) = START_TILE
    board[y][x] = (('Start', None))

    return board

# Checks if a spot on the board is free
def is_free_board_spot(board, x, y):
    (tile_tipe, letter) = board[y][x]
    return letter == None

# Clears a tile (either on the board or the player board)
def clear_tile(board, player_board, board_type, x, y):
    if board_type is not None:
        if board_type == 'Player Board':
            letter = player_board[x]
            player_board[x] = None
        if board_type == 'Board':
            (mult, letter) = board[y][x]
            board[y][x] = (mult, None)
        return letter

# Puts the tile on the board
def put_tile_on_board(board, x, y, tile):
    (mult, crt_tile) = board[y][x]
    board[y][x] = (mult, tile)


# Returns the tile under the mouse (either on the main board or on the player board)
def get_tile_under_mouse(board, player_board):

    mouse_pos_on_board = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos_on_board]
    if x >= 0 and y >= 0 and x < 15 and y < 15: return ('Board', board[y][x][1], x, y)

    mouse_pos_on_player_board = pygame.Vector2(pygame.mouse.get_pos()) - PLAYER_BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos_on_player_board]
    if x >= 0 and y == 0 and x < 8: return ('Player Board', player_board[x], x, y)

    return None, None, None, None

def draw_drag_tile(screen, board, player_board, selected_tile, font):
    if selected_tile and selected_tile[0]:

        selected_piece = selected_tile[1]

        # board_type, piece, x, y = get_tile_under_mouse(board, player_board)

        # if x != None:
        #     rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        #     pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        pos = pygame.Vector2(pygame.mouse.get_pos()) # Mouse position
        letter_render = font.render(selected_piece, True, BLACK)   # Letter
        letter_rect = pygame.Rect(0, 0, TILESIZE-TILE_MARGIN*2, TILESIZE-TILE_MARGIN*2)
        letter_rect.center = pos
        pygame.draw.rect(screen, WHITE, letter_rect)
        screen.blit(letter_render, letter_render.get_rect(center=letter_rect.center))

# Creates a surface for an empty player board with 8 tiles
def create_player_board_surf():
    player_pieces_surf = pygame.Surface((TILESIZE*8, TILESIZE))
    for x in range(8):
        rect = pygame.Rect(x*TILESIZE, 0, TILESIZE, TILESIZE)
        pygame.draw.rect(player_pieces_surf, MAIN_THEME, rect)
    return player_pieces_surf

# Creates the initial pieces for a player
def create_player_pieces(shuffled_letters: list):
    player_pieces = [None] * 8
    for x in range(7):
        player_pieces[x] = shuffled_letters.pop()
    return player_pieces

# Shuffle letters in random order and return a list from which to take letters
def shuffle_letters():
    letters = []
    for letter in LETTER_COUNT.keys():
        for i in range(LETTER_COUNT[letter]):
            letters.append(letter)
    random.shuffle(letters)
    # print ('Shuffled letters are:', letters)
    return letters

def draw_player_pieces(screen, player_pieces, font, selected_tile):
    if selected_tile:
        selected_board_type = selected_tile[0]
        selected_x = selected_tile[2]
    for x in range(8): 
        letter = player_pieces[x]
        if letter is not None:
            # print (f'Position {x}: letter: {letter}')
            if selected_tile and selected_board_type == 'Player Board' and x == selected_x:
                continue
            letter_render = font.render(letter, True, BLACK)   # Letter
            letter_rect = pygame.Rect(PLAYER_BOARD_POS[0] + x*TILESIZE+TILE_MARGIN, PLAYER_BOARD_POS[1]+TILE_MARGIN, TILESIZE-TILE_MARGIN*2, TILESIZE-TILE_MARGIN*2)
            pygame.draw.rect(screen, WHITE, letter_rect)
            screen.blit(letter_render, letter_render.get_rect(center=letter_rect.center))

def draw_board_pieces(screen, board, font, selected_tile):
    if selected_tile:
        selected_board_type = selected_tile[0]
        selected_x = selected_tile[2]
        selected_y = selected_tile[3]
    for y in range(15):
        for x in range(15):
            letter = board[y][x][1]
            if letter is not None:
                # print (f'Position {x}, {y}: letter: {letter}')
                if selected_tile and selected_board_type == 'Board' and x == selected_x and y == selected_y:
                    continue
                letter_render = font.render(letter, True, BLACK)   # Letter
                letter_rect = pygame.Rect(BOARD_POS[0] + x*TILESIZE+TILE_MARGIN, BOARD_POS[1] + y*TILESIZE+TILE_MARGIN, TILESIZE-TILE_MARGIN*2, TILESIZE-TILE_MARGIN*2)
                pygame.draw.rect(screen, WHITE, letter_rect)
                screen.blit(letter_render, letter_render.get_rect(center=letter_rect.center))

def draw_buttons():
	for b in buttons:
		b.draw()

# === MAIN === 

# --- (global) variables ---

# --- init ---
 
pygame.init()
letter_font = pygame.font.SysFont('', 24)
bonus_font = pygame.font.SysFont('', 20)
button_font = pygame.font.SysFont('', 100)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

board = create_board()
board_surf = create_board_surf(board)

shuffled_letters = shuffle_letters()
player_board_surf = create_player_board_surf()
player_board = create_player_pieces(shuffled_letters)

submit_button = Button('Submit', 80, 20, SUBMIT_BUTTON_POS, 1, letter_font)

# --- objects ---

selected = None
   
# --- mainloop ---
 
clock = pygame.time.Clock()
is_running = True
selected_tile = None
 
while is_running:

    tile = get_tile_under_mouse(board, player_board)
    board_type, piece, x, y = tile
 
    # --- events ---
   
    for event in pygame.event.get():
 
        # --- global events ---
       
        if event.type == pygame.QUIT:
            is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if piece is not None:
                    selected_tile = tile
               
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected_tile is not None:
                    (selected_tile_board, selected_piece, selected_x, selected_y) = selected_tile
                    if board_type == 'Player Board':
                        if selected_tile_board == 'Player Board':
                            # Move from player board to player board
                            print ('Move piece to player board')
                            if piece is None:
                                # Free space => Just put it there
                                player_board[selected_x] = None
                                player_board[x] = selected_piece
                            else:
                                # Put the selected piece on position x and shift the other pieces to the left/right to make space
                                if selected_x < x:
                                    direction = -1
                                else:
                                    direction = 1
                                
                                player_board[selected_x] = None
                                position_to_move = x
                                piece_to_move = player_board[position_to_move]
                                player_board[position_to_move] = selected_piece
                                while piece_to_move is not None:
                                    position_to_move += direction
                                    next_piece = player_board[position_to_move]
                                    player_board[position_to_move] = piece_to_move
                                    piece_to_move = next_piece

                        if selected_tile_board == 'Board':
                            # Move from board to player board
                            clear_tile(board, player_board, selected_tile_board, selected_x, selected_y)
                            
                    if board_type == 'Board':
                        # Move to board
                        print ('Move piece to board')
                        if is_free_board_spot(board, x, y):
                            print("Move to free spot")
                            clear_tile(board, player_board, selected_tile_board, selected_x, selected_y)
                            put_tile_on_board(board, x, y, selected_piece)

                    selected_tile = None
       
    # --- updates ---
 
       
    # --- draws ---
   
    screen.fill(WHITE)
    screen.blit(board_surf, BOARD_POS)
    screen.blit(player_board_surf, PLAYER_BOARD_POS)
   
    # draw pieces
    draw_player_pieces(screen, player_board, letter_font, selected_tile)
    draw_board_pieces(screen, board, letter_font, selected_tile)

    # draw the tile as it is dragged
    draw_drag_tile(screen, board, player_board, selected_tile, letter_font)
       
    # draw buttons
    draw_buttons()

    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(60)
 
# --- the end ---
   
pygame.quit()