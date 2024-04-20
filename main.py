import sys
from data import *
import math
import Memory as M
import csv
import pandas as pd
m = M.Memory()

#===========================================
#  1. Function Name: setAddress  
#  2. Description: Increments the address of the data part of the memory and assigns it  
#  to particular element
#  3. Input_arguments: variable name for which the address needs to be reserved   
#===========================================
def setAddress(variable):
    variable_address[variable] = m.current_data_addr - m.data_start_addr
    m.occupyMemory(8)
    return variable_address[variable]

#===========================================
#  1. Function Name: setRegisterFor  
#  2. Description: Increments the address of the data part of the memory and assigns it  
#  to particular element
#  3. Input_arguments: variable name for which the address needs to be reserved   
#===========================================
def setRegisterFor(variable):
    for i in Registers:
        if Registers[i] == None:
            Registers[i] = {'var_name': variable}
            return i
    for i in Registers:
        if i not in variables_in_progress:
            Registers[i] = None
            variables_in_progress.append(variable)
            return i

#===========================================
#  1. Function Name: getRegisterFor  
#  2. Description: Increments the address of the data part of the memory and assigns it  
#  to particular element
#  3. Input_arguments: variable name for which the address needs to be reserved   
#===========================================
def getRegisterFor(variable):
    for i in Registers:
        if Registers[i] == None:
            continue
        if variable == Registers[i]['var_name']:
            return i
    return setRegisterFor(variable)

#===========================================
#  1. Function Name: generateAssembly  
#  2. Description: Increments the address of the data part of the memory and assigns it  
#  to particular element
#  3. Input_arguments: variable name for which the address needs to be reserved   
#===========================================
def generateAssembly(line):
    assembly_line = ""
    arith = False
    if "print" in line:
        assembly_line += f"PUSH  {hex(m.current_data_addr)} , {hex(int(line.strip().split(" ")[1].strip()))} \n"
        m.occupyMemory(8)
        return assembly_line
    for i in arith_operators:
        if i in line:
            line_split = line.strip().split("=")
            variable = line_split[0]
            expression = line_split[1]
            operand1 = expression.split(i)[0].strip()
            operand2 = expression.split(i)[1].strip()
            if operand1 == "":
                arith = False
                break
            else:
                arith = True
            register_op1 = getRegisterFor(operand1)
            if operand2.isdigit():
                register_op2 = operand2
            else:
                register_op2 = getRegisterFor(operand2)
                operand2 = f"ptr[{operand2}]"

            operation = arith_operators[i]
            assembly_line += f"MMR {register_op1} , ptr[{operand1}]\n"
            assembly_line += f"MMR {register_op2} , {operand2}\n"
            assembly_line += f"{operation} {register_op1} , {register_op2} \n"
            assembly_line += f"MRM ptr[{variable.strip()}] , {register_op1} \n"
            if operand1 in variables_in_progress:
                variables_in_progress.remove(operand1)
            if operand2 in variables_in_progress:
                variables_in_progress.remove(operand1)
            break 


    if arith == False:    # Normal Assignment
        line_split = line.split("=")
        variable = line_split[0].strip()
        value = line_split[1].strip()
        assembly_line += f"MIM ptr[{variable}] , {value} \n"
        variables_dictionary[variable]["value"] = value

    return assembly_line

