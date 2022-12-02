from load_functions import load_text

# Import input as list
text_input = load_text(day=2)

# Convert to pairs of letters
pair_input = [line.split(' ') for line in text_input]

# Map to rock/paper/scissors for part 1
map_inputs_pt1 = {
	'A': 'R',
	'X': 'R',
	'B': 'P',
	'Y': 'P',
	'C': 'S',
	'Z': 'S',
	}
pair_input_mapped_pt1 = [[map_inputs_pt1[a], map_inputs_pt1[b]] for [a, b] in pair_input]


def outcome(first, second):

	# Draw worth 3
	if first == second:
		return 3
	# Win worth 6
	elif (first == 'R' and second == 'P') or (first == 'P' and second == 'S') or (first == 'S' and second == 'R'):
		return 6
	# Loss worth nothing
	else:
		return 0


def round_score(input_pair):
	opp, you = input_pair
	score = 0

	# Add outcome score
	score += outcome(opp, you)

	# Add shape score
	score += {'R': 1, 'P':2 , 'S':3}[you]

	return score


# Apply logic to every pair of games for part 1
print(f'Day 2 Part 1: {sum(list(map(round_score, pair_input_mapped_pt1)))}')


# Define win/loss for part 2
map_inputs_pt2 = {
	'R': ['S', 'P'],
	'P': ['R', 'S'],
	'S': ['P', 'R'],
	}

# Keep first (opponent's) draw from part 1, but map your draw according to whether we need to draw/lose/win
pair_input_opp_draw_mapped = [[map_inputs_pt1[a], b] for [a, b] in pair_input]
pair_input_mapped_pt2 = [[a, a if b == 'Y' else map_inputs_pt2[a][0 if b == 'X' else 1]] for [a, b] in pair_input_opp_draw_mapped]

# Apply logic to every pair of games for part 1
print(f'Day 2 Part 2: {sum(list(map(round_score, pair_input_mapped_pt2)))}')