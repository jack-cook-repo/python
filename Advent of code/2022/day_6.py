from load_functions import load_text

# Import input as list
text_input = load_text(day=6)

# Split to characters
char_input = list(text_input[0])

# Function to find start of packet
def get_start_of_packet(character_list, unique_chars):
	for i in range(unique_chars, len(char_input)+1):
		# Looks at trailing N unique characters from a point in the list
		# e.g. 4 unique characters starts at index 4, but scans indices 0:3 as "i" would be excluded from the slice
		characters = character_list[i-unique_chars:i]
		# Check that the set of characters is unique by converting to a set
		if sorted(list(set(characters))) == sorted(characters):
			return i

print(f'Day 6, Part 1: {get_start_of_packet(char_input, unique_chars=4)}')
print(f'Day 6, Part 2: {get_start_of_packet(char_input, unique_chars=14)}')