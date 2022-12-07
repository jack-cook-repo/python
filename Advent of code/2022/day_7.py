from load_functions import load_text
from collections import defaultdict

# Import input as list
text_input = load_text(day=7)

# List of directories and file sizes in each
directory_dict = defaultdict(int)
current_path = []

for line in text_input:
    # Command
    if line[0] == '$':
        command = line[2:]
        # Change directory
        if command[:2] == 'cd':
            directory = command.split()[1]

            if directory == '..':
                current_path.pop()
            else:

                current_path.append(directory)

    # Result of a list command
    else:
        # Check if directory contained within parent directory
        if line[:3] == 'dir':
            pass
        else:
            # Add file size to total
            file_size = int(line.split()[0])
            for l in range(len(current_path)):
                # Individual folder names may not be unique, so we need to record the whole path
                directory_dict[tuple(current_path[:l+1])] += file_size
    
# Return size of all directories with size <= 100,000
print(f'Day 7, Part 1: {sum(value for value in dict(directory_dict).values() if value <= 100000)}')

# Get smallest directory that could be deleted to provide 30,000,000 of free space
# The maximum space is 70,000,000

space_free = 7*10**7 - directory_dict[('/',)]
space_needed = 3*10**7 - space_free

smallest_key, smallest_value = '', 10**100
for key, value in directory_dict.items():
    if value >= space_needed and value <= smallest_value:
        smallest_key, smallest_value = key, value

# Return size of smallest directory we can delete to get to space needed
print(f'Day 7, Part 2: {directory_dict[smallest_key]}')

