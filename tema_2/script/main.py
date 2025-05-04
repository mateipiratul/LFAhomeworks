# definirea alfabetului: [a-zA-Z0-9]

#--------------------------------IMPORTS--------------------------------#
import json                                                             #
from tema_2.script.REGEX_RPN import shunting_yard                       #
from tema_2.script.RPN_NFA import rpn_to_enfa, enfa_to_nfa              #
from tema_2.script.NFA_DFA import class_to_dic, nfa_to_dfa              #
from tema_2.script.DFA_word_checker import dfa_clear_view, word_checker #
#-----------------------------------------------------------------------#

#-----------JSON FILE PARSER-----------#
def json_parser(json_file_path):       #
    with open(json_file_path) as file: #
        data = json.load(file)         #
    return data                        #
#--------------------------------------#

def main(file_path):
    json_regex = json_parser(file_path)

    for test_case in json_regex:
        name = test_case["name"]
        regex = test_case["regex"]

        dfa = dfa_clear_view(nfa_to_dfa(class_to_dic(enfa_to_nfa(rpn_to_enfa(shunting_yard(regex))))))
        print(f"Test case: {name} - RegEx: {regex}")

        for test_string in test_case["test_strings"]:
            input_string = test_string["input"]
            expected = test_string["expected"]
            print(f"Word given: {input_string} - ", end="")
            if word_checker(input_string, dfa) == expected:
                if expected is True:
                    print("PASSED")
                else:
                    print("FAILED")
            else:
                print("FATAL ERROR")
                break
        print()

if __name__ == '__main__':
    # json_file_path = input("Please, provide the path of the .json file: ")
    # main(json_file_path)
    main("../LFA-Assignment2_Regex_DFA_v2.json")
