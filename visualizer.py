#!/usr/bin/python3
# Written by Nikolay Budin, 2017

import time
import sys
import colorama

colorama.init()

"""
start: s
accept: ac
reject: rj
blank: _
s _ -> ac _ ^
s 0 -> a _ >
a 0 -> b _ >
b 0 -> a _ >
a _ -> rj _ ^
b _ -> ac _ ^

"""

name = sys.argv[1]
f_inp = sys.argv[2]
delay = 1
if (len(sys.argv) > 3):
    delay = float(sys.argv[3])

red = lambda s: colorama.Fore.RED + s + colorama.Style.RESET_ALL
green = lambda s: colorama.Fore.GREEN + s + colorama.Style.RESET_ALL
green_bright = lambda s: colorama.Fore.GREEN + colorama.Style.BRIGHT + s + colorama.Style.RESET_ALL

def get_dir(act):
    if (act == "<"):
        return -1
    if (act == "^"):
        return 0
    if (act == ">"):
        return 1

class jump:
    def __init__(self, state, symbol, act):
        self.state = state
        self.symbol = symbol
        self.act = act

    def __repr__(self):
        return '{%s, %s, %d}' % (self.state, self.symbol, self.act)

class tape:
    def __init__(self, tape_positive):
        self.tape_positive = tape_positive
        self.tape_negative = []
        self.pos = 0

    def __str__(self):
        cur_s = ' '
        for i in range(len(self.tape_negative) - 1, -1, -1):
            if -i - 1 == self.pos:
                cur_s += green_bright(self.tape_negative[i])
            else:
                cur_s += self.tape_negative[i]
            cur_s += ' '

        for i in range(len(self.tape_positive)):
            if i == self.pos:
                cur_s += green_bright(self.tape_positive[i])
            else:
                cur_s += self.tape_positive[i]
            cur_s += ' '
        return cur_s

def println(s):
    sys.stdout.write(s + '\n')

prog = open(name, 'r').read().split('\n')

accept = ''
reject = ''
cur = ''
blank = '_'

graph = {}

def read_config(prog):
    parse = lambda s: s[s.find(':') + 1:].strip()
    global cur, accept, reject, blank
    cur = parse(prog[0])
    accept = parse(prog[1])
    reject = parse(prog[2])
    blank = parse(prog[3])

read_config(prog)
n = int(prog[4])
prog = prog[5:]

for s in prog:
    if s.strip() != '':
        entry = s.split()
        begin_state = entry[0].strip()
        symbols = []
        for i in range(n):
            symbols.append(entry[i + 1].strip())
        state = entry[n + 2]
        entry = entry[n + 3:]
        link = []
        for i in range(0, 2 * n, 2):
            link.append(jump(state, entry[i], get_dir(entry[i + 1])))
        graph[tuple([begin_state] + symbols)] = link

inp = open(f_inp, 'r')

tapes = []
for i in range(n):
    tape_positive = inp.readline().split()
    if (len(tape_positive) == 0):
        tape_positive.append(blank)
    tapes.append(tape(tape_positive))

prev_l = [0 for i in range(n)]

while (True):
    lines = []
    for i in range(n):
        s = str(tapes[i])
        if len(s) < prev_l[i]:
            s += ' ' * (prev_l - len(s))
        prev_l[i] = len(s)
        lines.append(s)

    if cur == accept:
        println('\n' * (n + 1) + green('Accepted'))
        break
    if cur == reject:
        println('\n' * (n + 1) + red('Rejected'))
        break

    for tape in tapes:
        println(str(tape))
    println('current state: ' + cur)

    symbols = []
    for tape in tapes:
        symbols.append(tape.tape_positive[tape.pos] if tape.pos >= 0 else tape.tape_negative[-tape.pos - 1])

    if tuple([cur] + symbols) in graph:
        link = graph[tuple([cur] + symbols)]
        for i in range(n):
            tape = tapes[i]
            if tape.pos < 0:
                tape.tape_negative[-tape.pos - 1] = link[i].symbol
            else:
                tape.tape_positive[tape.pos] = link[i].symbol
            tape.pos += link[i].act
            if tape.pos < 0:
                if -tape.pos - 1 == len(tape.tape_negative):
                    tape.tape_negative.append(blank)
            else:
                if tape.pos == len(tape.tape_positive):
                    tape.tape_positive.append(blank)

        cur = link[0].state
    else:
        println('\n' + red('Failed, No edge by this symbol from current node, Rejected'))
        break

    time.sleep(delay)
    for i in range(n + 1):
        sys.stdout.write('\033[F')
    sys.stdout.write('\r')
