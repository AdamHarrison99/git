import random as rand


if __name__ == '__main__':

    n = []
    occur_more_than_once = []

    for i in range(10):
        for j in range(rand.randint(0,5)):
            n.append(i)

    last_int = ' '
    occur_more_than_once.append('start')

    for i in n:
        if i == last_int:
            if occur_more_than_once[-1] != i:
                occur_more_than_once.append(i)
        last_int = i
    occur_more_than_once.pop(0)
    print("Starting list: ", n, "\noccur_more_than_once: ", occur_more_than_once)
