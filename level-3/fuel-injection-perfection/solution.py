#   SOLUTION THAT PASS ALL TESTS

def solution(n):
    moves = 0
    n = int(n)
    while (n != 1):
        if (n % 2 == 0):
            moves += 1
            n //= 2
        else:
            moves += 2
            n = deepSearch(n)
        
    return moves


def deepSearch(n):
    n1 = (n - 1) / 2
    if (n1 % 2 == 0 or n1 == 1):
        return n1
    
    return (n + 1) / 2


# THIS SOLUTION DOESN'T PASS ALL TESTS, BECAUSE POOR PERFORMANCE

def solution2(n):
    return backTracking(int(n), 0, float('inf'))


def backTracking(n, currentMoves, minMoves):
    if (n == 1 or currentMoves == minMoves):
        return currentMoves
    
    for move in getMoves(n):
        minMoves = min(minMoves, backTracking(move, currentMoves+1, minMoves))

    return minMoves


def getMoves(n):
    moves = [
        n-1,
        n+1,
    ]
    if (n & 1 == 0):
        moves.append(n//2)

    return moves


if __name__ == "__main__":
    print(f'solution for 15 -> {solution(15)}')