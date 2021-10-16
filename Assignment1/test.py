a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
b = [0, 1, 2, 3, 4, 5]


def improve_quality(array):
    winLength = 2
    maxSum = 0
    tarIndex = 0
    # print(max(1,2,3))
    # print(sum(array))
    for i in range(0, len(array)):
        curSum = sum(array[i:i+winLength])
        if(curSum>maxSum):
            maxSum = curSum
            tarIndex = i
        i = i + winLength
        # print(i, array[i])
    return tarIndex, maxSum

m,n = improve_quality(a)
print(m,n)