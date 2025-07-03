def nombres_pairs():
    n = 0
    while True:
        yield n
        n += 2

# Utilisation du générateur
gen = nombres_pairs()
for _ in range(5):
    print(next(gen))
