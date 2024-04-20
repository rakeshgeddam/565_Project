# Memory 

instruction_set = {
    'MMR': 0,
    'MRR': 1,
    'MRM': 2,
    'MIM': 3,
    'ADD': 4,
    'SUB': 5,
    'MUL': 6,
    'DIV': 7,
    'JUMP': 8,
    'JGE': 9,
    'JLE': 10,
    'JNE': 11,
    'CMP': 12,
    'PUSH': 13,
    'POP': 14
}
instruction_sizes = {
    'MMR': [6,2,8],
    'MRR': [6,2,2],
    'MRM': [6,8,2],
    'MIM': [6,2,8],
    'ADD': [6,2,2],
    'SUB': [6,2,2],
    'MUL': [6,2,2],
    'DIV': [6,2,2],
    'JUMP': [6,10],
    'JGE': [6,10],
    'JLE': [6,10],
    'JNE': [6,10],
    'CMP': [6,10]
}



Registers = {
    "eax": None,
    "ebx": None,
    "ecx": None,
    "edx": None
}
register_address = {
    "eax": 0,
    "ebx": 1,
    "ecx": 2,
    "edx": 3
}

arith_operators = {
    "+" : "ADD",
    "-" : "SUB",
    "*" : "MUL",
    "/" : "DIV"
}

relational_operators = {
    "==":"JNE",
    "!=":"JE",
    "<": "JGE",
    ">":"JLE",
    "<=":"JG",
    ">=":"JL"
}

# Variable information Dictionary
# Structure {variable_name:"",variable_type:"",variable_value:"" }
variables_dictionary = {}

register_values = {}
# {variable_name : address}
variable_address = {}
# {instruction : address}
instruction_address = {}
label_address = {}
variables_in_progress = []
variable_values = {}

signed_variables = []
unsigned_variables = []
hlc_to_assembly = {}
output = {"HLC instruction":[],"YMC address":[],"YMC assembly":[],
          "YMC ENCODING":[],"Modified Registers":[],"Modified flags":[]}