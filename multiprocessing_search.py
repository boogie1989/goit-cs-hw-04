import multiprocessing
import time


def search_in_file(file_path, keywords, queue):
    """Search for keywords in the specified file and send results to a multiprocessing queue."""
    result = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, "r") as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    result[keyword].append(file_path)
    except Exception as e:
        result['errors'] = f"Error reading file {file_path}: {e}"
    queue.put(result)


def multiprocess_file_search(file_paths, keywords):
    """Use multiple processes to search for keywords in a list of files."""
    processes = []
    queue = multiprocessing.Queue()
    result = {keyword: [] for keyword in keywords}
    result['errors'] = []

    for file_path in file_paths:
        process = multiprocessing.Process(
            target=search_in_file, args=(file_path, keywords, queue)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        partial_result = queue.get()
        for key in partial_result:
            if key == 'errors':
                result['errors'].append(partial_result[key])
            else:
                result[key].extend(partial_result[key])

    return result


if __name__ == "__main__":
    keywords = ["програми", "засобів"]
    file_paths = ["./files/file_1.txt", "./files/file_2.txt",
                  "./files/file_3.txt", "./files/file_4.txt", "./files/file_5.txt"]

    start_time = time.time()
    results = multiprocess_file_search(file_paths, keywords)
    end_time = time.time()

    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")
