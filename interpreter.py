import sys
import re

def gen(s, vars, repl_ind):
    result = []
    insert_ind = s.find('[')
    s = s[:insert_ind] + s[s.find(']') + 1:]
    for var in vars:
        line = s[:insert_ind] + var + s[insert_ind:]
        line = line.replace('%' + str(repl_ind), var)
        result.append(line)
    return result

def parse_string(s):
    groups = re.findall('\[(.*?)\]', s)
    t = [elem for elem in groups[0].split(',')]
    groups = list(map(lambda group: [elem.strip() for elem in group.split(',')], groups))
    result = [s]
    for i in range(len(groups)):
        group = groups[i]
        result = list(map(lambda line: gen(line, group, i + 1), result))
        result = [item for sublist in result for item in sublist]
    return result;

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('usage: <input_filename> [<output_filename>]')
    exit(0)

filein = open(sys.argv[1], 'r')

parsed = [] 
for line in filein.read().split('\n'):
    parsed += parse_string(line)

fileout = open(sys.argv[1] + '.out' if len(sys.argv) == 2 else sys.argv[2], 'w')
for line in parsed:
    fileout.write(line + '\n')
fileout.close()