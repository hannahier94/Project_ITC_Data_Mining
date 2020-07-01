import argparse

def add(*args):
    """This function combines the default search and the additional topics into a uniform format without duplicates"""
    def_search = [z.lower() for z in DEFAULT_SEARCH]
    topics = [x.lower().replace('_'," ") for x in args[0] if x.lower().replace('_'," ") not in def_search]
    return def_search + topics

def default(*args):
    """This function returns a uniform format for the default topics"""
    return [z.lower() for z in DEFAULT_SEARCH]

def custom(*args):
    """This function returns a uniform format for the custom input topics"""
    return [x.lower().replace('_'," ") for x in args[0]]


## ARGParse set-up
# actualy default list will change, this is just for show
DEFAULT_SEARCH = ['data science', 'ML', 'AI', 'data']

topics_to_search = []

FUNCTION_MAP = {'default': default,
                'add': add,
                'custom': custom}

# Takes in inputs from argparse
parser = argparse.ArgumentParser(f"""Welcome to the Reddit Web Scraper!\n The default list to scrape is: \n {DEFAULT_SEARCH}\n Enter -h for help.""" )

parser.add_argument('command', choices=FUNCTION_MAP.keys(),
                    type=str, nargs=1, help='''Any two word topics  should be separated with an underscore 
                    (ex: to search 'data science', input data_science .
                    Options include 
                    default, add, replace, custom .\n
                    default : search only default topics, \n
                    add: keep default topics and add your own, \n
                    custom: provide your own topics to search.
''')
parser.add_argument('topics',nargs='+')

#input_args = parser.parse_args("custom data_science hello".split())   # Test

input_args = parser.parse_args()

def main(args):
    """
    Directs script to correct function based on inputs
    Author : Hanna Hier
    """
    #num1, num2 = float(args.number1), float(args.number2)

    topics_to_search = []
    func = FUNCTION_MAP[input_args.command[0]]
    return print(func(input_args.topics))



if __name__ == '__main__':
    #pass
    main(input_args)
