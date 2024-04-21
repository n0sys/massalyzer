import multiprocessing

def func1(queue):
    print("func1: starting")
    for i in range(10000000):
        pass

    queue.put(31)



def func2(queue):
    print("func2: starting")
    for i in range(10000000):
        pass

    queue.put(32)


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=func1, args=(queue, ))
    p1.start()
    p2 = multiprocessing.Process(target=func2, args=(queue, ))
    p2.start()
    p1.join()
    p2.join()
    queue.put()
    print(queue.get())
    print(queue.get())
    