#===========================================
#  1. Function Name: readFile  
#  2. Description: Increments the address of the data part of the memory and assigns it  
#  to particular element
#  3. Input_arguments: variable name for which the address needs to be reserved   
#===========================================
def readFile(file_name):
    with open(file_name) as f:
        content = ""
        loop_counter = 1
        is_if_block = False
        is_else_block = False
        is_loop = False
        for line in f:
            assembly_line = ""

            if "signed" in line or "unsigned" in line:
                var_type = line.split(" ")[0]
                variables = line.split(" ")[1].split(",")
                for i in variables:
                    variables_dictionary[f"{i}".strip()] = {"var_name":i,"type":var_type,"value":None,"address":setAddress(i)}
                continue
            if line == "" or line.strip() == "":
                continue
            if "if" in line:
                indentation = len(line) - len(line.strip())
                if indentation <= 1:
                    if is_loop:
                        is_loop = False
                        assembly_line += f"JUMP Loop_{loop_counter}\n"
                is_if_block = True
                condition = line.strip().split(" ")[1:]
                jump_condition = ""
                op = ""
                second_operand = ""
                for i in relational_operators:
                    if i in condition:
                        op = i
                        jump_condition = relational_operators[i]
                if jump_condition == "":
                    sys.exit(1, "The if condition has an issue please check and write the program again") 
                if condition[2].strip().isdigit():
                    second_operand = condition[2].strip()
                else:
                    second_operand = getRegisterFor(condition[2].strip())
                assembly_line += f"if_block: "
                assembly_line += f"CMP {getRegisterFor(condition[0].strip())} , {second_operand} \n"
                assembly_line += f"{jump_condition} else_block \n"
                split_assembly = assembly_line.split("\n")
                for i in split_assembly:
                    hlc_to_assembly[i] = line
                content +=assembly_line
                continue
            if "else" in line:
                is_if_block = False
                is_else_block = True
                assembly_line += "else_block: "
                split_assembly = assembly_line.split("\n")
                for i in split_assembly:
                    hlc_to_assembly[i] = line
                content +=assembly_line
                continue
            if "while" in line:
                is_if_block = False
                is_else_block = False
                is_loop = True
                equation = line.split(" ")[1:]
                for i in relational_operators:
                    if i in line:
                        jump_condition = relational_operators[i]
                operand1 = equation[0].strip()
                operand2 = equation[2].strip()
                if operand1.isdigit() == False:
                    operand1 = getRegisterFor(operand1)
                if operand2.isdigit() == False:
                    operand2 = getRegisterFor(operand2)                        
                assembly_line += f"Loop_{loop_counter} : "
                assembly_line += f"CMP {operand1} , {operand2} \n"
                assembly_line += f"{jump_condition} END_WHILE \n"
                split_assembly = assembly_line.split("\n")
                for i in split_assembly:
                    hlc_to_assembly[i] = line
                content +=assembly_line
                continue
            if (is_if_block == True) or (is_else_block == True) or (is_loop == True):
                indentation = len(line) - len(line.strip())
                loop_condition = ""
                if indentation <= 1:
                    if is_if_block:
                        is_if_block = False
                        assembly_line += f"else_block:\n"
                    elif is_else_block:
                        is_else_block = False
                    elif is_loop:
                        loop_condition = f"JUMP Loop_{loop_counter}"
                        is_loop = False
                        assembly_line += loop_condition
                else:
                    assembly_line += generateAssembly(line)
            else:
                assembly_line += generateAssembly(line)
            split_assembly = assembly_line.split("\n")
            for i in split_assembly:
                hlc_to_assembly[i] = line
            content +=assembly_line
        if is_loop == True:
            content +=f"JUMP Loop_{loop_counter} \n END_WHILE:"
           
        return content

def setLabelAdress(line,address):
    if "Loop" in line or "if_block" in line or "else_block" in line or "END_WHILE" in line:
        if ":" in line:
            # line = line.split(":")[1].strip()
            label_address[line.split(":")[0].strip()] = address
def is_number(value):
    if value.startswith("-"):
        value = value[1:]
    if value.isdigit():
        return True
    return False

def getSignedValue(number):
    twos_comp = (1 << 8) + number
    return format(twos_comp,'x')
output = {"HLC instruction":[],"YMC address":[],"YMC assembly":[],
          "YMC ENCODING":[],"Modified Registers":[],"Modified flags":[]}
def assembly_encoding(line,address):

    ymc_encoding = ""
    hlc_code = ""
    modified_reg = ""
    modified_flags = ""
    output["YMC address"].append(address)
    output["YMC assembly"].append(line)
    for i in hlc_to_assembly:
        if line in i:
            hlc_code = hlc_to_assembly[i]
    output["HLC instruction"].append(hlc_code)
    if "Loop" in line or "if_block" in line or "else_block" in line:
        if ":" in line:
            line = line.split(":")[1].strip()
            # label_address[line.split(":")[0].strip()] = address
    line_split = line.split(" ")
    
    #Extracting OpCode
    operation = line_split[0]

    if operation.strip() == "":
        return operation
    operand1 = line_split[1]
    
    operation = instruction_set[operation]        
    if operation >= 8 and operation <= 11:
        if operand1 in label_address:
            operand2 = label_address[operand1]
        else:
            operand2 = ""
        operand2 = ""
    else:
        operand2 = line_split[3]
