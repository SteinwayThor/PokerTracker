'''Possible hole cards in 2-card holdem'''

def possible_hands():
    return set((
        '22', '33', '44', '55', '66', '77', '88', '99', 'TT', 'JJ', 'QQ', 'KK', 'AA',
        'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
        'AKo', 'AQo', 'AJo', 'ATo', 'A9o', 'A8o', 'A7o', 'A6o', 'A5o', 'A4o', 'A3o', 'A2o',
        'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
        'KQo', 'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o', 'K5o', 'K4o', 'K3o', 'K2o',
        'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s',
        'QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o', 'Q6o', 'Q5o', 'Q4o', 'Q3o', 'Q2o',
        'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s',
        'JTo', 'J9o', 'J8o', 'J7o', 'J6o', 'J5o', 'J4o', 'J3o', 'J2o',
        'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s',
        'T9o', 'T8o', 'T7o', 'T6o', 'T5o', 'T4o', 'T3o', 'T2o',
        '98s', '97s', '96s', '95s', '94s', '93s', '92s',
        '98o', '97o', '96o', '95o', '94o', '93o', '92o',
        '87s', '86s', '85s', '84s', '83s', '82s',
        '87o', '86o', '85o', '84o', '83o', '82o',
        '76s', '75s', '74s', '73s', '72s',
        '76o', '75o', '74o', '73o', '72o',
        '65s', '64s', '63s', '62s',
        '65o', '64o', '63o', '62o',
        '54s', '53s', '52s',
        '54o', '53o', '52o',
        '43s', '42s',
        '43o', '42o',
        '32s',
        '32o'
    ))