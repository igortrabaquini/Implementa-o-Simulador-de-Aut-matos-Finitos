import json
import csv
import time
from collections import defaultdict

class Transition:
    def __init__(self, from_state, read, to_state):
        self.from_state = from_state
        self.read = read
        self.to_state = to_state

def read_automaton(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    initial_state = data['initial']
    final_states = data['final']
    transitions = []
    
    for trans in data['transitions']:
        from_state = int(trans['from'])
        to_state = int(trans['to'])
        read = trans.get('read', '')
        transitions.append(Transition(from_state, read, to_state))
    
    return initial_state, final_states, transitions

def determine_automaton_type(transitions):
    has_epsilon = any(t.read == '' for t in transitions)
    if has_epsilon:
        return "AFND_E"
    
    transition_map = defaultdict(set)
    for t in transitions:
        key = (t.from_state, t.read)
        transition_map[key].add(t.to_state)
    
    if any(len(states) > 1 for states in transition_map.values()):
        return "AFND"
    else:
        return "AFD"

def run_AFD(word, initial_state, final_states, transitions):
    current_state = initial_state
    for symbol in word:
        found = False
        for t in transitions:
            if t.from_state == current_state and t.read == symbol:
                current_state = t.to_state
                found = True
                break
        if not found:
            return False
    return current_state in final_states

def run_AFND(word, initial_state, final_states, transitions):
    current_states = {initial_state}
    for symbol in word:
        next_states = set()
        for state in current_states:
            for t in transitions:
                if t.from_state == state and t.read == symbol:
                    next_states.add(t.to_state)
        current_states = next_states
        if not current_states:
            return False
    return any(state in final_states for state in current_states)

def epsilon_closure(state, transitions):
    closure = set()
    stack = [state]
    closure.add(state)
    
    while stack:
        current = stack.pop()
        for t in transitions:
            if t.from_state == current and t.read == '' and t.to_state not in closure:
                closure.add(t.to_state)
                stack.append(t.to_state)
    return closure

def run_AFND_E(word, initial_state, final_states, transitions):
    current_states = epsilon_closure(initial_state, transitions)
    for symbol in word:
        next_states = set()
        for state in current_states:
            for t in transitions:
                if t.from_state == state and t.read == symbol:
                    next_states.update(epsilon_closure(t.to_state, transitions))
        current_states = next_states
        if not current_states:
            return False
    return any(state in final_states for state in current_states)

def process_csv(input_csv, output_csv, automaton_type, initial_state, final_states, transitions):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')
        
        for row in reader:
            if len(row) != 2:
                continue
            
            word, expected = row
            start_time = time.time_ns()
            
            if automaton_type == "AFD":
                result = run_AFD(word, initial_state, final_states, transitions)
            elif automaton_type == "AFND":
                result = run_AFND(word, initial_state, final_states, transitions)
            else:
                result = run_AFND_E(word, initial_state, final_states, transitions)
            
            elapsed_time = time.time_ns() - start_time
            writer.writerow([word, expected, '1' if result else '0', elapsed_time])

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python simulador.py <automaton.json> <input.csv> <output.csv>")
        return
    
    automaton_file = sys.argv[1]
    input_csv = sys.argv[2]
    output_csv = sys.argv[3]
    
    initial_state, final_states, transitions = read_automaton(automaton_file)
    automaton_type = determine_automaton_type(transitions)
    process_csv(input_csv, output_csv, automaton_type, initial_state, final_states, transitions)

if __name__ == "__main__":
    main()