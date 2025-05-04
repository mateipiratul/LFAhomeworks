#---------------------------------------------------------------------------------------------#
def dfa_clear_view(dfa):                                                                      #
    alphabet = dfa["alphabet"]                                                                #
    i, states, res_states = 0, {}, []                                                         #
    start_state, final_states = "", []                                                        #
    transitions = {}                                                                          #
    for state in dfa["states"]:                                                               #
        state_name = "q" + str(i)                                                             #
        states[state] = state_name                                                            #
        res_states.append(state_name)                                                         #
        if state == dfa["start"]:                                                             #
            start_state = state_name                                                          #
        if state in dfa["accept"]:                                                            #
            final_states.append(state_name)                                                   #
        i += 1                                                                                #
    for state in dfa["transitions"]:                                                          #
        if state not in transitions:                                                          #
            transitions[states[state]] = {}                                                   #
        for char in dfa["transitions"][state]:                                                #
            transitions[states[state]][char] = states[dfa["transitions"][state][char]]        #
                                                                                              #
    resultant_dfa = {                                                                         #
        "states": res_states,                                                                 #
        "alphabet": alphabet,                                                                 #
        "transitions": transitions,                                                           #
        "start": start_state,                                                                 #
        "accept": final_states                                                                #
    }                                                                                         #
    return resultant_dfa                                                                      #
#---------------------------------------------------------------------------------------------#

#--------------------------------------WORD CHECKER FOR DFA-----------------------------------#
def word_checker(word, dfa):                                                                  #
    currStat = dfa["start"]                                                                   #
    for char in word:                                                                         #
        if char not in dfa["transitions"][currStat]:                                          #
            return False                                                                      #
        if not dfa["transitions"][currStat][char] or not dfa["transitions"][currStat][char]:  #
            return False                                                                      #
        currStat = dfa["transitions"][currStat][char]                                         #
    if currStat not in dfa["accept"]:                                                         #
        return False                                                                          #
    return True                                                                               #
#---------------------------------------------------------------------------------------------#