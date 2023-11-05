
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

A = [12, 1131, 13, 5, 6, 7, 541, 63]
 
two_pivot_quicksort_iterative(A, 1024)
print(A)