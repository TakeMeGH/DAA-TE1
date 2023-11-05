import random
import time
import sys
from memory_profiler import memory_usage
sys.setrecursionlimit(131072)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  
        L = arr[:mid]  
        R = arr[mid:]

        merge_sort(L)  
        merge_sort(R)  

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

#---------------------------------------------------------------

def median_of_three(a, low, high):
    mid = (low + high) // 2
    if a[low] > a[mid]:
        a[low], a[mid] = a[mid], a[low]
    if a[mid] > a[high]:
        a[mid], a[high] = a[high], a[mid]
    if a[low] > a[mid]:
        a[low], a[mid] = a[mid], a[low]
    return mid


def block_lomuto2(A, B, low, high):
    mid = median_of_three(A, low, high)
    A[low], A[mid] = A[mid], A[low]

    p = A[low]  
    q = A[high]  
    block = [0] * B
    i = low + 1 
    j = low + 1
    k = low + 1
    num_less_p = num_leq_q = 0

    while k < high:
        t = min(B, high - k)
        for c in range(t):
            block[num_leq_q] = c
            num_leq_q += q >= A[k + c]

        for c in range(num_leq_q):
            A[j + c], A[k + block[c]] = A[k + block[c]], A[j + c]

        k += t

        for c in range(num_leq_q):
            block[num_less_p] = c
            num_less_p += p > A[j + c]

        for c in range(num_less_p):
            A[i], A[j + block[c]] = A[j + block[c]], A[i]
            i += 1

        j += num_leq_q
        num_less_p = num_leq_q = 0

    A[i - 1], A[low] = A[low], A[i - 1]
    A[j], A[high] = A[high], A[j]

    return i - 1, j

def two_pivot_quicksort_iterative(A, B=100):
    high = len(A) - 1
    stack = [(0, high)]

    while stack:
        low, high = stack.pop()
        if low < high:
            i, j = block_lomuto2(A, B, low, high)
            
            if j < high:
                stack.append((j + 1, high))
            
            if i < j - 1:
                stack.append((i, j - 1))
            
            if low < i - 1:
                stack.append((low, i - 1))

#----------------------------------------

def generate_datasets():
    sizes = [(2**9, 'Small'), (2**13, 'Medium'), (2**16, 'Large')]
    conditions = ['sorted', 'random', 'reversed']
    datasets = {}
    for size, name in sizes:
        for condition in conditions:
            if condition == 'sorted':
                datasets[(name, condition)] = list(range(size))
            elif condition == 'random':
                datasets[(name, condition)] = random.sample(range(size), size)
            elif condition == 'reversed':
                datasets[(name, condition)] = list(range(size, 0, -1))
    return datasets

def benchmark(algorithm, arr):
    if algorithm == "two_pivot_quicksort":
        start_time = time.perf_counter()
        two_pivot_quicksort_iterative(arr, 1024)
        time_taken = time.perf_counter() - start_time
        mem_usage = memory_usage((two_pivot_quicksort_iterative, (arr, 1024)), interval=0.1, timeout=200)
        return max(mem_usage), time_taken * 1000, arr
    else:
        start_time = time.perf_counter()
        merge_sort(arr)
        time_taken = time.perf_counter() - start_time
        mem_usage = memory_usage((merge_sort, (arr, )), interval=0.1, timeout=200)
        return max(mem_usage), time_taken * 1000, arr
    


if __name__ == '__main__':
    datasets = generate_datasets()

    for (size, condition), dataset in datasets.items():
        print(f"Benchmarking {condition} dataset of {size} size.")

        dataset_ans = dataset[:]
        dataset_qs = dataset[:]
        dataset_2qs = dataset[:]

        answer = sorted(dataset_ans)
        
        mem_qs, time_qs, merge_result = benchmark("merge_sort", dataset_qs)

        mem_2qs, time_2qs, tp_result = benchmark("two_pivot_quicksort", dataset_2qs)

        print(f"Merge-Sort: Memory = {mem_qs} MiB, Time = {time_qs} ms")
        if answer == merge_result:
            print(f"Merge Sort Berhasil")
        else:
            print(f"Merge Sort Gagal")

        print(f"Two-Pivot Quicksort: Memory = {mem_2qs} MiB, Time = {time_2qs} ms")
        if answer == tp_result:
            print(f"Two-Pivot Quicksort Sort Berhasil")
        else:
            print(f"Two-Pivot Quicksort Sort Gagal")
        print("-" * 60)
