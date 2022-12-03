from load_functions import load_text

# Import input as list
text_input = load_text(day=3)

# Split into compartments
compartments = []
for line in text_input:
    compartment_size = int(len(line)/2)
    compartments.append([line[:compartment_size], line[compartment_size:]])

# For each compartment, get overlapping letters
overlapping_letters = [list(set(comp1).intersection(set(comp2)))[0] for comp1, comp2 in compartments]

# Convert to unicode values, and then to priorities
# Unicode for uppercase letters starts from 65, and from 97 for lowercase
priority_values = [ord(letter) - (65-27 if letter.upper() == letter else 97-1) for letter in overlapping_letters]

print(f'Day 3 Part 1: {sum(priority_values)}')

# Get number of groups
groups = int(len(text_input) / 3)
results = []

for group in range(1, groups+1):
    # Put rucksacks into groups of 3
    group_rucksacks = text_input[group*3-3:group*3]

    # Find overlapping letter between the 3 rucksacks
    overlapping_letter = list(set(group_rucksacks[0]).intersection(group_rucksacks[1]).intersection(group_rucksacks[2]))[0]

    # Convert as above
    results.append(ord(overlapping_letter) - (65-27 if overlapping_letter.upper() == overlapping_letter else 97-1))

print(f'Day 3 Part 2: {sum(results)}')