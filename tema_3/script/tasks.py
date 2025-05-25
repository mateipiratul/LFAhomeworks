# Cocu Matei-Iulian - 152

import random as rand

class CFG:
    def __init__(self): # member data
        self.non_terminals = set()
        self.terminals = set()
        self.productions = []
        self.start_symbol = None

    # member functions for data manipulation
    def set_start_symbol(self, symbol):
        self.start_symbol = symbol
        self.non_terminals.add(symbol)

    def add_production(self, production):
        if production not in self.productions:
            self.productions.append(production)
            for symbol in production: # symbol sorting
                if symbol.islower():
                    self.terminals.add(symbol)
                else:
                    self.non_terminals.add(symbol)

    # printing member functions
    def print_cfg(self): # display of given CFG
        prods = " | ".join(self.productions)
        print(self.start_symbol, "->", prods)

    def print_cfg_info(self): # component display of given CFG
        print("Start symbol:", self.start_symbol)
        print("Non-terminals:", self.non_terminals)
        print("Terminals:", self.terminals)
        print("Productions:", self.productions)

    def production_choice(self): # weighted decision
        non_epsilon_productions = [prod for prod in self.productions if prod != "ε"]
        epsilon_chance = 50 / len(self.productions) # epsilon has smaller chance
        if rand.randint(1, 100) <= epsilon_chance: # of being picked
            return "ε"
        else: # rest of the productions are 'equally weighed'
            return non_epsilon_productions[rand.randint(0, len(non_epsilon_productions) - 1)]


def string_generator(cfg, max_num_words=10, max_word_length=10):
    print("Randomly generated strings from the given CFG:")
    generated_strings = [] # keep track of all strings

    for i in range(max_num_words):
        current_string= cfg.start_symbol

        while any(symbol in cfg.non_terminals for symbol in current_string):
            for j, symbol in enumerate(current_string):
                if symbol in cfg.non_terminals:
                    chosen_prod = cfg.production_choice()
                    if chosen_prod == "ε":
                        current_string = current_string[:j] + current_string[j + 1:]
                    else:
                        current_string = current_string[:j] + chosen_prod + current_string[j + 1:]
                    break

        if len(current_string) <= max_word_length:
            if current_string:
                generated_strings.append(current_string)
            else:
                generated_strings.append("ε")
    for i in range(len(generated_strings)):
        print(f"{i + 1}. {generated_strings[i]}")
    return generated_strings # strings will also be returned in array

# derivation generator and membership checker function
def membership_derivation(cfg, target_string=""):
    derivation_steps = [] # stack of steps taken
    if target_string == "ε": # empty string edge case
        target_string = ""

    def find_derivation(current_string, steps):
        steps.append(current_string)

        curr_str_wo_eps = current_string.replace("ε", "") # removal of all
        if curr_str_wo_eps == target_string: # epsilon symbols in current word
            return True # so it can be checked accordingly with the target word

        if not any(symbol in cfg.non_terminals for symbol in current_string):
            steps.pop() # if there are not any non-terminal symbols left, yet
            return False # the current word does not match with the target

        if len(current_string) > len(target_string) + 1:
            steps.pop() # avoid infinite recursion case if the current word
            return False # is bigger than the target word

        for i, symbol in enumerate(current_string):
            if symbol in cfg.non_terminals:
                for prod in cfg.productions:
                    new_string = current_string[:i] + prod + current_string[i + 1:]

                    if find_derivation(new_string, steps):
                        return True
                break

        steps.pop()
        return False

    if find_derivation(cfg.start_symbol, derivation_steps):
        print("Derivation found: ", end="")
        print(" -> ".join(derivation_steps), end="")
        if len(target_string) > 1: # add the additional step of removing
            print(f" -> {target_string}") # all epsilon symbols
        return True # boolean membership tester
    else:
        print(f"No derivation found - {target_string} NOT in language") # prints
        return False # negative message and returns boolean value accordingly