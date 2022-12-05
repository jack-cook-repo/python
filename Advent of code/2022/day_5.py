from load_functions import load_text
import copy
import re

# Import input as list
text_input = load_text(day=5)

# Parse inputs in 2 sections: stacks and movements
first_movement = 0
for i, line in enumerate(text_input):
    if line[:4] == 'move':
        first_movement = i
        break

# Split input
stacks_inputs = text_input[:first_movement-2]
movement_inputs = text_input[first_movement:]

# Parse stacks into lists
# Each stack letter is 3 characters, and has 1 space separating each letter
# So, we end up with 3n + (n-1) characters (4n - 1) in an input line, where n is the number of stacks 
n_stacks = int((len(stacks_inputs[0]) + 1) / 4)

stacks = {i+1: [] for i in range(n_stacks)}
for stack_row in stacks_inputs:
    for stack_num in stacks.keys():
        # Letters in format '[A] [B]' etc.
        # Want to move along by 4 each time, and take 2nd character in group
        letter = stack_row[4*(stack_num-1)+1]
        # If we have a letter, append it to our stack
        if letter != ' ':
            stacks[stack_num].append(letter)

# Parse movement commands
movements = [[int(n) for n in re.search(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)', movement).groups()] for movement in movement_inputs]


def move_crates(stacks, movements, crane_type):
    # Copy input dict
    output_stacks = copy.deepcopy(stacks)
    i = 1
    for movement in movements:
        (n_moved, from_stack, to_stack) = movement

        # Transfer crates from one stack to another
        if crane_type == 9000:
            moved_crates = list(reversed(output_stacks[from_stack][:n_moved]))
        elif crane_type == 9001:
            moved_crates = output_stacks[from_stack][:n_moved]
        output_stacks[to_stack] = moved_crates + output_stacks[to_stack]
        output_stacks[from_stack] = output_stacks[from_stack][n_moved:]
        i+=1
    return output_stacks


# Part 1
pt1_stacks = move_crates(stacks, movements, crane_type=9000)
print(f"Day 4, part 1: {''.join([stack[0] for stack in pt1_stacks.values()])}")

# Part 2
pt2_stacks = move_crates(stacks, movements, crane_type=9001)
print(f"Day 4, part 2: {''.join([stack[0] for stack in pt2_stacks.values()])}")