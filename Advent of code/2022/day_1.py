from load_functions import load_text

# Import input as list
text_input = load_text(day=1)

results = []
sub_total = 0

for n in text_input:
	if n == '':
		results.append(sub_total)
		sub_total = 0
	else:
		sub_total += int(n)

# Add final number
results.append(sub_total)

print(f'Part 1 answer: {max(results)}')

# Sort
results_sorted = sorted(results)

print(f'Part 2 answer: {sum(results_sorted[-3:])}')