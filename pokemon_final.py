#!/usr/bin/env/python
#Written by Tyler Marbach and Emma Bishop
import pandas as pd

pokemon = pd.read_csv("pokemon.csv", index_col = [30])
poke_type = pokemon.rename(columns={'against_bug':'bug', 'against_dark':'dark', 'against_dragon':'dragon',
                                     'against_electric':'electric', 'against_fairy':'fairy', 'against_fight':'fight',
                                     'against_fire':'fire', 'against_flying':'flying', 'against_ghost':'ghost',
                                     'against_grass':'grass', 'against_ground':'ground', 'against_ice':'ice',
                                     'against_normal':'normal', 'against_poison':'poison', 'against_psychic':'psychic',
                                     'against_rock':'rock', 'against_steel':'steel', 'against_water':'water'})

def main():

    names = poke_names(poke_type)
    party = party_maker(names)
    wild = wild_poke(names)
    powers = against_power(party, wild)
    pp = power_printer(powers, party, wild)
    your_poke = Pokemon(pp[0], poke_type.loc[pp[0], 'hp'], pp[1], poke_type.loc[pp[0], 'sp_defense'])
    wild_mon = Pokemon(wild,poke_type.loc[wild, 'hp'],poke_type.loc[wild, 'sp_attack'],poke_type.loc[wild, 'sp_defense'])
    battle(your_poke, wild_mon)


class Pokemon:
    def __init__(self, name='', hp=0, attack=0, defense=0, **kwargs):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def attack(self):
        return self.attack

    def defense(self):
        return self.defense


def poke_names(file_of_pokemon = poke_type):
    all_pokes = []
    for name, stats in poke_type.iterrows():
        all_pokes.append(name)
    return all_pokes


def party_maker(poke_name_list, trigger = False):
    if trigger == False:
        for name in poke_name_list:
            print(name)
    print('\n' + 'Example party list: Charizard, Moltres, Mew, Snorlax ')
    party = input("Pick up to 6 Pokemon as your party from this list: ")
    clean_party = party.strip()
    indivs = clean_party.split(', ')
    for poke in indivs:
        if poke not in poke_name_list:
            print("Uh oh, one of your pokemon, isn't a pokemon. Let's try again...")
            return party_maker(poke_name_list, True)
        else:
            return indivs


def wild_poke(poke_name_list, trigger = False):
    if trigger == False:
        for name in poke_name_list:
            print(name)
    party = input("Pick one wild pokemon to battle: ")
    wild = party.strip()
    if wild not in poke_name_list:
        print("Hmm, I don't recognize that pokemon. Let's try again...")
        return wild_poke(poke_name_list, True)
    else:
        return wild


def against_power(party_list, wild_poke):
    power_list = []
    wild_t1 = poke_type.loc[wild_poke, 'type1']
    wild_t2 = poke_type.loc[wild_poke, 'type2']
    types = []
    types.append(wild_t1)
    if type(wild_t2) != float:
        types.append(wild_t2)
    for poke in party_list:
        power = poke_type.loc[poke, 'sp_attack']
        multi1 = poke_type.loc[poke, wild_t1]
        type1 = power * multi1
        if len(types) > 1:
            multi2 = poke_type.loc[poke, wild_t2]
            type2 = power * multi2
            if type1 >= type2:
                poke_power = (poke,type1)
                power_list.append(poke_power)
            else:
                poke_power = (poke,type2)
                power_list.append(poke_power)
        else:
            poke_power = (poke,type1)
            power_list.append(poke_power)
    return sorted(power_list, key = lambda x: x[1], reverse = True)


def power_printer(powers_list, party_list, wild_poke):
    best_poke = powers_list[0]
    for poke in powers_list:
        print(poke[0], ' sp-attack: ', poke[1])
    print('Battle between', best_poke[0], 'and', wild_poke, '!')
    return best_poke


def battle(your_poke_class, wild_poke_class, trigger=False):
    if trigger == False:
        damage = your_poke_class.attack - wild_poke_class.defense
        if damage <= 0:
            print(
                "Looks like this Pokemon is too tough!\n It's defense is too high!\n Try again with a different team.")
            return 0
        else:
            return battle(your_poke_class, wild_poke_class, trigger=True)
    elif wild_poke_class.hp <= 0:
        victory = "The wild " + wild_poke_class.name + " has fainted! Congrats trainer, you've won!"
        print(victory)
        return 1
    else:
        damage = your_poke_class.attack - wild_poke_class.defense
        hurt_hp = wild_poke_class.hp - damage
        hurt_poke = Pokemon(wild_poke_class.name, hurt_hp, wild_poke_class.attack, wild_poke_class.defense)
        print("Wild", wild_poke_class.name, "took", damage, '!')
        return battle(your_poke_class, hurt_poke, True)


if __name__ == "__main__":
    main()
