#1/usr/bin/env python


import inquirer
import fire

class BreakPylint:
    def __init__(self):
        print("i'm innit'")
        print("This line is way to long and it should definitely not pass the linter since it has more than 100 characters")

if __name__ == '__main__':
    fire.Fire()



