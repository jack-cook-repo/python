def load_text(day):
    with open(f'day{day}_inputs.txt') as file:
        return [l.strip('\n') for l in file.readlines()]
