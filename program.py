################################################################################
# Program     : Lark Parser Generator Demo                                     #
# Authors     : David Velez and Patrick                                        #
# Date        : 11/27/18                                                       #
# Description : Demonstrate the Lark Parser Generator and how it can parse     #
#               dictionaries, lists, strings, numbers, pairs, and user defined #
#               variables, all within python                                   #
################################################################################

# Imports
import os
from lark import Lark

# Global Directories
base_folder = os.path.dirname(__file__)
data = os.path.join(base_folder, "json")


# Main
def main():
    print_header()
    # test_lark_grammar()
    custom_json_parser()


def print_header():
    print("---------------------------------")
    print("   Lark Parser Generator Demo")
    print("---------------------------------")
    print()


def test_lark_grammar():
    json_parser = Lark(r"""
    value: dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" value

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value')

    # Things to call - Use Python Console for better demonstration
    text = '{"key": ["item0", "item1", 3.14]}'
    print(json_parser.parse(text).pretty())


def custom_json_parser():
    json_parser = Lark(r"""
    ?value: dict
          | list
          | ESCAPED_STRING
          | SIGNED_NUMBER      -> decimal
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value
    
    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value')
    monsters = os.path.join(data, "monsters")

    with open(monsters) as f:
        monster_json = json_parser.parse(f.read())
        print(monster_json.pretty())


if __name__ == "__main__":
    main()
