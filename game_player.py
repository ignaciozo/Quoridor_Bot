from hashlib import new
from shutil import move
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
        already_set = -1
        for i in range(len(self.board_array)):
            if self.board_array[i] == BoardInfo.MY_PIECE:
                for j in range(len(self.my_pieces)):
                    if j > already_set:
                        aux_row = i // BoardInfo.BOARD_ROWS
                        aux_col = i % BoardInfo.BOARD_ROWS
                        self.my_pieces[j] = [aux_col,aux_row]
                        already_set = j
                        break
            if already_set == 2:
                break    
        if self.side == "N":  
            self.my_pieces = np.flip(self.my_pieces,0)

    def translate_str_to_nparray(self, board):
        #trimmed_str = board[2:289]
        self.board_str = board
        for i in range (len(self.board_str)):
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
        return self.board_array
    def move_piece (self,board):
        self.translate_str_to_nparray(board)
        #self.print_str(self.array_to_str())
        self.update_pieces_location()
        #print(self.my_pieces)
        coordinates = []
        if self.side == "N":
            for i in range(len(self.my_pieces)):
                if self.check_move_south(i) == 2:
                    coordinates = self.jump_south(i)
                    break
                elif self.check_move_south(i) == 1:
                    coordinates = self.move_south(i)
                    break
            if not coordinates:
                for i in range(len(self.my_pieces)):
                    if self.check_move_east(i) == 2:
                        coordinates = self.jump_east(i)
                        break
                    elif self.check_move_east(i) == 1:
                        coordinates = self.move_east(i)
                        break
                    elif self.check_move_west(i) == 2:
                        coordinates = self.jump_west(i)
                        break
                    elif self.check_move_west(i) == 1:
                        coordinates = self.move_west(i)
                        break
                    elif self.check_move_north(i) == 1:
                        coordinates = self.move_north(i)
                        break
        elif self.side == "S":
            for i in range(len(self.my_pieces)):
                if self.check_move_north(i) == 2:
                    coordinates = self.jump_north(i)
                    break
                elif self.check_move_north(i) == 1:
                    coordinates = self.move_north(i)
                    break
            if not coordinates:
                for i in range(len(self.my_pieces)):    
                    if self.check_move_east(i) == 2:
                        coordinates = self.jump_east(i)
                        break
                    elif self.check_move_east(i) == 1:
                        coordinates = self.move_east(i)
                        break
                    elif self.check_move_west(i) == 2:
                        coordinates = self.jump_west(i)
                        break
                    elif self.check_move_west(i) == 1:
                        coordinates = self.move_west(i)
                        break
                    elif self.check_move_south(i) == 1:
                        coordinates = self.move_south(i)
                        break
        
        return coordinates

    def locate_my_pieces (self):
        already_set = -1
        for i in range(len(self.board_array)):
            if self.board_array[i] == BoardInfo.MY_PIECE:
                
                for j in range(len(self.my_pieces)):
                    #print(already_set)
                    if j > already_set:
                        aux_row = i // BoardInfo.BOARD_ROWS
                        aux_col = i % BoardInfo.BOARD_ROWS
                        self.my_pieces[j] = [aux_col,aux_row]
                        already_set=j
                        break
    
    def check_move_south (self,i):
        piece_index = self.my_pieces[i,1] * BoardInfo.BOARD_ROWS + self.my_pieces [i,0]
        if self.board_array[piece_index+2*BoardInfo.BOARD_ROWS] == BoardInfo.FREE_SQUARE and self.board_array[piece_index+1*BoardInfo.BOARD_ROWS] == \
            BoardInfo.FREE_WALL and self.my_pieces[i,1] < BoardInfo.SOUTH_END_ROW:
            return BoardInfo.MOVE_STRAIGHT
        elif self.my_pieces[i,1] < BoardInfo.SOUTH_END_ROW - 2:
            if self.board_array[piece_index+2*BoardInfo.BOARD_ROWS] == BoardInfo.OPPONENT_PIECE and self.board_array[piece_index+3*BoardInfo.BOARD_ROWS] == \
            BoardInfo.FREE_WALL and self.board_array[piece_index+4*BoardInfo.BOARD_ROWS] == BoardInfo.FREE_SQUARE:
                return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP

    def check_move_north (self,i):
        piece_index = self.my_pieces[i,1] * BoardInfo.BOARD_ROWS + self.my_pieces [i,0]
        if self.board_array[piece_index-2*BoardInfo.BOARD_ROWS] == BoardInfo.FREE_SQUARE and self.board_array[piece_index-1*BoardInfo.BOARD_ROWS] == \
            BoardInfo.FREE_WALL and self.my_pieces[i,1] > BoardInfo.NORTH_END_ROW:
            return BoardInfo.MOVE_STRAIGHT
        elif self.my_pieces[i,1] > BoardInfo.NORTH_END_ROW + 2:
            if self.board_array[piece_index-2*BoardInfo.BOARD_ROWS] == BoardInfo.OPPONENT_PIECE and self.board_array[piece_index-3*BoardInfo.BOARD_ROWS] == \
            BoardInfo.FREE_WALL and self.board_array[piece_index-4*BoardInfo.BOARD_ROWS] == BoardInfo.FREE_SQUARE:
                return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP

    def check_move_east (self,i):
        piece_index = self.my_pieces[i,1] * BoardInfo.BOARD_ROWS + self.my_pieces [i,0]
        if self.board_array[piece_index+2] == BoardInfo.FREE_SQUARE and self.board_array[piece_index+1] == BoardInfo.FREE_WALL and \
            self.board_array[piece_index+2] < BoardInfo.EAST_END_COL:
            return BoardInfo.MOVE_STRAIGHT
        elif self.my_pieces[i,1] < BoardInfo.EAST_END_COL - 2:
            if self.board_array[piece_index+2] == BoardInfo.OPPONENT_PIECE and self.board_array[piece_index+3] == BoardInfo.FREE_WALL and \
            self.board_array[piece_index+4] == BoardInfo.FREE_SQUARE:
                return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP
    
    def check_move_west (self,i):
        piece_index = self.my_pieces[i,1] * BoardInfo.BOARD_ROWS + self.my_pieces [i,0]
        if self.board_array[piece_index-2] == BoardInfo.FREE_SQUARE and self.board_array[piece_index-1] == BoardInfo.FREE_WALL:
            return BoardInfo.MOVE_STRAIGHT
        elif self.my_pieces[i,1] > BoardInfo.WEST_END_COL + 2:
            if self.board_array[piece_index-2] == BoardInfo.OPPONENT_PIECE and self.board_array[piece_index-3] == BoardInfo.FREE_WALL and \
            self.board_array[piece_index-4] == BoardInfo.FREE_SQUARE:
                return BoardInfo.MOVE_JUMP
        else:
            return BoardInfo.STOP
    
    def move_south (self,i):
        
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] + 2
        to_col = self.my_pieces[i,0]
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("moving south")
        return coordinates

    def move_north (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] - 2
        to_col = self.my_pieces[i,0]
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("moving north")
        return coordinates
    
    def move_east (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1]
        to_col = self.my_pieces[i,0] + 2
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("moving east")
        return coordinates

    def move_west (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1]
        to_col = self.my_pieces[i,0] - 2
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("moving west")
        return coordinates

    def jump_south (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] + 4
        to_col = self.my_pieces[i,0]
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("jumping south")
        return coordinates

    def jump_north (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] - 4
        to_col = self.my_pieces[i,0]
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("jumping north")
        return coordinates

    def jump_east (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] 
        to_col = self.my_pieces[i,0] + 4
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("jumping east")
        return coordinates

    def jump_west (self,i):
        from_row = self.my_pieces[i,1]
        from_col = self.my_pieces[i,0]
        to_row = self.my_pieces[i,1] 
        to_col = self.my_pieces[i,0] - 4
        self.board_array [from_col + from_row * BoardInfo.BOARD_ROWS] = 0
        self.board_array [to_col + to_row * BoardInfo.BOARD_ROWS] = 1
        coordinates = [from_row,from_col,to_row,to_col]
        print("jumping west")
        return coordinates

    def array_to_str (self):
        
        new_board_str = ""
        for i in range(len(self.board_array)):
            if self.board_array[i] == BoardInfo.FREE_SQUARE:
                new_board_str += " "
            elif self.board_array[i] == BoardInfo.MY_PIECE:
                new_board_str += self.side
            elif self.board_array[i] == BoardInfo.OPPONENT_PIECE:
                new_board_str += self.opponent_side
            elif self.board_array[i] == BoardInfo.FREE_WALL:
                new_board_str += " "
            elif self.board_array[i] == BoardInfo.EXISTING_WALL:
                if i // BoardInfo.BOARD_ROWS % 2 == 0:
                    new_board_str += "|"
                else:
                    new_board_str += "-"
            else:
                new_board_str += " "
        return new_board_str

    def print_str(self,board):
        print ("  0a1b2c3d4e5f6g7h8"+"\n  -----------------")
        for i in range(len(board)):
            if (i // BoardInfo.BOARD_ROWS) % 2 == 0:
                if i % BoardInfo.BOARD_ROWS == 0:
                    print(str(i//BoardInfo.BOARD_ROWS//2)+'|'+board[i], sep='', end='')
                else:
                    print(board[i], sep='', end='')
                if i > 1 and ((i+1) % BoardInfo.BOARD_ROWS) == 0:
                        print("")
            else:
                if i % BoardInfo.BOARD_ROWS == 0:
                    j = (i // BoardInfo.BOARD_ROWS)//2+97
                    print(chr(j)+'|'+board[i], sep='', end='')
                else:
                    print(board[i], sep='', end='')
                if i > BoardInfo.BOARD_ROWS and ((i+1) % BoardInfo.BOARD_ROWS) == 0:
                        print("")