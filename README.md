# **Teme de laborator la LFA**

**`1)` Finite Automata Checker** Determines if a finite automata is either *deterministic or not*, and if a *particular word* is part of the *language described by the given automata*.

**`2)` Regular Expression to Deterministic Finite Automata Conversion** A script that goes through each step of converting a *regular expression* into a *deterministic finite automata*, as it follows: 
- **RegEx** to **RPN** *(reverse polish notation)*;
- **RPN** to **ε-NFA** *(epsilon non-deterministic finite automata)*;
- **ε-NFA** to **NFA** *(non-deterministic finite automata)*;
- **NFA** to **DFA** *(deterministic finite automata)*.

The script will then check if for the given RegEx, a set of words *(all provided via json files)* can be accepted by its **DFA machine**.

**`3)`**