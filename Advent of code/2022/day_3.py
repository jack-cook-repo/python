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

print(sum(priority_values))