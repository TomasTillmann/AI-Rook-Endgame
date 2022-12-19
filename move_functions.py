# mapa hodnot policek na sachovnici
# na kraji, napriklad na poli (7,3) je hodnota 4, protoze jelikoz je cerny kral na kraji, tak se jedna o dobrou pozici pro bileho,
# naopak pokud je cerny kral uprostred, napriklad na poli (3,3) vraci -4, jelikoz se jedna o spatnou pozici pro bileho ale dobrou pro cerneho -> 
# ve stredu sachovnice se tezko dava mat 
EVAL_TABLE = ((4,4,4,4,4,4,4,4),(4,2,2,2,2,2,2,4),(4,2,-2,-2,-2,-2,2,4),(4,2,-2,-4,-4,-2,2,4),(4,2,-2,-4,-4,-2,2,4),(4,2,-2,-2,-2,-2,2,4),(4,2,2,2,2,2,2,4),(4,4,4,4,4,4,4,4))

# pointa nasledujicich globalnich promennych je urychleni programu - pokud uz jsem v nasledujici pozici vygeneroval to co zrovna je treba, neni duvod to delat opakovane 

# dict pozic (key) a statickych evaluaci (value) pozic, ktere uz byli ohodnoceny funkci static_evaluation(position)
STATIC_EVALUATIONS = {}
# dict pozic (key) a tahu cerneho krale (value), ktere uz byli vygenerovany funkci generate_black_king_moves(position)
BLACK_KING_MOVES = {}
# dict pozic (key) a moznych pozic (value), ktere uz byli vygenerovany funkci generate_white_king_positions(position)
WHITE_KING_POSITIONS = {}
# to stejne jako white_king_positions, ale pro cerneho, vygenerovane funkci generate_black_king_positions(position)
BLACK_KING_POSITIONS = {}
# dict pozic (key) a pozic (value), kde tahla bila vez, vygenerovane funkci generate_rook_positions(position)
ROOK_POSITIONS = {}
#dict pozic (key) a vsech rook_span ( viz funkce generate_rook_span(position)) (value), vygenerovany funkci generate_rook_span(position)
ROOK_SPANS = {}
# dict pozic (key) a  moznych pozic provedene po jednom tahu (value), vygenerovane funkci generate_child_positions(position, white)
CHILD_POSITIONS = {}


def game_over(position: tuple, white: bool):
    """
    vrati bool hodnotu
    True - konec partie, False - neni konec partie
    """

    if position[0] == position[2]: return True                             # cerny kral vzal vezku, bily uz nemuze dat mat. To je v podstate konec partie. Tahani holymi krali nedava smysl
    if white: return False                                                 # pokud je bily na tahu, nemuze nastat konec partie. Bily vzdy muze provest nejaky tah
    else:
        if len(generate_black_king_moves(position)) == 0: return True      #cerny nema zadne tahy, takze nastal bud mat nebo pat - to je konec partie
        else: return False

def static_evaluation(position: tuple, white: bool):
    """
    vrati staticke vyhodnoceni pozice jako float
    """

    global EVAL_TABLE   
    global STATIC_EVALUATIONS
    if position in STATIC_EVALUATIONS:
        return STATIC_EVALUATIONS[position]

    rook_span = generate_rook_span(position)    
    bk_moves = generate_black_king_moves(position)
    bk_moves_count = len(bk_moves)
    evaluation = -100                                                                           # nemuze byt float("-inf") ale zaroven musi byt "hodne mala" viz dale
    if not white:
        if bk_moves_count == 0 and position[0] in rook_span: evaluation =  float("inf")         # nastal mat
        if (bk_moves_count == 0 and position[0] not in rook_span): evaluation = float("-inf")   # nastal pat

        # kontroluju zda nevisi vez
        # pozice kde v dalsim tahu cerny muze vzit zadarmo vez nejsou pro bileho vitany
        if (abs(position[0][0] - position[2][0]) <= 1 and abs(position[0][1] - position[2][1]) <= 1) and (abs(position[1][0] - position[2][0]) > 1 or abs(position[1][1] - position[2][1]) > 1):
                evaluation =  float("-inf")

    if evaluation != float("inf") and evaluation != float("-inf"):                              # nyni je zrejme proc evaluation nemuze byt -inf, jedna se ciste o technicky detail
        try:
            s = 0
            # poscitam pres vsechny hodnoty z EVAL_TABLE kam cerny kral muze jit
            for move in bk_moves:
                s += EVAL_TABLE[move[0]][move[1]]
            evaluation = s / bk_moves_count                                                                         # vydelim poctem moznych tahu, zajima me totiz pomer na jak "dobre policka muze v dalsim tahu jit" ku celkovemu poctu tahu
            king_distance = 1 / (abs(position[0][0] - position[1][0]) + abs(position[0][1] - position[1][1]))       # 1 ku mannhattan distance pozic kralu - cim bliz je bily kral cernemu, tim je to lepsi pozice
            evaluation = evaluation + king_distance
        except ZeroDivisionError:
            # pokud bych delil nulou, tak vratim hodnotu policka kde prave cerny kral stoji
            evaluation = EVAL_TABLE[position[0][0]][position[0][1]]

    STATIC_EVALUATIONS[position] = evaluation
    return evaluation

