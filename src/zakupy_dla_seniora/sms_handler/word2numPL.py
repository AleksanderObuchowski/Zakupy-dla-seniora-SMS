# Made based on num2words for Polish
# https://github.com/savoirfairelinux/num2words/blob/master/num2words/lang_PL.py


FRACTIONS = {
    0.25: ("ćwierć", "ćwiartka", "ćwiartkę", "ćwiartki"),
    0.5: ("pół", 'połówka', "połówkę", "połówki"),
    1.5: ("półtora", "półtorej"),
}

ONES = {
    1: ('jeden', 'jedną', 'raz'),
    2: ('dwa', 'dwoje', 'dwie', 'dwójkę', 'dwóch'),
    3: ('trzy', 'troje', 'trójka'),
    4: ('cztery',),
    5: ('pięć',),
    6: ('sześć',),
    7: ('siedem',),
    8: ('osiem',),
    9: ('dziewięć',),
}

TENS = {
    0: ('dziesięć',),
    1: ('jedenaście',),
    2: ('dwanaście',),
    3: ('trzynaście',),
    4: ('czternaście',),
    5: ('piętnaście',),
    6: ('szesnaście',),
    7: ('siedemnaście',),
    8: ('osiemnaście',),
    9: ('dziewiętnaście',),
}

TWENTIES = {
    2: ('dwadzieścia',),
    3: ('trzydzieści',),
    4: ('czterdzieści',),
    5: ('pięćdziesiąt',),
    6: ('sześćdziesiąt',),
    7: ('siedemdziesiąt',),
    8: ('osiemdziesiąt',),
    9: ('dziewięćdzisiąt',),
}

HUNDREDS = {
    1: ('sto',),
    2: ('dwieście',),
    3: ('trzysta',),
    4: ('czterysta',),
    5: ('pięćset',),
    6: ('sześćset',),
    7: ('siedemset',),
    8: ('osiemset',),
    9: ('dziewięćset',),
}


def words2num(num):
    result = 0
    num = num.lower()
    for word in num.split():
        for key in FRACTIONS.keys():
            if word in FRACTIONS[key]:
                result += key
        for key in ONES.keys():
            if word in ONES[key]:
                result += key
        for key in TENS.keys():
            if word in TENS[key]:
                result += 10
                result += key % 10
        for key in TWENTIES.keys():
            if word in TWENTIES[key]:
                result += key * 10
        for key in ONES.keys():
            if word in HUNDREDS[key]:
                result += key * 100
    return result
