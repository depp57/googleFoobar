from fractions import Fraction

# This tutorial helped me a lot, very detailled and clear : 
# https://github.com/ivanseed/google-foobar-help/blob/master/challenges/doomsday_fuel/doomsday_fuel.md
# 
# It uses Absorbing markov chains to solve the problem.
# 
#     s0 s1 s2 s3 s4 s5
# s0 [0, 1, 0, 0, 0, 1]
# s1 [4, 0, 0, 3, 2, 0]
# s2 [0, 0, 0, 0, 0, 0]     Given this matrix.
# s3 [0, 0, 0, 0, 0, 0]
# s4 [0, 0, 0, 0, 0, 0]
# s5 [0, 0, 0, 0, 0, 0]
# 
# Step 1 : Order the matrix so that rows start with terminal states first. 
# 
#     s2 s3 s4 s5   s0 s1
# s2 [1, 0, 0, 0, | 0, 0]
# s3 [0, 1, 0, 0, | 0, 0]
# s4 [0, 0, 1, 0, | 0, 0]     I also added a 100% chance that the terminal state
# s5 [0, 0, 0, 1, | 0, 0]     will transform into itself in the next evolution.
#    --------------------
# s0 [0, 0, 0, 1, | 0, 1]
# s1 [0, 3, 2, 0, | 4, 0]
#          ^          ^
#          |          |
#          R          Q
#
# Step 2 : Extract R and Q sub matrices
#
# Step 3 : Calculate F = (I-Q)^-1
#
# Step 4 : Calculate FR = F * R
#
# Step 5 : Get the first line of FR, which contains the probabilities
#
# Step 6 : Find a common denominator, and return the solution

def shift(list, n):
    return list[-n:]+list[:-n]

def subtractMatrices(m_left, m_right):
    for line in range(len(m_left)):
        for col in range(len(m_left[line])):
            m_right[line][col] = m_left[line][col] - m_right[line][col]

def matrixProduct(a, b):
    zip_b = list(zip(*b))
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmList(L):
    a = L[0].denominator
    b = L[1].denominator
    current_lcm = lcm(a, b)
    for i in range(2, len(L)):
        current_lcm = lcm(current_lcm, L[i].denominator)
    
    return current_lcm

def transposeMat(m):
    return list(map(list, zip(*m)))

def subMat(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def determinantMat(m):
    #special case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*determinantMat(subMat(m,0,c))
    return determinant

def inverseMat(m):
    """Return the inverse of the matrix, using cofactors"""
    determinant = determinantMat(m)

    #special case for 1x1 matrix:
    if len(m) == 1:
        scalar = m[0][0]
        return [1/scalar if scalar != 0 else 0]

    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = subMat(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * determinantMat(minor))

        cofactors.append(cofactorRow)

    cofactors = transposeMat(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant

    return cofactors

def toStandardFormMarkov(m):
    for row_index, row in enumerate(m):
        row_sum = sum(m[row_index])
        if row_sum == 0:
            m[row_index][row_index] = 1
        else:
            for col_index, col in enumerate(row):
                m[row_index][col_index] = Fraction(col, row_sum)

def extractSubMat(m, rows, cols):
    new_matrix = []

    for row in rows:
        current_row = []
        for col in cols:
            current_row.append(m[row][col])
        new_matrix.append(current_row)
    return new_matrix

def identityMat(size):
    return [[1 if line == col else 0 for col in range(size)] for line in range(size)]


def solution(m):
    terminal_states = []
    non_terminal_states = []
    for line, row in enumerate(m):
        if sum(row) == 0:
            terminal_states.append(line)
        else:
            non_terminal_states.append(line)

    # ================== Edge case ==================

    # If there is only one terminal state, there is a 100% chance to end with it.
    if len(terminal_states) == 1:
        return [1, 1]

    # ================== Edge case ==================

    # Order the matrix so that rows start with terminal states first.
    toStandardFormMarkov(m)

    # Find R and Q
    R = extractSubMat(m, non_terminal_states, terminal_states)
    Q = extractSubMat(m, non_terminal_states, non_terminal_states)

    # Compute Q <-- (I-Q)
    I = identityMat(len(Q))
    subtractMatrices(I, Q)

    # Compute F <-- (I-Q)^-1
    F = inverseMat(Q)

    # FR <-- F*R
    FR = matrixProduct(F, R)

    probabilities = FR[0]

    lcm_p = lcmList(probabilities)
    probabilities = list(map(lambda p: p.numerator if p.denominator == lcm_p
    else p.numerator * (lcm_p // p.denominator), probabilities))

    probabilities.append(lcm_p)

    return probabilities
    

if __name__ == "__main__":
    print('Solution for test 1 :', solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]));

    print('Solution for test 2 :', solution([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]));
