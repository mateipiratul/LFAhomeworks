#----------------------NFA STRUCTURE-----------------------#
state_counter = 0                                          #
class State: # structure of a state (node)                 #
    def __init__(self, state_id=None):                     #
        self.state_id = state_id # unique number of state  #
        self.transitions = {} # transitions of the state   #
        self.eps_trans = [] # epsilon transitions          #
        self.is_final = False # final (terminal) state     #
#----------------------------------------------------------#
class FA:                                                  #
    def __init__(self):                                    #
        self.states = []                                   #
        self.start_state = None                            #
        self.alphabet = set()                              #
                                                           #
    def add_state(self):                                   #
        global state_counter                               #
        state = State(state_counter)                       #
        state_counter += 1                                 #
        self.states.append(state)                          #
        return state                                       #
                                                           #
class ENFA(FA):                                            #
    def __init__(self):                                    #
        super().__init__()                                 #
        self.final_state = None                            #
                                                           #
class NFA(FA):                                             #
    def __init__(self):                                    #
        super().__init__()                                 #
        self.final_states = []                             #
#----------------------------------------------------------#

#-----------------------------------------------POSTFIX TO ENFA--------------------------------------------------#
def rpn_to_enfa(postfix):                                                                                        #
    nfa_stack = [] # keep track of all NFA structures                                                            #
                                                                                                                 #
    for c in postfix:                                                                                            #
        if c == '*' or c == '+': # Kleene Star or Plus                                                           #
            if not nfa_stack:                                                                                    #
                raise ValueError(f"Invalid expression: '{c}' operator requires an operand")                      #
                                                                                                                 #
            nfa1 = nfa_stack.pop() # NFA selection for                                                           #
            new_nfa = ENFA() # applying the Kleene Star                                                          #
                                                                                                                 #
            start = new_nfa.add_state() # add a new initial state                                                #
            end = new_nfa.add_state() # add a new end state                                                      #
            end.is_final = True # make it final                                                                  #
                                                                                                                 #
            # transition from new initial state to former one                                                    #
            start.eps_trans.append(nfa1.start_state)                                                             #
            if c == '*':                                                                                         #
                start.eps_trans.append(end) # character may have no repetitions                                  #
                                                                                                                 #
            nfa1.final_state.eps_trans.append(nfa1.start_state) # loop                                           #
            nfa1.final_state.eps_trans.append(end) # exit loop                                                   #
            nfa1.final_state.is_final = False # former final state gets revoked of property                      #
                                                                                                                 #
            # add new NFA structure to the stack                                                                 #
            new_nfa.start_state = start                                                                          #
            new_nfa.final_state = end                                                                            #
            new_nfa.alphabet = nfa1.alphabet                                                                     #
            new_nfa.states.extend(nfa1.states)                                                                   #
            nfa_stack.append(new_nfa)                                                                            #
                                                                                                                 #
        elif c == '?': # Optional character                                                                      #
            if not nfa_stack:                                                                                    #
                raise ValueError(f"Invalid expression: '{c}' operator (optional 'letter') requires an operand")  #
                                                                                                                 #
            nfa1 = nfa_stack.pop()                                                                               #
            new_nfa = ENFA()                                                                                     #
                                                                                                                 #
            start = new_nfa.add_state()                                                                          #
            end = new_nfa.add_state()                                                                            #
            end.is_final = True                                                                                  #
                                                                                                                 #
            start.eps_trans.append(nfa1.start_state) # either take character as input                            #
            start.eps_trans.append(end) # or just an epsilon-transition                                          #
                                                                                                                 #
            nfa1.final_state.eps_trans.append(end) # exit former nfa                                             #
            nfa1.final_state.is_final = False                                                                    #
                                                                                                                 #
            new_nfa.start_state = start                                                                          #
            new_nfa.final_state = end                                                                            #
            new_nfa.alphabet = nfa1.alphabet                                                                     #
            new_nfa.states.extend(nfa1.states)                                                                   #
            nfa_stack.append(new_nfa)                                                                            #
                                                                                                                 #
        elif c == '.': # Concatenation                                                                           #
            if len(nfa_stack) < 2:                                                                               #
                raise ValueError("Invalid expression: '.' operator (concatenation) requires two operands")       #
                                                                                                                 #
            nfa2 = nfa_stack.pop()                                                                               #
            nfa1 = nfa_stack.pop()                                                                               #
                                                                                                                 #
            # connect 1st NFA final state to the start state of the 2nd one and revoke property                  #
            nfa1.final_state.eps_trans.append(nfa2.start_state)                                                  #
            nfa1.final_state.is_final = False                                                                    #
                                                                                                                 #
            nfa1.final_state = nfa2.final_state                                                                  #
            nfa1.alphabet.update(nfa2.alphabet)                                                                  #
            nfa1.states.extend(nfa2.states)                                                                      #
            nfa_stack.append(nfa1)                                                                               #
                                                                                                                 #
        elif c == '|': # Union (OR operation)                                                                    #
            if len(nfa_stack) < 2:                                                                               #
                raise ValueError("Invalid expression: '|' operator (union) requires two operands")               #
                                                                                                                 #
            nfa2 = nfa_stack.pop()                                                                               #
            nfa1 = nfa_stack.pop()                                                                               #
            new_nfa = ENFA() # create bifurcation                                                                #
                                                                                                                 #
            start = new_nfa.add_state()                                                                          #
            end = new_nfa.add_state()                                                                            #
            end.is_final = True                                                                                  #
                                                                                                                 #
            # connect new initial state to both former initial states of the NFAs                                #
            start.eps_trans.append(nfa1.start_state)                                                             #
            start.eps_trans.append(nfa2.start_state)                                                             #
                                                                                                                 #
            # connect both final states of the two NFAs to the new final state and revoke property               #
            nfa1.final_state.eps_trans.append(end)                                                               #
            nfa2.final_state.eps_trans.append(end)                                                               #
            nfa1.final_state.is_final = False                                                                    #
            nfa2.final_state.is_final = False                                                                    #
                                                                                                                 #
            new_nfa.start_state = start                                                                          #
            new_nfa.final_state = end                                                                            #
            new_nfa.alphabet = nfa1.alphabet.union(nfa2.alphabet)                                                #
            new_nfa.states.extend(nfa1.states)                                                                   #
            new_nfa.states.extend(nfa2.states)                                                                   #
            nfa_stack.append(new_nfa)                                                                            #
                                                                                                                 #
        else: # simple character                                                                                 #
            new_nfa = ENFA()                                                                                     #
                                                                                                                 #
            start = new_nfa.add_state()                                                                          #
            end = new_nfa.add_state()                                                                            #
            end.is_final = True                                                                                  #
                                                                                                                 #
            if c not in start.transitions:                                                                       #
                start.transitions[c] = [end]                                                                     #
                                                                                                                 #
            new_nfa.start_state = start                                                                          #
            new_nfa.final_state = end                                                                            #
            new_nfa.alphabet.add(c) # add new character to the alphabet                                          #
            nfa_stack.append(new_nfa)                                                                            #
                                                                                                                 #
    if len(nfa_stack) != 1: # throw error                                                                        #
        raise ValueError("Invalid expression: too many operands")                                                #
                                                                                                                 #
    return nfa_stack.pop() # return updated NFA                                                                  #