def generate_black_king_moves(position: tuple):
    """
    vygeneruje tahy cerneho krale z dane pozice a vrati jako list
    """
    global BLACK_KING_MOVES
    if position in BLACK_KING_MOVES:
        return BLACK_KING_MOVES[position]

    rook_span = generate_rook_span(position)
    b_king, w_king = position[0], position[1]
    child_moves = []
    king_moves = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    king_move = [-1,-1]

    # zkousim vsechny mozne tahy krale a testuju, zda jsou legalni
    for move in king_moves:
        king_move[0] = b_king[0] + move[0]
        king_move[1] = b_king[1] + move[1]

        king_move = tuple(king_move)
        # je kral na sachovnici, aspon jedno policko vzdalen od bileho krale a neni v ohrozeni veze?
        if 0 <= king_move[0] <= 7 and 0 <= king_move[1] <= 7 and (abs(king_move[0] - w_king[0]) > 1 or abs(king_move[1] - w_king[1]) > 1) and king_move not in rook_span:
            child_moves.append(king_move)
        king_move = list(king_move)

    BLACK_KING_MOVES[position] = child_moves
    return child_moves

def generate_black_king_positions(position: tuple):
    """
    vygeneruje pozice z dane pozice kde cerny pohnul kralem a vrati jako dict
    """
    global BLACK_KING_POSITIONS
    if position in BLACK_KING_POSITIONS:
        return BLACK_KING_POSITIONS[position]

    rook_span = generate_rook_span(position)
    b_king, w_king = position[0], position[1]
    child_positions = {}
    king_moves = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    king_move = [-1,-1]

    # zkousim vsechny mozne tahy krale a testuju, zda jsou legalni
    for move in king_moves:
        king_move[0] = b_king[0] + move[0]
        king_move[1] = b_king[1] + move[1]

        king_move = tuple(king_move)
        # je kral na sachovnici, aspon jedno policko vzdalen od bileho krale a neni v ohrozeni veze?
        if 0 <= king_move[0] <= 7 and 0 <= king_move[1] <= 7 and (abs(king_move[0] - w_king[0]) > 1 or abs(king_move[1] - w_king[1]) > 1) and king_move not in rook_span:
            child_position = generate_position(position, king_move, 0)
            child_positions[child_position] = static_evaluation(child_position, True)
        king_move = list(king_move)

    BLACK_KING_POSITIONS[position] = child_positions
    return child_positions

def generate_white_king_positions(position: tuple):
    """
    vygeneruje pozice z dane pozice kde bily pohnul kralem a vrati jako dict
    """
    global WHITE_KING_POSITIONS
    if position in WHITE_KING_POSITIONS:
        return WHITE_KING_POSITIONS[position]

    b_king, w_king, rook = position[0], position[1], position[2]
    child_positions = {}
    king_moves = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    king_move = [-1,-1]

    for move in king_moves:
        king_move[0] = w_king[0] + move[0]
        king_move[1] = w_king[1] + move[1]

        # je kral na sachovnici a vzdalen aspon jedno policko od cerneho krale?    
        if 0 <= king_move[0] <= 7 and 0 <= king_move[1] <= 7 and (abs(king_move[0] - b_king[0]) > 1 or abs(king_move[1] - b_king[1]) > 1) and king_move != list(rook):
            child_position = generate_position(position, king_move, 1)
            child_positions[child_position] = static_evaluation(child_position, False)

    WHITE_KING_POSITIONS[position] = child_positions
    return child_positions

