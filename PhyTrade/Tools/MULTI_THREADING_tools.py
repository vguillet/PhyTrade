
def multi_thread_loops(tasks, process,  max_worker_threads=8):
    import threading
    import queue

    # -- Create evaluation queue and fill with population lst
    evaluation_queue = queue.Queue(maxsize=len(tasks))
    for i in tasks:
        evaluation_queue.put_nowait(i)

    # -- Define worker function for multi-threading
    def worker():
        while True:
            item = evaluation_queue.get()
            process(item)
            print("Parameter set evaluation completed")
            evaluation_queue.task_done()

    # -- Initiate multi-threading process
    for i in range(max_worker_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    evaluation_queue.join()  # block until all tasks are done


