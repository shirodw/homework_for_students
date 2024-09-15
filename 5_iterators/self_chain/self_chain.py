from itertools import cycle, batched, chain

my_dict = {
    "a": 1,
    "b": 2,
}

for i in cycle(my_dict):
    print(i)