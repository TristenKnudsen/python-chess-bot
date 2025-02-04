class Piece:
    def __init__(self, colour: int, row :int, col:int):
        self.colour = colour # 1 for white, -1 for black
        self.symbol = ""
        self.hasMoved = False
        self.row = row
        self.col = col
    def safeAccess(self, row, col, board): #Make sure we are not 
        try:
            return board.board[row][col]
        except IndexError:
            return None
            
    def moves(self, board):
        moves = []
        possibleMoves = self.capturables(board)
        for move in possibleMoves:
            row, col = move
            square = self.safeAccess(row, col, board)
            if square is None:
                moves.append(move)
            elif isinstance(square, King):
                pass
            elif square.colour != self.colour:
                moves.append(move)
        return moves
    
    def __repr__(self):
        return self.symbol.upper() if self.colour == 1 else self.symbol.lower()
    

class Pawn(Piece):
    def __init__(self, colour: int, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "P"
        self.firstmove = False  
        self.potentialenPassant = False
        
        #used to make sure king is not walking through checks
    def capturables(self, board): #Returns a theoretical squares a pawn could capture
        possibleCaptures = [
            [self.row + self.colour, self.col + 1],
            [self.row + self.colour, self.col - 1]
        ]
        
        validCaptures = [
            [r, c]
            for r, c in possibleCaptures
                if 0 <= r < 8 and 0 <= c < 8
        ]
        return validCaptures
            
    def normalCaptures(self, board): #Returns actual squares a pawn could capture
        captures = [
            [self.row + self.colour, self.col + 1],
            [self.row + self.colour, self.col - 1]
        ]
        
        validCaptures = []
        for capture in captures:
            row,col = capture
            piece = self.safeAccess(row, col, board)
            if piece is None:
                continue
            if piece.colour != self.colour:
                validCaptures.append(capture)
        return validCaptures
        
    def enPassantCaptures(self, board): #Returns actual squares a pawn could capture
        enPassant = [
            [self.row,self.col + 1],
            [self.row,self.col - 1]
        ]
        
        validEnpassant=[]
        
        for capture in enPassant:
            row,col = capture
            piece = self.safeAccess(row, col, board)
            if piece is None:
                continue
            if piece.colour != self.colour and piece.potentialenPassant == True:
                validEnpassant.append(capture) #MUST FIX THIS, RIGHT NOW IT CAN JUST CAPTURE TO THE RIGHT
        return validEnpassant#MAKE WORK SO CAPTURE GOES RIGHT OR LEFT AND UP LIKE A NORMAL CAPTURE
    
    def forwardMoves(self, board):
        if self.firstmove:
            forwardMove = [
                [self.row + (1 * self.colour), self.col],
                [self.row + (2 * self.colour) ,self.col]
            ]
        else:
            forwardMove = [[self.row + (1 * self.colour), self.col]]
            
        validForward = []
        
        for move in forwardMove:
            row,col = move
            if row == 8 or row == -1:
                break;
            if board.board[row][col] != None:
                break;
            else:
                validForward.append(move)
        return validForward
    
    #determine what square the pawn can move too and return as a list
    #make this return possible moves
    def moves(self, board):
        moves = []
        
        validForward = self.forwardMoves(board)
        validCaptures = self.normalCaptures(board)
        validEnpassant = self.enPassantCaptures(board)
        
        moves.extend(validForward)
        moves.extend(validCaptures)
        moves.extend(validEnpassant)
        return moves
        
class King(Piece):
    def __init__(self, colour: str, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "K"
        self.inCheck = False
        self.firstMove = True
        self.castleKingside = False
        self.castleQueenside = False 
        # keep track of this through game manager
        
    def capturables(self, board):
        row, col = self.row, self.col
        capturables = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                if 0 <= row + dr < 8 and 0 <= col + dc < 8:
                    capturables.append([row + dr, col + dc])
        #print(capturables)
        return capturables
        
       
    def moves(self, board):
        possibleMoves = []

        possibleMoves = self.capturables(board)
        
        validMoves = []
        for move in possibleMoves:
            row,col = move
            piece = self.safeAccess(row, col, board)
            if piece is None:
                validMoves.append(move)
            elif piece.colour != self.colour:
                validMoves.append(move)
        
        enemyCapturables = board.getAllEnemyCapturableSquare(self.colour, board)
        #add check to make sure enemycapturables isnt empty or NoneType
        #enemyCapturables = [i for sublist in enemyCapturables for i in sublist]
        
        
        moves = []
        #moves = [x for x in validMoves if x not in enemyCapturables]
        moves = [move for move in validMoves if move not in enemyCapturables]
        
        #moves = [x for x in validMoves if x not in enemyCapturables]
        #print(moves)
        return moves

class Knight(Piece):
    def __init__(self, colour: int, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "N"
        self.firstmove = True
    
    def capturables(self, board):
        capturables = []
        current_row = self.row
        current_col = self.col
        knight_moves = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),  # Moves with 2-row jump
            (-1, -2), (-1, 2), (1, -2), (1, 2)   # Moves with 2-column jump
        ]

        for dr, dc in knight_moves:
            new_row = current_row + dr
            new_col = current_col + dc

            # Check if the move stays within board limits
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                capturables.append([new_row, new_col])

        return capturables # returns moves in bounds
    
        
class Rook(Piece):
    def __init__(self, colour: int, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "R"
        self.firstmove = True
        
    def capturables(self, board):
        row, col = self.row, self.col
        capturables = []
        
        # Directions for the rook: (row change, col change)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
        
        for dr, dc in directions:
            currentRow, currentCol = row, col
            foundKing = False
            while True:
                currentRow += dr
                currentCol += dc
                
                # Check boundaries
                if currentRow < 0 or currentRow > 7 or currentCol < 0 or currentCol > 7:
                    break  # Stop if out of bounds
                
                square = self.safeAccess(currentRow, currentCol, board)
                
                if(foundKing):
                    capturables.append([currentRow, currentCol])
                    break
                
                if square is None:  # Empty square, add to capturables
                    capturables.append([currentRow, currentCol])
                    #print(isinstance(square, King))
                elif isinstance(square, King):
                    #print("found king")
                    capturables.append([currentRow, currentCol])
                    foundKing= True
                else: #found a different piece
                    capturables.append([currentRow, currentCol])
                    break  # Stop in this direction
            
        return capturables
        
        
        
class Bishop(Piece):
    def __init__(self, colour: int, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "B"
        self.firstmove = True
        
    def capturables(self, board):
        row, col = self.row, self.col
        capturables = []
        
        
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # diagonals
        foundKing = False
        
        for dr, dc in directions:
            foundKing = False
            currentRow, currentCol = row, col
            while True:
                currentRow += dr
                currentCol += dc
                
                # Check boundaries
                if currentRow < 0 or currentRow > 7 or currentCol < 0 or currentCol > 7:
                    break  # Stop if out of bounds
                
                square = self.safeAccess(currentRow, currentCol, board)
                
                if(foundKing):
                    capturables.append([currentRow, currentCol])
                    break
                
                if square is None:  # Empty square, add to capturables
                    capturables.append([currentRow, currentCol])
                    #print(isinstance(square, King))
                elif isinstance(square, King):
                    capturables.append([currentRow, currentCol])
                    foundKing= True
                else: #found a different piece
                    capturables.append([currentRow, currentCol])
                    break  # Stop in this direction
                    
        return capturables
    
        
class Queen(Piece):
    def __init__(self, colour: int, row: int ,col: int):
        super().__init__(colour,row,col)
        self.symbol = "Q"
        self.firstmove = True
        
    def capturables(self, board):
        row, col = self.row, self.col
        capturables = []
        
        #DIAGONALS
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # diagonals
        
        
        for dr, dc in directions:
            foundKing = False
            currentRow, currentCol = row, col
            while True:
                currentRow += dr
                currentCol += dc
                
                # Check boundaries
                if currentRow < 0 or currentRow > 7 or currentCol < 0 or currentCol > 7:
                    break  # Stop if out of bounds
                
                square = self.safeAccess(currentRow, currentCol, board)
                
                if(foundKing):
                    capturables.append([currentRow, currentCol])
                    break
                
                if square is None:  # Empty square, add to capturables
                    capturables.append([currentRow, currentCol])
                    #print(isinstance(square, King))
                elif isinstance(square, King):
                    #print("found king")
                    capturables.append([currentRow, currentCol])
                    foundKing= True
                else: #found a different piece
                    capturables.append([currentRow, currentCol])
                    break  # Stop in this direction
        
        
        ##HORZ VERT
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
        
        for dr, dc in directions:
            currentRow, currentCol = row, col
            foundKing = False
            while True:
                currentRow += dr
                currentCol += dc
                
                # Check boundaries
                if currentRow < 0 or currentRow > 7 or currentCol < 0 or currentCol > 7:
                    break  # Stop if out of bounds
                
                square = self.safeAccess(currentRow, currentCol, board)
                
                if(foundKing):
                    capturables.append([currentRow, currentCol])
                    break
                
                if square is None:  # Empty square, add to capturables
                    capturables.append([currentRow, currentCol])
                    #print(isinstance(square, King))
                elif isinstance(square, King):
                    #print("found king")
                    capturables.append([currentRow, currentCol])
                    foundKing= True
                else: #found a different piece
                    capturables.append([currentRow, currentCol])
                    break  # Stop in this direction
                     
        return capturables
    
        