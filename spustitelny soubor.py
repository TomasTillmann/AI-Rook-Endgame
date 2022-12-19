from main import *
from move_functions import *

def print_position(position):
    """
    vytiske pozici do konzole
    """
    chessboard = [["."]*8 for x in range(8)]
    chessboard[position[0][0]][position[0][1]] = "k"
    chessboard[position[1][0]][position[1][1]] = "K"
    chessboard[position[2][0]][position[2][1]] = "V"
    for row in chessboard:
        print(*row)
    print()

def is_valid_black_king_move(position, inp):
    """
    testuje vstup, zda dany tah cernym kralem je legalni
    vrati bool hodnotu
    """
    # overeni vstupu je v try bloku, protoze uzivatel muze zadat uplne libovolny vstup. Zabrani se tak spadnuti programu
    try:
        if len(inp) != 2: return False
        move = (int(inp[0]), int(inp[1]))
        black_king_moves = generate_black_king_moves(position)
        if move in black_king_moves:
            return True
        else: 
            return False
    except ValueError:
        return False

def is_valid_move(inp):
    """
    testuje zda zadany vstup je legalni tah
    vrati bool hodnotu
    """
    # overeni vstupu je v try bloku, protoze uzivatel muze zadat uplne libovolny vstup. Zabrani se tak spadnuti programu
    try:
        if len(inp) != 2: return False
        if 0 <= int(inp[0]) <= 7 and 0 <= int(inp[1]) <= 7:
            return True
        else:
            return False
    except ValueError:
        return False

def is_valid_position(position):
    """
    Kontroluje, zda dana pozice je legalni, pokud je bily na tahu
    """
    b_king, w_king, rook = position[0], position[1], position[2]
    if  b_king == w_king or b_king == rook or w_king == rook:                       # kontroluje zda nejsou nejake dve figurky na stejnych polickach
        return False
    if (abs(w_king[0] - b_king[0]) <= 1 and abs(w_king[1] - b_king[1]) <= 1):       # zda jsou kralove u sebe, tak se jedna o nelegalni pozici
        return False
    rook_span = generate_rook_span(position)
    if b_king in rook_span:                                                         # kontroluje zda cerny kral neni v ohrozeni veze, protoze kdyby byl v ohrozeni veze, tak ho bila vez muze sebrat
        return False
    return True  

def is_valid_yes_no(inp):
    """
    kontroluje, zda se jedna o validni odpoved uzivatele na otazku,
    zda chce hrat znovu
    """
    # overeni vstupu je v try bloku, protoze uzivatel muze zadat uplne libovolny vstup. Zabrani se tak spadnuti programu
    try:
        if len(inp) != 1: return False
        if inp[0] != 'Y' and inp[0] != 'N': return False
        return True
    except ValueError:
        return False

def print_possible_moves(position):
    """
    vytiskne tahy, ktere cerny muze v dane pozici
    zahrat
    """
    moves = generate_black_king_moves(position)
    print("possible inputs: ")
    for move in moves:
        print(move[0], move[1], end="   ")
    print()

def play_move(position):
    """
    nacita a overuje vstup cerneho 
    vrati legalni pozici po tahu cerneho krale
    """
    inp = input().split()
    while not is_valid_black_king_move(position, inp):
        print("Impossible move or wrong format of the input. Please, try again. ")
        print_possible_moves(position)
        inp = input().split()

    position = list(position)
    move = (int(inp[0]), int(inp[1]))
    position = (move, position[1], position[2])
    return tuple(position)

def start_playing(position):
    """
    Interaktivne hraje danou pozici s uzivatelem
    """
    print("starting position: ")
    print_position(position)
    position = best_positions(position)
    print("engine's move:")
    print_position(position)
    while not game_over(position, False):
        print("make a move: ")
        position = play_move(position)
        position = best_positions(position)
        print()
        print("engine's move:")
        print_position(position)

def setup_position():
    """
    Prijima vstup od uzivatele, testuje ho, a nasledne
    vrati legalni pozici
    """
    pieces = ["black king","white king", "white rook"]
    position = [(),(),()]
    i = 0
    for piece in pieces:
        print(f"Enter {piece}'s position: ", end = " ")
        inp = input().split()
        while not is_valid_move(inp):
            print("Please, try again. Possible input example:")
            print("4 7")
            inp = input().split()
        position[i] = (int(inp[0]), int(inp[1]))
        i += 1
    return tuple(position)     

def start_program():
    """
    Interaktivne komunikuje s uzivatelem
    a hraje s nim danou koncovku
    """
    print("Setup the starting position ")
    position = setup_position()
    while not is_valid_position(position):
        print_position((position[0],position[1],position[2]))
        print("This is not a valid input position.")
        print("Example of possible input:")
        print("1 2")
        print("3 3")
        print("6 7")
        print("This input corresponds to this position:")
        print_position(((1,2),(3,3),(6,7)))
        print("Please, try again: ")
        position = setup_position()
        print()
    start_playing(position)


start_program()
do_play = True
while do_play:
    print("CHECKMATE! Good game.")
    print("Do you want to play another game?")
    print("Y - yes, N - no")

    inp = input().split()
    while not is_valid_yes_no(inp):
        print("Please, try again.")
        print("Y - yes, N - no")
        inp = input().split()
    if inp[0] == 'Y':
        print("Let's play!")
        print()
        print()
        PLAYED_POSITIONS.clear()
        start_program()
    else:
        print("Goodbye!")
        do_play = False
    
        
