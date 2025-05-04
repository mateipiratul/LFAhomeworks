#----------------------------------PARSE HELPER: OBJECT TO MAP-----------------------#
def class_to_dic(nfa):
    dic = {}
    dic["alphabet"] = {char for char in nfa.alphabet}
    dic["start"] = str(nfa.start_state.state_id)
    dic["accept"] = {str(x.state_id) for x in nfa.final_states}
    d_trans = {}
    for state in nfa.states:
        if state not in d_trans:
            d_trans[str(state.state_id)] = {}
        for char in state.transitions.keys():
            d_trans[str(state.state_id)][char] =\
                {str(next_state.state_id) for next_state in state.transitions[char]}
    dic["transitions"] = d_trans
    return dic
#------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------#
def nfa_to_dfa(nfa_config):
    alphabet = nfa_config["alphabet"]
    transitions = nfa_config["transitions"]
    start = nfa_config["start"]
    accept = nfa_config["accept"]

    dfa_start = frozenset([start])

    dfa_states = []
    dfa_transitions = {}
    dfa_accept = set()

    unprocessed = [dfa_start]
    while unprocessed:
        current = unprocessed.pop(0)
        if current not in dfa_states:
            dfa_states.append(current)

        if any(state in accept for state in current):
            dfa_accept.add(current)

        for symbol in alphabet:
            next_state = set()
            # for each NFA state in the current DFA state, get transitions on the symbol
            for state in current:
                # if the state has a transition on this symbol, add the resulting states
                if symbol in transitions.get(state, {}):
                    next_state.update(transitions[state][symbol])
            # convert to frozenset to use as a DFA state
            next_state = frozenset(next_state)
            if not next_state:
                continue  # no transitions on this symbol
            # record the DFA transition.
            dfa_transitions.setdefault(current, {})[symbol] = next_state
            # if the next state hasn't been processed yet, add it to the queue
            if next_state not in dfa_states and next_state not in unprocessed:
                unprocessed.append(next_state)
    dfa = {
        "states": dfa_states,
        "alphabet": list(alphabet),
        "transitions": dfa_transitions,
        "start": dfa_start,
        "accept": list(dfa_accept)
    }
    return dfa
#------------------------------------------------------------------------------------#