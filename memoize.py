

def memoize(f):
    memory = {}

    def inner(num):
        if num not in memory:
            memory[num] = f(num)
        return memory[num]

    return inner
