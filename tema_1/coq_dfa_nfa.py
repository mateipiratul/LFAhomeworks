# Cocu Matei-Iulian
# Grupa 152
# Python 3.12.6

#-----------------------------------------File Parsing-----------------------------------------#
def readLinesWhile(block):
    data, i = [], 0 # tratarea tuplurilor din sectiunile STATES si TRANSITIONS
    while i < len(block) and block[i].strip().upper() != "END":
        if block[i].strip() and block[i].strip()[0] != "#":
            data_tuple = block[i].strip().replace(",", " ").split()
            data.append(data_tuple)
        i += 1  # i = indentatia de returnat in functia principala
    return data, i

def configFileParser(filePath):
    file = open(filePath) # parsarea fisierului
    lines = file.readlines() # crearea unui vector de string-uri
    states, transitions, alphabet = [], [], []
    i = 0
    while i < len(lines): # iteratia principala
        if lines[i].strip().upper() == "STATES:":
            states, indent = readLinesWhile(lines[i+1:])
            i += indent
        elif lines[i].strip().upper() == "TRANSITIONS:":
            transitions, indent = readLinesWhile(lines[i+1:])
            i += indent
        elif lines[i].strip().upper() == "SIGMA:":
            i += 1
            while i < len(lines) and lines[i].strip().upper() != "END":
                if lines[i].strip() and lines[i].strip()[0] != "#":
                    alphabet.append(lines[i].strip())
                i += 1
        i += 1
    return states, transitions, alphabet # cele 3 sectiuni ale automatului
#----------------------------------------------------------------------------------------------#


#-----------------------------------------Automata Issue Checker-----------------------------------------#
def solveSigmaConflicts(transitions, sigma):
    # verificare daca exista litere in tranzitiile
    # date care nu exista in alfabetul dat ca input
    for transit in transitions:
        if transit[1] not in sigma:
            return False
    return True

def solveStateConflicts(transitions, states):
    nodes = [] # vectorul de stari de returnat
    # verificare daca exista stari in tranzitiile
    # date care nu exista in starile date ca input
    for state in states:
        nodes.append(state[0])
    for transit in transitions:
        if transit[0] not in nodes or transit[2] not in nodes:
            return False # conflicte la nivelul tranzitiilor
    return nodes # daca nu, este returnat vectorul de stari

def checkStates(states):
    contor, finalStates, startState = 0, [], ""
    for stat in states:
        if contor > 1:
            return False # exista mai mult
        # de o singura stare de intrare
        if len(stat) == 3:
            contor += 1
            startState = stat[0]
            finalStates.append(stat[0])
        elif len(stat) == 2:
            if stat[1].upper() == "S":
                contor += 1
                startState = stat[0]
            elif stat[1].upper() == "F":
                finalStates.append(stat[0])
    if contor == 0:
        return False # nu exista stare de intrare
    return startState, finalStates # automatul este valid
#--------------------------------------------------------------------------------------------------------#


#--------------------------Transition mapping and automata type determination----------------------------#
def transitPathing(transit):
    dic = {} # este creat dictionarul tranzitiilor
    for trans in transit: # iterarea prin array-ul de tranzitii
        if trans[0] not in dic:
            dic[trans[0]] = {}
        if trans[1] not in dic[trans[0]]: # daca este DFA
            dic[trans[0]][trans[1]] = [] # acest array are lungimea 1
        if trans[2] not in dic[trans[0]][trans[1]]:
            dic[trans[0]][trans[1]].append(trans[2])
    return dic # pentru cazul NFA, lungimea array-ului poate fi > 1

def determineType(dic):
    for trans in dic: # primul return este string-ul afisat in terminat
        for letter in dic[trans]: # al doilea este o valoare booleana
            if len(dic[trans][letter]) > 1: # necesara functiei wordChecker
                return "nedeterminist (NFA)\n", 0
    return "determinist (DFA)\n", 1
#--------------------------------------------------------------------------------------------------------#


#-----------------------------------------Word Checking-----------------------------------------#
def wordChecker(word, init, fin, transit, automaType):
    if automaType: # cazul DFA
        currStat = init # initierea starii initiale
        for char in word: # iterarea prin literele cuvantului
            if char not in transit[currStat]: # nu exista muchii valabile
                return "cuvantul NU face parte din limbaj"
            if not transit[currStat][char] or not transit[currStat][char][0]:
                return "cuvantul NU face parte din limbaj"
            currStat = transit[currStat][char][0] # se trece la urmatoarea stare
        if currStat not in fin: # verificam daca starea finala a cuvantului este valida
            return "cuvantul NU face parte din limbaj"
        return "cuvantul FACE parte din limbaj!"
    else: # cazul NFA
        currStats = [init] # array-ul de stari curente
        for char in word: # iterarea prin literele cuvantului
            auxStats = [] # array auxiliar pentru currStats
            for stat in currStats: # iterarea prin starile curente (pot fi mai multe)
                if char in transit[stat]:
                    for nextStat in transit[stat][char]:
                        if nextStat not in auxStats:
                            auxStats.append(nextStat) # sunt adaugate doar starile valide
            currStats = auxStats
            if not currStats: # daca nu mai exista stari valabile
                return "cuvantul NU face parte din limbaj"
        for stat in currStats:
            if stat in fin: # verificam daca starile finale ale cuvantului sunt valide
                return "cuvantul FACE parte din limbaj!" # este necesara cel putin una
        return "cuvantul NU face parte din limbaj" # daca nu exista NICI o stare valida
#-----------------------------------------------------------------------------------------------#


#-----------------------------------------MAIN-----------------------------------------#
def main():
    fileAbsolutePath = input("Calea absoluta a fisierului: ") # path-ul absolut al fisierului dat ca string
    stat, transit, sigma = configFileParser(fileAbsolutePath) # parsarea datelor din fisier

    if not(solveSigmaConflicts(transit, sigma) and solveStateConflicts(transit, stat)):
        print("!!Automatul este invalid (prin conflicte logice la nivelul declararii datelor de intrare)")
        return
    if not checkStates(stat): # probleme la starea initiala (starting state)
        print("!!Automatul este invalid (nu exista o unica stare initiala/ de intrare)")
        return
    else: # automatul este valid, sunt determinate starile speciale (starea initiala si starile finale)
        print("Automatul este valid ", end="")
        initState, finStates = checkStates(stat)

    dicTransit = transitPathing(transit) # maparea tranzitiilor
    print(determineType(dicTransit)[0]) # determinarea tipului de automat

    while (True):
        inputWord = input("Cuvantul de verificat: ") # cuvantul de verificat
        inputWord = inputWord.strip()
        if inputWord.upper() == "KILL PROCEDURE":
            print("ENDING PROCEDURE...")
            break
        print(wordChecker(inputWord, initState, finStates, dicTransit, determineType(dicTransit)[1]))
        print()

if __name__ == '__main__':
    main()
#--------------------------------------------------------------------------------------#