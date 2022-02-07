from operator import le
import re
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
	def __init__(self,text,width,height,pos,elevation,font,click_function):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		self.font = font
		self.click_function = click_function
 
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
					print('clicked')
					self.pressed = False
					self.change_text(self.text)
					self.click_function(board, player_board)
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
            (tile_type, tile) = board[y][x]
            if (tile_type == 'X3Word'):
                pygame.draw.rect(board_surf, X3_WORD_COLOR, rect)
                continue
            if (tile_type == 'X2Word'):
                pygame.draw.rect(board_surf, X2_WORD_COLOR, rect)
                continue
            if (tile_type == 'X2Letter'):
                pygame.draw.rect(board_surf, X2_LETTER_COLOR, rect)
                continue
            if (tile_type == 'X3Letter'):
                pygame.draw.rect(board_surf, X3_LETTER_COLOR, rect)
                continue
            if (tile_type == 'Start'):
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

def get_free_player_board_spot(player_board, x):
    for i in range(x, 8):
        if player_board[i] == None:
            return i
    for i in range(x-1, -1, -1):
        if player_board[i] == None:
            return i

# places selected piece to x position and fixes the other pieces
def place_selected_piece_fix_player_board(player_board, x, selected_x, selected_piece, direction):
    position_to_move = x
    piece_to_move = player_board[position_to_move]
    player_board[position_to_move] = selected_piece
    while piece_to_move is not None:
        position_to_move += direction
        next_piece = player_board[position_to_move]
        player_board[position_to_move] = piece_to_move
        piece_to_move = next_piece

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

# draws the selected tile at the mouse position
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

# Get a list of the newly placed letter positions
def get_placed_letters_positions():
    placed_letters_positions = []
    for y in range(15):
        for x in range(15):
            (tile_tipe, tile) = board[y][x]
            if tile is not None and tile_tipe != 'Fixed':
                placed_letters_positions.append((x, y))
    print (f'Placed letters positions are {placed_letters_positions}')
    return placed_letters_positions


def has_adjacent_vertical_letters(board, position):
    x, y = position
    tile_type, tile = board[y][x]
    for (adjacent_x, adjacent_y) in [(x, y-1), (x, y+1)]:
        tile_type, tile = board[adjacent_y][adjacent_x]
        if tile is not None:
            return True
    return False

def has_adjacent_horizontal_letters(board, position):
    x, y = position
    tile_type, tile = board[y][x]
    for (adjacent_x, adjacent_y) in [(x-1, y), (x+1, y)]:
        tile_type, tile = board[adjacent_y][adjacent_x]
        if tile is not None:
            return True
    return False


# Return true if position is next to a fixed letter or position is a start tile
def has_adjacent_fixed_letters_or_is_start(board, position):
    x, y = position
    tile_type, tile = board[y][x]
    if tile_type == 'Start':
        print ('Start position')
        return True
    for (adjacent_x, adjacent_y) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        tile_type, tile = board[adjacent_y][adjacent_x]
        if tile_type == 'Fixed':
            return True
    return False

def has_no_empty_spots(board, direction, stable_coordinate, min, max):
    if direction == 'Vertical':
        print(f'Checking for empty spots x={stable_coordinate}, y=[{min},{max}]')
        # X is stable, check Y
        for y in range(min, max+1):
            tile_type, tile = board[y][stable_coordinate]
            if tile is None:
                return False
        return True
    if direction == 'Horizontal':
        # Y is stable, check X
        print(f'Checking for empty spots y={stable_coordinate}, x=[{min},{max}]')
        for x in range(min, max+1):
            tile_type, tile = board[stable_coordinate][x]
            if tile is None:
                return False
        return True

# Check if positions are in a row / column
def check_placed_letters_positions(board, placed_letters_positions):
    flag = False
    (min_x, min_y) = (max_x, max_y) = placed_letters_positions[0]
    for (x, y) in placed_letters_positions:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        flag = flag or has_adjacent_fixed_letters_or_is_start(board, (x, y))
        
    if flag == False:
        return False, None
    
    print(f'x=[{min_x},{max_x}] y=[{min_y}, {max_y}]')

    if min_x == max_x:
        return has_no_empty_spots(board, 'Vertical', min_x, min_y, max_y), 'Vertical'
    
    if min_y == max_y:
        return has_no_empty_spots(board, 'Horizontal', min_y, min_x, max_x), 'Horizontal'

    return False, None


def get_horizontal_word(board, pos):
    x, y = pos
    score = 0
    word = ''
    word_multiplier = 1
    while board[y][x][1] is not None:
        tile_type, tile = board[y][x]
        letter_score = LETTER_SCORE[tile]
        if tile_type == 'X2Letter':
            letter_score *= 2
        if tile_type == 'X3Letter':
            letter_score *= 3
        if (tile_type == 'X2Word'):
            word_multiplier *= 2
        if (tile_type == 'X2Word'):
            word_multiplier *= 3
        
        word = tile + word
        score += letter_score
        x -= 1
    x, y = pos
    x += 1
    while board[y][x][1] is not None:
        tile_type, tile = board[y][x]
        letter_score = LETTER_SCORE[tile]
        if tile_type == 'X2Letter':
            letter_score *= 2
        if tile_type == 'X3Letter':
            letter_score *= 3
        if (tile_type == 'X2Word'):
            word_multiplier *= 2
        if (tile_type == 'X2Word'):
            word_multiplier *= 3
        word = word + tile
        score += letter_score
        x += 1
    score *= word_multiplier
    return (word, score)

