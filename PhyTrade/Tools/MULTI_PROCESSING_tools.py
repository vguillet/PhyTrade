
def multi_process_pool(tasks, process,  max_worker_processes=4):
    from multiprocessing import Process
    import time
    import os
    import queue

    p0 = Process(target=process, args=tasks)
    p1 = Process(target=process, args=tasks)
    p2 = Process(target=process, args=tasks)
    p3 = Process(target=process, args=tasks)

    p0.start()
    p1.start()
    p2.start()
    p2.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()

    # # -- Create evaluation queue and fill with population lst
    # evaluation_queue = queue.Queue(maxsize=len(tasks))
    # for i in tasks:
    #     evaluation_queue.put_nowait(i)
    #
    # # -- Define worker function for multi-processing
    # def worker():
    #     while True:
    #         item = evaluation_queue.get()
    #         Process(item)
    #         print("Parameter set evaluation completed")
    #         evaluation_queue.task_done()
    #
    # # -- Initiate multi-processing process
    # for i in range(max_worker_processes):
    #     t = Process(target=worker)
    #     t.start()


    # evaluation_queue.join()  # block until all tasks are done


