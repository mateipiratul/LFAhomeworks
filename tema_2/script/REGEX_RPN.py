#----------------------APPROACH---------------------#
#   before  postfixating  the input  string, the    #
#   string  will  be  written  in  its  explicit    #
#   form, for the ease of  use for concatenation    #
#                                                   #
#      cases when explicit concatenation is needed: #
# if curr_char(isalnum or ')' or '*' or '+' or '?') #
#                AND next_char_char(isalnum or '(') #
#---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
def shunting_yard(string):                                                                                             #
    precedence = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}                                                              #
    fin_output = [] # result array                                                                                     #
    operator_stack = []                                                                                                #
                                                                                                                       #
    i = 0 # conversion to explicit form for                                                                            #
    explicit_regex = [] # concatenation operator                                                                       #
    while i < len(string):                                                                                             #
        explicit_regex.append(string[i])                                                                               #
                                                                                                                       #
        if i < len(string) - 1: # concatenation cases                                                                  #
            curr_char, next_char = string[i], string[i + 1]                                                            #
            # check for possible concatenations                                                                        #
            if ((curr_char.isalnum() or curr_char == ')' or curr_char == '*' or curr_char == '+' or curr_char == '?')  #
                and (next_char.isalnum() or next_char == '(')):                                                        #
                explicit_regex.append('.')                                                                             #
                                                                                                                       #
        i += 1                                                                                                         #
                                                                                                                       #
    for char in explicit_regex:                                                                                        #
        if char == '(':                                                                                                #
            operator_stack.append(char) # treating the start of a parentheses                                          #
        elif char == ')':                                                                                              #
            while operator_stack and operator_stack[-1] != '(':                                                        #
                fin_output.append(operator_stack.pop()) # treating the operations                                      #
            if operator_stack[-1] == '(': # inside a parentheses accordingly                                           #
                operator_stack.pop() # closing the parentheses                                                         #
        elif char in precedence: # operations                                                                          #
            while (operator_stack and operator_stack[-1] != '(' and                                                    #
                   precedence[char] <= precedence[operator_stack[-1]]):                                                #
                fin_output.append(operator_stack.pop()) # determine the priority of operations                         #
            operator_stack.append(char) # letter of the alphabet                                                       #
        else:                                                                                                          #
            fin_output.append(char)                                                                                    #
                                                                                                                       #
    while operator_stack:                                                                                              #
        fin_output.append(operator_stack.pop())                                                                        #
                                                                                                                       #
    return ''.join(fin_output)                                                                                         #
#----------------------------------------------------------------------------------------------------------------------#