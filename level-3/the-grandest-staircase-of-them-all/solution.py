def solution(n):
    # Uses https://en.wikipedia.org/wiki/Memoization to improve performance
    # Because same values are retrieved multiple times.
    memoization = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
    
    return staircase(1, n, memoization) - 1


def staircase(height, left, memoization):
    if memoization[height][left] != 0:
        return memoization[height][left]
    if left == 0:
        return 1
    if left < height:
        return 0

    memoization[height][left] = staircase(height + 1, left - height, memoization) + staircase(height + 1, left, memoization)
    
    return memoization[height][left]


if __name__ == "__main__":
    print(f'Solution for 200 -> {solution(200)}')
