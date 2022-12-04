from load_functions import load_text

# Import input as list
text_input = load_text(day=4)

# Split into ranges delimited by commas
ranges = [pair.split(',') for pair in text_input]

# For these ranges, convert into ints
range_int_list = []
for range_pair in ranges:
    int_result = []
    for r in range_pair:
        # Split each pair into individual numbers and append as list
        n_start, n_end = r.split('-')
        int_result.append([int(n_start), int(n_end)])
    range_int_list.append(int_result)

# For part 1, check how many encompassed ranges there are
pt1_result = 0
for pair in range_int_list:
    if (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]) or (pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1]):
        pt1_result += 1

print(f'Day 4 Part 1: {pt1_result}')


# For part 2, check how many ranges don't overlap at all
pt2_result = len(range_int_list)
for pair in range_int_list:
    if (pair[0][0] > pair[1][1]) or (pair[1][0] > pair[0][1]):
        pt2_result -= 1

print(f'Day 4 Part 2: {pt2_result}')