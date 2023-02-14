
RULE_SET = [
    
]


def syntax_analyze(code):
    print("PARSER: \n")
    for line in code.lines:
        for token in line:
            print(token.identif, end="  ")
        print()
