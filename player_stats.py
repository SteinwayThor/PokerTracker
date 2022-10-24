players = {} # player to statistics

def adjust_player(player, phase, action, in_position):
    #if phase == 'pre-flop' or phase == 'facing open' or phase == 'facing callers' or phase == :
        #if action == 'joins':
        #    if player not in players:
              #  players[player] = {}
              # players[player]['hands dealt'] = 0
              #  players[player]['hands played'] = 0
           # players[player]['hands dealt'] += 1
           # players[player]['hands played'] += 1
        # elif action == 'fold':
            # players[player]['hands played'] -= 1
    pass

def player_joins(player, position, act):
    # distinguish between raised and called here for VPIP/PFR stats
    if act == 'bets' or act == 'calls':
        if player not in players:
            players[player] = {}
            players[player]['hands dealt'] = {}
            players[player]['hands played'] = {}

        if position not in players[player]['hands played']:
            players[player]['hands played'][position] = 0
            players[player]['hands dealt'][position] = 0
        else:
            players[player]['hands played'][position] += 1
            players[player]['hands dealt'][position] += 1
       

def get_player_stats():
    calculate_stats()
    print(players)
    print(len(players))

def calculate_stats():
    for player in players:
        players[player]['VPIP'] = players[player]['hands played'] / players[player]['hands dealt']
    
# VPIP doesn't work yet because I don't check whether the fold was due to a 3bet