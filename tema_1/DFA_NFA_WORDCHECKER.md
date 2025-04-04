# coqFAchecker

A script that checks if the description of a finite automaton is valid and determines whether it is deterministic (DFA) or non-deterministic (NFA), and also lets the user provide various words, that are then chcked if they can be accepted by the automaton or not

## Table of Contents
- [1. Parser](#parser)
- [2. Validity Checker](#validity-checker)
- [3. Automaton Processing](#automaton-processing)
  - [3.1. Mapping of Transitions](#mapping-of-transitions)
  - [3.2. Automaton Type Determination](#automaton-type-determination)
- [4. Word Checker](#word-checker)
- [5. Main Function](#main-function)

---

## Parser

### `configFileParser(filePath)`
This function takes the absolute path of the text file describing the automaton and parses its contents. It reads the file into an array of strings (each representing a row). Three empty arrays are initialized:

1. **`states`**: Stores the automaton's states.
2. **`transitions`**: To be converted into a dictionary mapping transitions.
3. **`alphabet`**: Stores all allowed letters.

It utilizes the `readLinesWhile(block)` function to extract relevant sections from the input file *(block being a slice of the array of strings)*, ignoring comments in the meantime. The function returns the three arrays after parsing.

---

## Validity Checker

### `solveSigmaConflicts(transitions, sigma)`
Checks for inconsistencies between the `transitions` array and the `alphabet` array. If any letter appears in `transitions` but not in `alphabet`, the function returns `False`. Otherwise, it returns `True`.

### `solveStateConflicts(transitions, states)`
Checks for inconsistencies between the `transitions` array and the `states` array. If any state in `transitions` is missing from `states`, the function returns `False`; otherwise, it returns `True`.

### `checkStates(states)`
Verifies the validity of the automaton by ensuring there is exactly **one initial state**. If valid, it returns:
- The **unique initial state**.
- An **array of final states** (which may be empty but still valid).

If multiple or zero initial states exist, it returns `False`.

---

## Automaton Processing

### Mapping of Transitions

### `transitPathing(transit)`
This function processes the `transitions` array into a dictionary. The structure of the dictionary is:

```python
dic[currentState][letter] = [listOfNextStates]
```

The dictionary facilitates both word processing and automaton type determination.

---

### Automaton Type Determination

### `determineType(dic)`
Determines if the automaton is **deterministic** or **non-deterministic** by checking the length of the state arrays for each letter:
- If any transition contains more than one possible next state, the automaton is **non-deterministic (NFA)**.
- Otherwise, it is **deterministic (DFA)**.

The function returns a tuple containing:
- A string indicating the automaton type (`"determinist (DFA)"` or `"nedeterminist (NFA)"`).
- A numerical flag to assist in word checking.

---

## Word Checker

### `wordChecker(word, init, fin, transit, automatonType)`

This function checks whether a given word is accepted by the automaton. It follows different approaches based on the automaton type:

#### **Deterministic Case (DFA)**
- Iterates through the word linearly.
- If the transition is undefined, the word is **rejected**.
- If the final state after full traversal is in the `final_states` array, the word is **accepted**; otherwise, it is **rejected**.

#### **Non-Deterministic Case (NFA)**
- Maintains a list of **possible current states**.
- Iterates through the word, updating the list based on available transitions.
- If the list becomes empty, the word is **rejected**.
- If any state in the final set is reached, the word is **accepted**.

---

## Main Function

### `main()`

The script interaction is straightforward:
1. The user provides an **absolute file path** to the automaton description.
2. The script validates the automaton and displays an appropriate message, including its **type** (DFA or NFA).
3. The user inputs words to test against the automaton.
4. The script checks each word and prints an acceptance or rejection message.
5. To exit, the user will simply input `KILL PROCEDURE`.

---

## Usage Example

Example input/output:
```plaintext
Calea absoluta a fisierului: /path/to/automaton.txt
Automatul este valid determinist (DFA)

Cuvantul de verificat: abba
cuvantul FACE parte din limbaj!

Cuvantul de verificat: abab
cuvantul NU face parte din limbaj

Cuvantul de verificat: KILL PROCEDURE
ENDING PROCEDURE...
```

---
