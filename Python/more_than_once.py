import random as rand
#this is a test
if __name__ == '__main__':
    #settup vars
    n = []
    occur_more_than_once = []

    for i in range(10):
        for j in range(rand.randint(0,5)):
            n.append(i)
    #We do this so that 0 is not counted each time
    last_int = ' '
    occur_more_than_once.append('start')

    for i in n:
        if i == last_int:
            #last var in occur_more_than_once
            if occur_more_than_once[-1] != i:
                occur_more_than_once.append(i)
        last_int = i
    occur_more_than_once.pop(0)
    print("Starting list: ", n, "\noccur_more_than_once: ", occur_more_than_once)
