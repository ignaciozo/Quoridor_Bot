import numpy as np

class BoardInfo:
    BOARD_ROWS = 17
    BOARD_COLS = 17
    FREE_SQUARE = 0
    MY_PIECE = 1
    OPPONENT_PIECE = 2
    FREE_WALL = 3
    EXISTING_WALL = 4
    INTERSECTION = 5
    STOP = 0
    MOVE_STRAIGHT = 1
    MOVE_JUMP = 2
    NORTH_END_ROW = 0
    SOUTH_END_ROW = 16
    WEST_END_COL = 0
    EAST_END_COL = 16

class GamePlayer:
    def __init__(self, game_id, turn_token,side, walls, player_1, board, remaining_moves):
        
        self.game_id = game_id
        self.turn_token = turn_token
        self.side = side
        if self.side == "N":
            self.opponent_side = "S"
        else:
            self.opponent_side = "N"
        self.my_remaining_walls = walls
        self.player_1 = player_1
        self.board_str = board
        self.remaing_moves = remaining_moves
        self.board_array = np.zeros((289), dtype=int)
        self.board_array = self.translate_str_to_nparray(self.board_str)
        self.my_pieces = np.array(([-1,-1],[-1,-1],[-1,-1]),dtype=int)
    
    def update_pieces_location(self):
        for i in range(len(self.board_array)):
            if self.board_array[i] == BoardInfo.MY_PIECE:
                for j in range(len(self.my_pieces)):
                    if self.my_pieces[j] == [-1,-1]:
                        aux_row = i // BoardInfo.BOARD_ROWS
                        aux_col = i % BoardInfo.BOARD_ROWS
                        self.my_pieces[j] = [aux_row,aux_col]

    def translate_str_to_nparray(self, board):
        for i in range (len(board)):
            if (i // BoardInfo.BOARD_ROWS) % 2 == 0:
                if i % 2 == 0:
                    if self.board_str[i] == " ":
                        self.board_array[i] = BoardInfo.FREE_SQUARE
                    elif self.board_str[i] == self.side:
                        self.board_array[i] = BoardInfo.MY_PIECE
                    elif self.board_str[i] == self.opponent_side:
                        self.board_array[i] = BoardInfo.OPPONENT_PIECE
                    else:
                        print("Invalid piece character")
                else:
                    if self.board_str[i] == " ":
                        self.board_array[i] = BoardInfo.FREE_WALL
                    elif self.board_str[i] == "|":
                        self.board_array[i] = BoardInfo.EXISTING_WALL
                    else:
                        print("Invalid wall character")
            else:
                if (i % BoardInfo.BOARD_ROWS) % 2 == 0:
                    if self.board_str[i] == " ":
                        self.board_array[i] = BoardInfo.FREE_WALL
                    elif self.board_str[i] == "-":
                        self.board_array[i] = BoardInfo.EXISTING_WALL
                else:
                    self.board_array[i] = BoardInfo.INTERSECTION
    
    def move_piece ():
        
        
        None

        
        # from_col = i
        # from_row = j
        
        # k,l = 0,0
        
        # to_col = k
        # to_row = l    

        # board_array [from_col + from_row * BOARD_ROWS] = 0
        # board_array [to_col + to_row * BOARD_ROWS] = 1

    def locate_my_pieces (self):
        already_set = -1
        for i in range(self.board_array):
            if self.board_array[i] == BoardInfo.MY_PIECE:
                
                for j in range(len(self.my_pieces)):
                    #print(already_set)
                    if j > already_set:
                        aux_row = i // BoardInfo.BOARD_ROWS
                        aux_col = i % BoardInfo.BOARD_ROWS
                        self.my_pieces[j] = [aux_row,aux_col]
                        already_set=j
                        break
    
    def check_move_south (self,i):
        aux_row = self.my_pieces[i,0]
        if self.board_array[aux_row+2] == BoardInfo.FREE_SQUARE and self.board_array[aux_row+1] == BoardInfo.FREE_WALL and \
            self.board_array[aux_row+2] < BoardInfo.SOUTH_END_ROW:
            return BoardInfo.MOVE_STRAIGHT
        elif self.board_array[aux_row+2] == BoardInfo.OPPONENT_PIECE and self.board_array[aux_row+3] == BoardInfo.FREE_WALL and \
            self.board_array[aux_row+4] == BoardInfo.FREE_SQUARE and self.board_array[aux_row+4] < BoardInfo.SOUTH_END_ROW:
            return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP

    def check_move_north (self,i):
        aux_row = self.my_pieces[i,0]
        if self.board_array[aux_row-2] == BoardInfo.FREE_SQUARE and self.board_array[aux_row-1] == BoardInfo.FREE_WALL and \
            self.board_array[aux_row-2] > BoardInfo.NORTH_END_ROW:
            return BoardInfo.MOVE_STRAIGHT
        elif self.board_array[aux_row-2] == BoardInfo.OPPONENT_PIECE and self.board_array[aux_row-3] == BoardInfo.FREE_WALL and \
            self.board_array[aux_row-4] == BoardInfo.FREE_SQUARE and self.board_array[aux_row-4] > BoardInfo.NORTH_END_ROW:
            return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP

    def check_move_east (self,i):
        aux_col = self.my_pieces[0,i]
        if self.board_array[aux_col+2] == BoardInfo.FREE_SQUARE and self.board_array[aux_col+1] == BoardInfo.FREE_WALL and \
            self.board_array[aux_col+2] < BoardInfo.EAST_END_COL:
            return BoardInfo.MOVE_STRAIGHT
        elif self.board_array[aux_col+2] == BoardInfo.OPPONENT_PIECE and self.board_array[aux_col+3] == BoardInfo.FREE_WALL and \
            self.board_array[aux_col+4] == BoardInfo.FREE_SQUARE and self.board_array[aux_col+4] < BoardInfo.EAST_END_COL:
            return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP
    
    def check_move_west (self,i):
        aux_col = self.my_pieces[0,i]
        if self.board_array[aux_col-2] == BoardInfo.FREE_SQUARE and self.board_array[aux_col-1] == BoardInfo.FREE_WALL:
            return BoardInfo.MOVE_STRAIGHT
        elif self.board_array[aux_col-2] == BoardInfo.OPPONENT_PIECE and self.board_array[aux_col-3] == BoardInfo.FREE_WALL and \
            self.board_array[aux_col-4] == BoardInfo.FREE_SQUARE and self.board_array[aux_col-4] > BoardInfo.WEST_END_COL:
            return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP