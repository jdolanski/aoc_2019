from aocd import data


# part A
def rev():
    return lambda decksize, num: (- 1 - num) % decksize


def cut(N):
    return lambda decksize, num: (num - N) % decksize


def inc(N):
    return lambda decksize, num: (N * num) % decksize


def parse(commands):
    funcs = []
    for command in commands.split('\n'):
        if command == "deal into new stack":
            funcs.append(rev())
        elif command.startswith('cut'):
            funcs.append(cut(int(command.split(' ')[-1])))
        elif command.startswith('deal with increment'):
            funcs.append(inc(int(command.split(' ')[-1])))

    return funcs


n_cards = 10007
wanted_card = 2019
# wanted card is at its label's position before shuffling
pos = wanted_card
for func in parse(data):
    pos = func(n_cards, pos)

print("Part A", pos)

# part B


"""
functions can be defined as ax + b mod d
rev => -1*n -1 mod d    [a=-1, b=-1]
cut => 1*n - N mod d    [a=1, b=-N]
inc => N*n mod d        [a=N, b=0]

identity: (a mod n) mod n = a mod n
distribution:
        addition: (a + b) mod n = [(a mod n) + (b mod n)] mod n
        multiplication: ab mod n = [(a mod n)(b mod n)] mod n

COMPOSITIONS:
--------------------
rev(rev(num)) => -(-num-1 mod d)-1 mod d == num mod d (involution)
=> -((-num-1 mod d) + 1) mod d
=> -((-num-1 mod d) mod d + 1 mod d) mod d          distribution
=> -((-num-1) mod d + 1 mod d) mod d                identity
=> -(-num-1 + 1) mod d                              distribution
=> -(-num) mod d
=> num mod d or <-(-num -1) -1 mod d>
        a=-1, x=-num-1, b=-1

cut(cut(num, N), M) => ((num - N) mod d - M) mod d == cut(num, N+M) == n - (N + M) mod d
=> [ ((num - N) mod d) mod d + (-M mod d) ] mod d   distribution
=> [ (num - N) mod d + (-M) mod d ] mod d           identity
=> num - N - M mod d                                distribution
=> num - (N + M) mod d or <(num - N) - M mod d>
        a=1, x=num-N, b=-M

inc(inc(num, N), M) => M*inc(num, N) mod d => M*(N*num mod d) mod d
=> [(M mod d)*((N*num mod d) mod d)] mod d          distribution
=> [(M mod d)*(N*num mod d)] mod d                  identity
=> [M*N*num] mod d                                  distribution
=> <M*(N*num) mod d>
        a=M, x=N*num, b=0
--------------------
cut(rev(num), N)
=> rev(num) - N mod d
=> (((-num - 1) mod d) - N) mod d
=> [((-num - 1) mod d) mod d + (-N) mod d] mod d  distribution
=> [(-num - 1) mod d + (-N) mod d] mod d          identity
=> [-num - 1 - N] mod d                           distribution
=> <(-num - 1) - N mod d>
        a=1, x=-num-1, b=-N

inc(rev(num), N)
=> N*(rev(num)) mod d => N*(-num - 1 mod d) mod d
=> [(N mod d)*((-num - 1 mod d) mod d)] mod d       distribution
=> [(N mod d)*(-num - 1 mod d)] mod d               identity
=> <N*(-num - 1) mod d>                             distribution
        a=N, x=-num-1, b=0
--------------------
rev(cut(num, N))
=> -1*cut(num, N) - 1 mod d
=> -(num - N mod d) - 1 mod d
=> [(-(num - N mod d) mod d) + (-1 mod d)] mod d  distribution
=> [(-num + N mod d) + (-1 mod d)] mod d          identity
=> -num + N - 1 mod d                             distribution
=> <-(num - N) - 1 mod d>
        a=-1, x=num-N, b=-1

inc(cut(num, N), M)
=> M*cut(num, N) mod d => M*(num - N mod d) mod d
=> [(M mod d)*((num - N mod d) mod d)] mod d    distribution
=> [(M mod d)*(num - N mod d)] mod d            identity
=> <M*(num - N) mod d>                          distribution
        a=M, x=num-N, b=0
--------------------
rev(inc(num, N))
=> -1*inc(num, N) - 1 mod d => -1*(N*num mod d) - 1 mod d
=> [(-(N*num mod d) mod d) + (-1 mod d)] mod d  distribution
=> [(-N*num mod d) + (-1 mod d)] mod d          identity
=> -N*num - 1 mod d                             distribution
=> <-(N*num) - 1 mod d>
        a=-1, x=N*num, b=-1

cut(inc(num, N), M)
=> inc(num, N) - M mod d => (N*num mod d) - M mod d
=> [(N*num mod d) mod d + (-M) mod d] mod d     distribution
=> [N*num mod d + (-M) mod d] mod d             identity
=> <1*(N*num) - M mod d>                        distribution
        a=1, x=N*num, b=-M
--------------------
"""


def get_initial_shuffle_function(commands, d):
    """
    COMPOSITION FORMULA:
    f = ax + b mod d
    f.f => a1(a0x + b0) + b1 mod d => a1a0x + a1b0 + b1 mod d
        => a: a1a0x mod d, b: a1b0 + b1 mod d
    """
    a, b = 1, 0
    for command in commands.split('\n'):
        if command == "deal into new stack":
            a_n = -1
            b_n = -1
        elif command.startswith("cut"):
            N = int(command.split(' ')[-1])
            a_n = 1
            b_n = -N
        elif command.startswith("deal with increment"):
            N = int(command.split(' ')[-1])
            a_n = N
            b_n = 0

        a = (a_n*a) % d
        b = (a_n*b + b_n) % d

    return a, b


def get_shuffle_times_n(a, b, n, d):
    """
    COMPOSITION FORMULA:
    f = ax + b mod d
    f.f => a1(a0x+b0)+b1 mod d => a1a0x + a1b0 + b1 mod d, where a1=a0, b1=b0
        => x*a0^2 + a0b0 + b0 mod d => a: x*a0^2 mod d, b: b0*(a0 + 1) mod d
    f.f.f => a0(a0(a0x+b0)+b0)+b0 mod d => a0(x*a^2+a0b0+b0)+b0 mod d => x*a0^3 + a0^2*b0 + a0b0 + b0 mod d
        => a: x*a0^3 mod d, b: a0^2*b0 + a0b0 + b0 mod d => b: b0*(a0^2 + a0 + 1) mod d
    f n. f (n compositions)
        => a: x*a0^n mod d
        => b: b0*[(a0^n-1)/(a0-1)] mod d
            geometric series sum: a + ar + ar^2 + ... ar^(n-1) = a*((1 - r^n)/(1 - r))
            here a=1, r=a0, so 1 + 1*a0 + 1*a0^2 + ... 1*a0^(n-1) = 1*((1 - a0^n)/(1 - a0))
    """
    # powermod a0 to a0^n mod d
    pA = pow(a, n, d)
    # b0*(1 - a0^n)/(1 - a0) mod d
    # pB = (b*(1 - pow(a, n, d))/(1 - a)) % d
    # modular inverse exists iff a and m are relatively prime (gcd(a,m)=1).
    # modinv = pow(a, p-2, p)
    pB = (b*(1 - pA)*(pow(1 - a, d - 2, d))) % d

    return pA, pB


n_cards = 119315717514047
n_shuffles = 101741582076661
cardidx = 2020

# get initial a and b
a, b = get_initial_shuffle_function(data, n_cards)
pa, pb = get_shuffle_times_n(a, b, n_shuffles, n_cards)

# ax + b mod d
# cardpos = (pa*cardidx + pb) % n_cards
# print(cardpos)

# value of card at index 2020
# invert ax + b mod d => x/a - b/a mod d
#   with modinv => x*modinv(a) - b*modinv(a) mod d
#       => (x - b)*modinv(a) mod d => (x - b)*pow(a, d - 2, d) mod d
cardvalue = (cardidx - pb)*pow(pa, n_cards - 2, n_cards) % n_cards
print("Part B", cardvalue)