#----------------------------------------------------------------------------------------------------------------#

#----------------------------------------ENFA TO NFA-------------------------------------#
def enfa_to_nfa(enfa):                                                                   #
    nfa = NFA() # initiate NFA                                                           #
    state_map = {s: nfa.add_state() for s in enfa.states} # copy former ENFA states      #
                                                                                         #
    nfa.start_state = state_map[enfa.start_state] # copy former starting ENFA state      #
    nfa.alphabet = enfa.alphabet # alphabet remains the same                             #
                                                                                         #
    # compute all possible epsilon-closures for each state                               #
    eps_closure = {s: compute_eps_closure(s) for s in enfa.states}                       #
                                                                                         #
    for state in enfa.states: # build the NFA                                            #
        new_state = state_map[state]                                                     #
        closure = eps_closure[state]                                                     #
                                                                                         #
        for char in enfa.alphabet:                                                       #
            reachable = set()                                                            #
            for state in closure:                                                        #
                if char in state.transitions:                                            #
                    for x in state.transitions[char]:                                    #
                        reachable.update(eps_closure[x])                                 #
            if reachable:                                                                #
                new_state.transitions[char] = [state_map[t] for t in reachable]          #
                                                                                         #
    for state in enfa.states: # set all final states of NFA based on initial final state #
        if any(s.is_final for s in eps_closure[state]): # utilizing the epsilon-closures #
            state_map[state].is_final = True                                             #
            nfa.final_states.append(state_map[state])                                    #
                                                                                         #
    return nfa                                                                           #
#------------------------------------------------------------------#---------------------#
# recursive function, searches for all epsilon-closures of a state #
def compute_eps_closure(state, visited=None):                      #
    if visited is None: # initialize set of visited states         #
        visited = set()                                            #
    if state in visited:                                           #
        return set()                                               #
    visited.add(state)                                             #
                                                                   #
    result = {state}                                               #
    for eps_state in state.eps_trans:                              #
        result.update(compute_eps_closure(eps_state, visited))     #
    return result                                                  #
#------------------------------------------------------------------#