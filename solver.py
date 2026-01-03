import sys



def parse_equation(equation):
    pass


def main(equation:str): 
    
    res = parse_equation(equation)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else: 
        equation = input("Enter the equation:\n")
        main(equation)