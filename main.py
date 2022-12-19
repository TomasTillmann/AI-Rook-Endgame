from move_functions import *

def minimax(position: tuple, depth: int, alpha: float, beta: float, white: bool):
    """ 
    funguje jako klasicky minimax
    vrati dynamicke hodnoceni pozice (position) jako float
    """
    # pokud uz jsem v dane hloubce nebo nastal konec partie, ukoncim pruchod do hloubky v danem uzlu a vratim staticke ohodnoceni pozice
    if depth == 0 or game_over(position, white):
        return (static_evaluation(position, white))

    # v kazde hladine se strida bily a cerny (maximizing player / minimizing player)
    # bily preferuje vyssi ohodnoceni, cerny nizsi
    if white:
        max_evaluation = float("-inf")                                      # pri prvnim pruchodu uzlem nastaveno na nejhorsi mozne hodnoceni bileho - technicky trik
        child_positions = generate_child_positions(position, True)          # vygeneruje pozice, ktere mohou nastat z vychozi pozice bilym na tahu
        for child in child_positions:                                       # postupne prochazi tyto pozice a rekurzivne na ne vola minimax
            evaluation = minimax(child, depth - 1, alpha, beta, False)      # rekurzivni volani do hloubky -1 a s cernym na tahu (False)
            max_evaluation = max(max_evaluation, evaluation)                # dosud maximalni dynamicke ohodnoceni vychozi pozice, pri prvnim pruchodu se vzdy nastavi na evaluation prvni child pozice
            # alfa beta prorezavani
            # je zbytecne dale prohledavat pozice, pokud uz mel bily nekde jinde lepsi moznost, ktere se v danem zanoreni jiste neda dosahnout
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_evaluation

    # analogicky, akorat je zde cerny na tahu
    else:
        min_evaluation = float("inf")                                       # nejhorsi mozne hodnoceni pro cerneho
        child_positions = generate_child_positions(position, False)
        for child in child_positions:
            evaluation = minimax(child, depth - 1, alpha, beta, True)       # vola minimax opet do hloubky -1 ale tentokrat s bilym na tahu (true)
            min_evaluation = min(min_evaluation, evaluation)
            # alfa beta prorezavani
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation

# set vsech pozic, ktere uz byli zahrany
# je potreba, aby do nekonecna neopakoval stejne tahy
PLAYED_POSITIONS = set()
def best_positions(position: tuple):
    """
    z vychozi pozice vrati nejlepsi pozici (tuple) pro bileho,
    ktera jeste nebyla zahrana, vyuzitim minimaxu
    """
    global PLAYED_POSITIONS
    white = True
    child_positions = generate_child_positions(position, white)
    best_positions = {}

    # podiva se, jestli nejde dat z vychozi pozice tri tahovy mat a pak jestli nejde dat petitahovy mat
    depths = [4,6]
    for depth in depths:
        for child in child_positions:
            evaluation = minimax(child, depth - 1, float("-inf"), float("inf"), not white)
            if evaluation == float("inf"): 
                PLAYED_POSITIONS.add(child)
                #print(child)
                return child

    # pokud nelze, tak zavola minimax na vsechny pozice, ktere mohou nastat bilym na tahu
    depth = 9
    for child in child_positions:
        evaluation = minimax(child, depth - 1, float("-inf"), float("inf"), not white)
        best_positions[child] = evaluation                                  # hodnoceni konkretni pozice (child) si ukladam do dict 
    
    # pozice z dictu setridim v klesajicim poradi a ulozim do list ve kterem jsou ulozeny dvojice (tuples), 
    # kde na prvni pozici je child pozice a na druhe jeji staticka evaluace
    sorted_best_positions = sorted(best_positions.items(), key = lambda item: item[1], reverse = True)
    #for i in sorted_best_positions: print(i)
    # prochazim sorted_best_positions a hledam pozici, ktera jeste nebyla zahrana
    i = 0
    while sorted_best_positions[0 + i][0] in PLAYED_POSITIONS:
        i += 1
    PLAYED_POSITIONS.add(sorted_best_positions[0 + i][0])                   # jakmile takovou najdu, pridam ji do PLAYED_POSITIONS
    return sorted_best_positions[0 + i][0]                                  # vratim tuto pozici, jedna se o nejlepsi pozici kterou muze byli z vychozi pozice zahrat (podle minimaxu)