def generate_rook_positions(position: tuple):
    """
    vygeneruje pozice kde bily pohnul vezkou a vrati jako dict
    """
    global ROOK_POSITIONS
    if position in ROOK_POSITIONS:
        return ROOK_POSITIONS[position]

    b_king, w_king, rook = position[0], position[1], position[2]
    child_positions = {}
    coordinates, directions = [1,1,0,0], [1,-1,1,-1]
    # postupne generuje vsechny tahy ktera vez muze zahrat a nasledne kontroluje zda jsou legalni
    for i in range(4):
        rook_move = list(rook)
        c, d = coordinates[i], directions[i]
        for j in range(7):
            rook_move[c] = rook[c] + d
            # je vez na sachovnici, nevyhazuje krale a nepreskakuje krale?
            if 0 <= rook_move[0] <= 7 and 0 <= rook_move[1] <= 7 and rook_move != list(w_king) and rook_move != list(b_king):
                child_position = generate_position(position, rook_move, 2)
                child_positions[child_position] = static_evaluation(child_position, False)
            else: break
            d += directions[i]

    ROOK_POSITIONS[position] = child_positions
    return child_positions

def generate_rook_span(position: tuple):
    """
    vygeneruje vsechny policka kam muze vez jit a vrati jako set
    """
    if position in ROOK_SPANS:
        return ROOK_SPANS[position]
    else:
        rook, w_king = position[2], position[1]
        rook_span = set()
        coordinates, directions = [1,1,0,0], [1,-1,1,-1]
        for i in range(4):
            rook_move = list(rook)
            c, d = coordinates[i], directions[i]
            for j in range(7):
                rook_move[c] = rook[c] + d
                # je vez na sachovnici a nevyhazuje vlastniho krale?
                if  0 <= rook_move[0] <= 7 and 0 <= rook_move[1] <= 7 and rook_move != list(w_king):
                    rook_span.add(tuple(rook_move))
                else: break
                d += directions[i]

        ROOK_SPANS[position] = rook_span
        return rook_span

def generate_position(position: tuple, move: list, piece: int):
    """
    move - tah ktery provadime
    piece - figura kterou hybeme v dane pozici (position)
    vrati novou pozici po provedeni daneho tahu danou figurou jako tuple
    """
    child_position = list(position)
    child_position[piece] = tuple(move)
    return tuple(child_position)

def generate_child_positions(position: tuple, white: bool):
    """ 
    vygeneruje vsechny pozice ktere muze bily/cerny provest z dane pozice
    vrati jako list, kde jsou pozice serazene od nejlepsi po nejhorsi na zaklade jejich staticke evaluace
    """
    global CHILD_POSITIONS
    if (position, white) in CHILD_POSITIONS:
        return CHILD_POSITIONS[(position, white)]

    sorted_child_positions = []
    if white:
        white_king_child_positions = generate_white_king_positions(position)
        rook_child_positions = generate_rook_positions(position)
        white_king_child_positions.update(rook_child_positions)                                                         # vytvori dict vsech pozic (key) a statickych evaluaci (value) ktere muze bily provest
        child_positions = sorted(white_king_child_positions.items(), key = lambda item: item[1], reverse = True)        # vytvori list dvojic serazeny podle hodnoty v klesajicim poradi
        # v klesajicim poradi, protoze nejlepsi pozice pro bileho maji nejvysii statickou evaluaci
        for i in range(0, len(child_positions) // 2):                                                                   # neukladam vsechnz mozne pozice, staci zhruba prvni polovina nejlepsich tahu. Urychlim tak minimax
            sorted_child_positions.append(child_positions[i][0])                                                        # hodnota byla potreba pouze pro serazeni, nyni uz staci pouze nove vygenerovane hodnoty
    else:
        black_king_child_positions = generate_black_king_positions(position)                                            # vytvori dict vsech pozic (key) a statickych evaluaci (value) ktere muze cerny provest
        child_positions = sorted(black_king_child_positions.items(), key = lambda item: item[1])                        # setridi v rostoucim poradi
        for i in range(0, len(child_positions)):
            sorted_child_positions.append(child_positions[i][0])                                                        # ulozim do listu
    
    # pozice tridim, protoze to pak znacne urychli minimax, protoze staticka evaluace vlastne urcuje s jakou pravdepodovnosti se jedna o dobry tah, takze jelikoz
    # se minimax pak jako prvni diva na pozice, ktere jsou pravdepodovne dobre tak pak diky alfa beta prorezavani proreze mnohem vice pozic
    CHILD_POSITIONS[(position, white)] = sorted_child_positions
    return sorted_child_positions
    
    


    


        



