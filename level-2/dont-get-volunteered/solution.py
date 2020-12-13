def solution(src, dest):
    return backTracking(src, dest, 0, float('inf'))


def backTracking(src, dest, currentMoves, minMoves):
    # Because, in the worst scenario, 6 moves are still sufficient
    if (src == dest or currentMoves == minMoves or currentMoves > 5):
        return currentMoves

    for move in L_MOVES:
        afterMove = moveTo(src, move)
        # If it's a valid move
        if (afterMove != -1):
            minMoves = min(minMoves, backTracking(afterMove, dest, currentMoves+1, minMoves))
        
    return minMoves  


def moveTo(src, move):
    arrayPos = [src % 8, int(src/8)]
    arrayPos[0] += move[0]
    arrayPos[1] += move[1]

    # Check if the position after the move is out ot the board
    if (isValid(arrayPos)):
        return arrayPos[0] + arrayPos[1] * 8
    else:
        return -1


def isValid(position):
    return 0 <= position[0] <= 7 and 0 <= position[1] <= 7


L_MOVES = [
    (-1, -2),
    (1, -2),
    (2, -1),
    (2, 1),
    (1, 2),
    (-1, 2),
    (-2, 1),
    (-2, -1)
]

if __name__ == "__main__":
    worstScenario = 0
    for i in range(64):
        for j in range(64):
            worstScenario = max(worstScenario, solution(i, j))
    print(f'moves required in the worst scenario : {worstScenario}')

    print(f'solution for 0 -> 45 : {solution(0, 45)}')
