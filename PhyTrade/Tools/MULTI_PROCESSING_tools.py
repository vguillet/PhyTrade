
def multi_process_pool(population_lst, data_slice,  max_worker_processes=6):
    # -- Multi-process evaluation
    from multiprocessing import Pool

    def process_ind(individual):
        print("\n ----------------------------------------------")
        individual.gen_economic_model(data_slice)
        individual.perform_trade_run(data_slice)
        return individual

    print("======================> Start multiprocess")
    p = Pool(max_worker_processes)
    results = p.map(process_ind, population_lst)

    p.close()
    p.join()
    print("======================> Finish multiprocess")
    print(results)

    return results

    # p0 = Process(target=process, args=tasks)
    # p1 = Process(target=process, args=tasks)
    # p2 = Process(target=process, args=tasks)
    # p3 = Process(target=process, args=tasks)
    #
    # p0.start()
    # p1.start()
    # p2.start()
    # p2.start()
    #
    # p0.join()
    # p1.join()
    # p2.join()
    # p3.join()

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


