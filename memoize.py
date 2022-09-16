

def memoize(f):
    memory = {}

    def inner(num):
        if num not in memory or memory[num] is None:
            memory[num] = f(num)
        return memory[num]

    return inner
