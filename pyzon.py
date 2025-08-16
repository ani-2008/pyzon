import sys

TRUE = "true"
FALSE = "false"
NULL = "null"
QUOTE = '"'
WHITESPACE = [" ","\t","\n","\r","\b"]
LBRACE = "{"
RBRACE = "}"
LBRACKET = "["
RBRACKET = "]"
COMMA = ","
COLON = ":"
SYNTAX = [QUOTE,COLON,COMMA,LBRACKET,RBRACKET,LBRACE,RBRACE]
def lex_str(inp_string):
    string = ''

    if inp_string[0] == QUOTE:
        inp_string = inp_string[1:]
    else:
        return None,inp_string

    for i in inp_string:
        if i == QUOTE:
            return string,inp_string[len(string)+1:]
        else:
            string += i

    raise Exception("Error expected a end of string character")

def lex_num(inp_string):
    number = ''

    numbers_char = [str(n) for n in range(0,11)] + ['e','.','-']

    for i in inp_string:
        if i in numbers_char:
            number += i
        else:
            break

    inp_string = inp_string[len(number):]

    if not number:
        return None,inp_string
    elif '.' in number:
        return float(number),inp_string

    return int(number),inp_string

def lex_bool(inp_string):
    string_len = len(inp_string)

    if string_len >= len(TRUE) and inp_string[:len(TRUE)] == TRUE:
        return True,inp_string[len(TRUE):]
    elif string_len >= len(TRUE) and inp_string[:len(FALSE)] == FALSE:
        return False,inp_string[len(FALSE):]

    return None, inp_string

def lex_null(inp_string):
    string_len = len(inp_string)

    if string_len >= len(NULL) and inp_string[:len(NULL)] == NULL:
        return None,inp_string[len(NULL):]
    return False, inp_string

def parse_array(tokens):
    array = []
    t = tokens[0]

    if t == RBRACKET:
        return array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        array.append(json)

        t = tokens[0]
        if t == RBRACKET:
            return array, tokens[1:]
        elif t != COMMA:
            raise Exception("Expected comma")
        else:
            tokens = tokens[1:]
    raise Exception("Expected ]")


def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == RBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception(f'Expected string key, got: {json_key}')

        if tokens[0] != COLON:
            raise Exception(f'Expected colon after key, got: {t}')

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]

        if t == RBRACE:
            return json_object, tokens[1:]
        elif t != COMMA:
            raise Exception(f'Expected comma, got: {t}')

        tokens = tokens[1:]

    raise Exception('Expected "}" at the end')

def parse(tokens):
    t = tokens[0]
    if t == LBRACKET:
        return parse_array(tokens[1:])
    elif t == LBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


def lex(string):
    tokens = []

    while len(string):
        json_string,string = lex_str(string)
        if json_string is not None:
            tokens.append(json_string)
            continue
        
        json_num,string = lex_num(string)
        if json_num is not None:
            tokens.append(json_num)
            continue

        json_bool,string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null,string = lex_null(string)
        if json_null is None:
            tokens.append(json_null)
            continue
        x = string[0]

        if x in WHITESPACE:
            string = string[1:]
        elif x in SYNTAX:
            tokens.append(x)
            string = string[1:]
        else:
            raise Exception(f"INVALID SYNTAX {x}")

    return tokens

def main(string):
    tokens = lex(string)
    
    return parse(tokens)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        f = open(sys.argv[1])
        st = f.read()
        print(main(st))
    else:
        print("Invalid file try like this-python pyzon.py <path-to-json-file>")
        sys.exit(1)


