import os
import re
from possible_hands import possible_hands
from player_stats import *

### NECESSARY FIXES ###

### 1. (No clean fix available) => Heavy reliance on text cues in hand history, unusual usernames could cause problems.
###   => Consider adding a system where I use findall to retrive the last instance of the target word (e.g. fold).
###   => This still doesn't fix the problem that a username could cause problems... e.g. "Never folds calls." Current parser would determine that Never has folded.  
### 2. Use current seating to determine how many players are still in hand (i.e. multiway?) just don't mess with it before position assignment                                                 

regexes = {'hand_info': '\s+[-]\s+', 'hole_cards': '[\[].+[\]]'}
current_hand = {
                'id' : None,
                'tournament' : None,
                'mode' : None,
                'handed': None,
                'blinds' : None,
                'time' : None,
                'on_bb' : None,
                'hero_cards' : None,
                'hand_phase' : None,
                'away_players' : [],
                'aggressor' : None, 
                'players_in_hand' : set()
            }

possible_hands = possible_hands()

current_seating = {} # hand id to seats
current_positions = {} # player to int position

all_files = os.listdir('SteinwayThor/')


def read_files(files):
    ''' Get a list of all the files to be parsed then collect data from them '''
    
    for file in files:
        parse_file(os.path.abspath('SteinwayThor/' + file))
        #get_player_stats()
        #exit()

def parse_file(file):
    with open('HUD//test.txt', 'wt') as fw:
        with open(file, 'rt') as f:
            for line in f:
                if re.match('Game Hand #', line):
                    tournament_header(line)
                    find_handed(f.readline())
                elif re.match('Hand #', line):
                    cash_header(line)
                    find_handed(f.readline())
                elif re.match('Seat ', line):
                    update_seating(line)
                elif re.search('posts the small blind', line):
                    update_positions(line, 'sb')
                elif re.search('posts the big blind', line):
                    update_positions(line, 'bb')
                elif re.search('waits for big blind', line) or re.search('sits out', line):
                    remove_away(line)
                elif re.search('HOLE CARDS', line):
                    assign_positions()
                elif re.match('Dealt to SteinwayThor', line):
                    hero_hole_cards(line)
                elif re.search('folds$', line):
                    player_acts(line, 'folds')
                             
                
def tournament_header(line):
    ''' Format: ID, Tournament ID, Mode, Blinds, Time (xxxx-xx-xx hr:min:sec UTC)'''

    header_info = re.split(regexes['hand_info'], line[:-1]) # remove extraneous /n
    current_hand['id'] = header_info[0][11:].strip()
    current_hand['tournament'] = header_info[1][12:].strip()
    current_hand['mode'] = header_info[2].strip()
    blinds_and_time = header_info[3].split('-')
    current_hand['blinds'] = blinds_and_time[0].strip()
    current_hand['time'] = blinds_and_time[1].strip()

    current_seating[current_hand['id']] = []

def cash_header(line):

    header_info = re.split(regexes['hand_info'], line[:-1]) # remove extraneous /n
    current_hand['id'] = header_info[0][6:].strip()
    current_hand['tournament'] = None
    current_hand['mode'] = header_info[1].strip()
    current_hand['blinds'] = header_info[2].strip()
    current_hand['time'] = header_info[3].strip()   

    current_seating[current_hand['id']] = []
    
    
def update_seating(line):
    name_and_stack = re.split(" ", line[8:]) # assumes no more than 9 handed
    
    # print(name_and_stack)
    if len(name_and_stack) == 2:
        current_seating[current_hand['id']].append(name_and_stack[0])
    else:
        name = name_and_stack[0]
        if re.search("will be allowed to play after the button", line) or re.search("is sitting out", line):
            for word in name_and_stack[1:]:
                if word[0] == '(' or word == 'will':
                    break
                name = name + " " + word
            # adjust_player(name, current_hand['hand_phase'], 'joins')
            current_hand['away_players'].append(name)
            current_seating[current_hand['id']].append(name)
            return
        for word in name_and_stack[1:-1]:
            name = name + " " + word
        current_seating[current_hand['id']].append(name)

def update_positions(line, pos):
    words = re.split(" ", line)
    end_of_name = words.index('posts')
    player = words[0]
    for word in words[1:end_of_name]:
        player = player + " " + word
    # player_pos = current_seating[current_hand['id']].index(player)
    # table_size = len(current_seating[current_hand['id']])
    if pos == 'sb':
        current_positions[player] = 1
    elif pos == 'bb':
        current_positions[player] = 2
        current_hand['on_bb'] = player