def get_vertical_word(board, pos):
    x, y = pos
    score = 0
    word = ''
    word_multiplier = 1
    while board[y][x][1] is not None:
        tile_type, tile = board[y][x]
        letter_score = LETTER_SCORE[tile]
        if tile_type == 'X2Letter':
            letter_score *= 2
        if tile_type == 'X3Letter':
            letter_score *= 3
        if (tile_type == 'X2Word'):
            word_multiplier *= 2
        if (tile_type == 'X2Word'):
            word_multiplier *= 3
        word = tile + word
        score += letter_score
        y -= 1
    x, y = pos
    y += 1
    while board[y][x][1] is not None:
        tile_type, tile = board[y][x]
        letter_score = LETTER_SCORE[tile]
        if tile_type == 'X2Letter':
            letter_score *= 2
        if tile_type == 'X3Letter':
            letter_score *= 3
        if (tile_type == 'X2Word'):
            word_multiplier *= 2
        if (tile_type == 'X2Word'):
            word_multiplier *= 3
        word = word + tile
        score += letter_score
        y += 1
    score *= word_multiplier
    return (word, score)
        

def get_newly_created_words(board, placed_letters_positions, direction):
    words = []
    total_score = 0
    first_pos = placed_letters_positions[0]
    if direction == 'Horizontal':
        main_word, main_score = get_horizontal_word(board, first_pos)
        words.append(main_word)
        total_score += main_score
        for pos in placed_letters_positions:
            if has_adjacent_vertical_letters(board, pos):
                word, score = get_vertical_word(board, pos)
                words.append(word)
                total_score += score
    if direction == 'Vertical':
        main_word, main_score = get_vertical_word(board, first_pos)
        words.append(main_word)
        total_score += main_score
        for pos in placed_letters_positions:
            if has_adjacent_horizontal_letters(board, pos):
                word, score = get_horizontal_word(board, pos)
                words.append(word)
                total_score += score
    print(f'Words {words} => {total_score}')
    return words, total_score


def check_words(new_words):
    # TODO: implement this:
    return True

def return_letters(player_board, board, placed_letters_positions):
    player_board_x = 0
    while len(placed_letters_positions) > 0:
        if player_board[player_board_x] is None:
            x, y = placed_letters_positions.pop()
            tile_type, tile = board[y][x]
            board[y][x] = (tile_type, None)
            player_board[player_board_x] = tile
        player_board_x += 1
        

def get_score(placed_letters_positions):
    # TODO: implement this:
    return 0

def get_new_letters(player_board, number_of_letters):
    x = 0
    while number_of_letters > 0 and len(shuffled_letters) > 0 and x < 8:
        if player_board[x] == None:
            player_board[x] = shuffled_letters.pop()
            number_of_letters -= 1
        x += 1

def mark_letters_as_fixed(board, placed_letters_positions):
    for (x, y) in placed_letters_positions:
        tile_type, tile = board[y][x]
        board[y][x] = ('Fixed', tile)


def click_submit_button(board, player_board):
    global turn_count

    placed_letters_positions = get_placed_letters_positions()

    if placed_letters_positions == []:
        return

    is_in_line, direction = check_placed_letters_positions(board, placed_letters_positions)

    if is_in_line == False:
        print('Letters can not be placed like this!')
        return_letters(player_board, board, placed_letters_positions)
        return

    new_words = get_newly_created_words(board, placed_letters_positions, direction)

    if check_words(new_words) == False:
        score = 0
        # return letters to player
        return_letters(player_board, board, placed_letters_positions)
        return
    else:
        score = get_score(placed_letters_positions)
        number_of_placed_letters = len(placed_letters_positions)
        get_new_letters(player_board, number_of_placed_letters)

    mark_letters_as_fixed(board, placed_letters_positions)

    # Increment turn count
    turn_count += 1
    print(f'Turn {turn_count}')
    

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

turn_count = 0

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

submit_button = Button('Submit', 80, 20, SUBMIT_BUTTON_POS, 1, letter_font, click_submit_button)

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
                    if (board_type == 'Board' and board[y][x][0] != 'Fixed') or board_type == 'Player Board':
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
                                place_selected_piece_fix_player_board(player_board, x, selected_x, selected_piece, direction)

                        if selected_tile_board == 'Board':
                            # Move from board to player board
                            clear_tile(board, player_board, selected_tile_board, selected_x, selected_y)
                            if piece is None:
                                # Free space => Just put it there
                                player_board[x] = selected_piece
                            else:
                                free_x = get_free_player_board_spot(player_board, x)
                                if free_x < x:
                                    direction = -1
                                else:
                                    direction = 1

                                place_selected_piece_fix_player_board(player_board, x, selected_x, selected_piece, direction)

                            
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