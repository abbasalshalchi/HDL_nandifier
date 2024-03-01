from re import *
path = "python hdl/Xor/Xor.hdl"  # put hdl input file path here
outputPath = "python hdl/Xor/"  # put hdl output file path here
# output will be presented in a file at the same directory as the input file and printed
# with input file in the console
file = open(path, "a+")
file.seek(0)
text = file.read()
tempVarSeed = 1


def not_to_nand(st):
    matches = finditer(r"Not.+;", st)
    for gate in matches:
        # print("reached" + str(gate))
        variables = [i[1: -1] for i in findall("=.+,|=.+[)]", gate.group())]
        replacement = "Nand(a={0}, b={0}, out={1});".format(*variables)
        st = sub(r"Not.+;", replacement, st, 1)
    return st


def or_to_nand(st):
    global tempVarSeed
    matches = finditer(r"Or.+;", st)
    for gate in matches:
        # print("reached" + str(gate))
        variables = [i[1: -1] for i in findall(r"=.?,|=.+[)]", gate.group())]
        print(variables + [tempVarSeed, tempVarSeed + 1])
        replacement = (
            """Nand(a={0}, b={0}, out=o{3});
    Nand(a={1}, b={1}, out=o{4});
    Nand(a=o{3}, b=o{4}, out={2});""".format(*variables + [tempVarSeed, tempVarSeed + 1]))
        st = sub(r"Or.+;", replacement, st, 1)
        tempVarSeed += 2
    return st


def and_to_nand(st):
    global tempVarSeed
    matches = finditer(r"And.+;", st)
    for gate in matches:
        # print("reached" + str(gate))
        variables = [i[1: -1] for i in findall(r"=.*?,|=.+[)]", gate.group())]
        print(variables + [tempVarSeed])
        replacement = (
            """Nand(a={0}, b={1}, out=o{3});
    Nand(a=o{3}, b=o{3}, out={2}); // made with python script by abbas atheel""".format(*variables + [tempVarSeed]))
        # - abbas atheel
        st = sub(r"And.+;", replacement, st, 1)
        tempVarSeed += 1
    return st

print("original: \n" + text)
print("\n_______________________________\nmade by python: \n\n" + and_to_nand(or_to_nand(not_to_nand(text))))


findChip = search(r'CHIP\s.*?\s', text).span()
findNameInChip = search(r'\s.*?\s', text[findChip[0]: findChip[1]]).span()
nameSpan = (findChip[0] + findNameInChip[0] + 1, findChip[0] + findNameInChip[1] - 1)
text = text[:nameSpan[0]] + text[nameSpan[0]:nameSpan[1]] + "PythonOutput" + text[nameSpan[1]:]
file = open(outputPath + str(text[nameSpan[0]:nameSpan[1]] + "PythonOutput.hdl"), "w+")
file.seek(0)
file.write(and_to_nand(or_to_nand(not_to_nand(text))))
# print(nandtext[nameSpan[0]:nameSpan[1]])