def assign_positions():
    # Update this when I have the chance -- just have numbers and then deal with position names somewhere else
    # for x in range(0, table_size):
    bb_pos = current_seating[current_hand['id']].index(current_hand['on_bb'])
    counter = 3
    table_size = len(current_seating[current_hand['id']])
    for x in range(1, table_size - 1):
        player = current_seating[current_hand['id']][(x + bb_pos) % table_size]
        if player in current_hand['away_players']:
            continue
        current_positions[player] = counter
        counter += 1

    current_hand['hand_phase'] = 'pre-flop'
    # print(current_seating[current_hand['id']])
    #for player in current_seating[current_hand['id']]:
    #    adjust_player(player, current_hand['hand_phase'], 'joins')

def find_handed(line):
    words = re.split(" ", line)
    for word in words:
        if word[0].isnumeric():
            current_hand['handed'] = word
    # print(current_hand)
    current_positions.clear()
    current_hand['away_players'].clear()

def remove_away(line):
    # sits or waits
    words = re.split(" ", line)
    if 'sits' in words:
        end_of_name = words.index('sits')
    elif 'waits' in words:
        end_of_name = words.index('waits')
    
    away_player = words[0]
    for word in words[1:end_of_name]:
        away_player = away_player + " " + word

    current_hand['away_players'].append(away_player)

def hero_hole_cards(line):
    hole_cards = re.findall(regexes['hole_cards'], line)[0][1:-1]
    two_cards = re.split(" ", hole_cards)
    if two_cards[0][-1] == two_cards[1][-1]:
        combo_one = two_cards[0][0] + two_cards[1][0] + 's'
        if combo_one in possible_hands:
            hand = combo_one
        else:
            hand = two_cards[1][0] + two_cards[0][0] + 's'
    else:
        combo_one = two_cards[0][0] + two_cards[1][0] + 'o'
        if combo_one in possible_hands:
            hand = combo_one
        else:
            hand = two_cards[1][0] + two_cards[0][0] + 'o'
    if hand[0] == hand[1]:
        hand = hand[:-1]
    current_hand['hero_cards'] = hand
    # print(current_hand)

def player_acts(line, act):
    
    words = re.split(" ", line)
    end_of_name = words.index(act + '\n')
    player = words[0]

    for word in words[1:end_of_name]:
        player = player + " " + word

    
         
    if act == 'bets':
        current_hand['aggressor'] = player

    phase = current_hand['hand_phase']
    if phase == 'pre-flop':
        if act == 'bets':
            current_hand['hand_phase'] == 'facing open'    
    elif phase == 'facing open':
        if act == 'bets':
            current_hand['hand_phase'] == 'facing 3-bet'
    elif phase == 'facing 3-bet':
        if act == 'bets':
            current_hand['hand_phase'] = 'facing 4-bet'
    elif phase == 'facing 3-bet and callers':
        if act == 'calls':
            pass
        elif act == 'folds':
            pass
        elif act == 'bets':
            current_hand['hand_phase'] = 'facing 4-bet'
    elif phase == 'facing 4-bet':
        if act == 'calls':
            current_hand['hand_phase'] = 'facing 4-bet and callers'
        elif act == 'folds':
            pass
        elif act == 'bets':
            current_hand['hand_phase'] = 'facing 5-bet'
    elif phase == 'facing 4-bet and callers':
        if act == 'calls':
            pass
        elif act == 'folds':
            pass
        elif act == 'bets':
            current_hand['hand_phase'] = 'facing 5-bet'
    elif phase == 'facing 5-bet':
        if act == 'calls':
            pass
        elif act == 'folds':
            pass
        elif act == 'bets':
            current_hand['hand_phase'] = 'more than 5-bet'
    elif phase == 'more than 5-bet':
        pass

    if (act == 'call' or act == 'bets') and player not in current_hand['players_in_hand']:
        current_hand['players_in_hand'].add(player)
        player_joins(player, current_positions[player])

    if current_positions[player] > current_positions[current_hand['aggressor']]:
        in_position = True
    else:
        in_position = False

    adjust_player(player, phase, act, in_position, multiway)
if __name__ == "__main__":
    read_files(all_files)
    get_player_stats()
# print(current_seating[current_hand['id']]) # Currently I'm double printing because the seats are given at the end again with action summary