#############################################################
#           HANDLE YMC ASSIGNEMNTS
#############################################################
    if (operation >= 0 and operation <= 3):
        if "ptr" in operand1:
            variable = operand1.split("[")[1].split("]")[0]
            if variables_dictionary[variable]["type"].lower() == "signed":
                modified_flags += "S = 1 , "
            operand1 = variables_dictionary[variable]['address']
            reg1_code = variables_dictionary[variable]['address'] 
        elif operand1 in Registers:
            reg1_code = register_address[operand1] 
            operand1 = register_address[operand1]
        
        if "ptr" in operand2:
            variable = operand2.split("[")[1].split("]")[0]
            operand2 = variables_dictionary[variable]['address']
        elif is_number(operand2):
            operand2 = int(operand2)
            if operand2 < 0:
                operand2 = getSignedValue(operand2)
            else:
                operand2 = format(operand2,'x')
        elif operand2 in Registers:
            operand2 = register_address[operand2]
        
        reg2_code = operand2
        ymc_encoding += f"{format(operation,'x')} {operand1} {reg2_code}"
#########################################################################
#       HANDLE ARITHMETIC YMC INSTRUCTIONS
##########################################################################            
    elif operation >= 4 and operation <= 7:
        if operand1 in Registers and operand2 in Registers:
            # write code to put these registers in output
            modified_reg += f"{operand1} , {operand2}"
            # reg1_value = register_values[operand1]
            # reg2_value = register_values[operand2]
            reg1_code = register_address[operand1]
            reg2_code = register_address[operand2]
            operand2 = register_address[operand2]
        elif operand1 in Registers and is_number(operand2):
            # operand1 = register_address[operand1]
            reg_code = register_address[operand1]
            # reg_value = register_values[operand1]
            modified_reg += f"{operand1}"
            if int(operand2) < 0:
                operand2  = getSignedValue(int(operand2))
            else:
                operand2 = format(int(operand2),'x')
        ymc_encoding += f"{format(operation,'x')} {register_address[operand1]} {operand2}"
    elif operation >= 8 and operation <= 11:
        ymc_encoding += f"{format(operation,'x')} {operand2}"
    elif operation == 12:
        reg1_code = register_address[operand1]
        reg2_code = ""
        if operand2 in Registers:
            reg2_code = register_address[operand2]
        elif is_number(operand2):
            if int(operand2) < 0:
                reg2_code = getSignedValue(operand2)
            else:
                reg2_code = format(int(operand2),'x')
        ymc_encoding += f"{format(operation,'x')} {reg1_code} {reg2_code}"    
    output["Modified flags"].append(modified_flags)
    ymc_encoding = ymc_encoding.zfill(4)
    output["YMC ENCODING"].append(ymc_encoding)
    output["Modified Registers"].append(modified_reg)
    return f"{operation} || {operand1} || {operand2}" #line.split(" ")#format(operation,'x')
content = readFile("test.txt")
instruction_address = []
lines = content.split("\n")

for idx,line in enumerate(lines):
    instruction_address.append(m.setInstructionAddress(16))
    address = instruction_address[idx]
    setLabelAdress(line,address)
    
for idx,line in enumerate(lines):
    address = instruction_address[idx]
#    print(address,"====>",line,"===>",assembly_encoding(line,address))
    assembly_encoding(line,address)
print(variables_dictionary)
print(label_address)
print(hlc_to_assembly)
print(output)
def dict_to_csv(dictionary, filename):
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(zip(*values))

def dict_of_lists_to_csv(dictionary, filename, delimiter='|'):
    df = pd.DataFrame.from_dict(dictionary)
    df.to_csv(filename, sep=delimiter, index=False, quoting=csv.QUOTE_MINIMAL)


for i in output:
    if i not in ['YMC ENCODING','Modified Registers', 'Modified flags']:
        output[i] = output[i][:-1]
    print(i , len(output[i]))

dict_of_lists_to_csv(output,'ouptut.csv','|')