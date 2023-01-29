from fractions import Fraction


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def lcm(a, b):
    return int(abs(a * b) / gcd(a, b))


def lcm_array(arr, idx):
    if idx == len(arr) - 1:
        return arr[idx]
    a = arr[idx]
    b = lcm_array(arr, idx + 1)
    return lcm(a, b)


def multiply_matrices(a, b):
    c = []
    for i in range(0, len(a)):
        temp = []
        for j in range(0, len(b[0])):
            s = 0
            for k in range(0, len(a[0])):
                s += a[i][k] * b[k][j]
            temp.append(s)
        c.append(temp)
    return c


def transpose_matrix(m):
    return map(list, zip(*m))


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def get_matrix_determinant(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))
    return determinant


def get_matrix_inverse(m):
    # special case fox 1x1 matrix:
    if len(m) == 1:
        f = m[0][0]
        return [[Fraction(f.denominator, f.numerator)]]
    determinant = get_matrix_determinant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    # find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = get_matrix_minor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * get_matrix_determinant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose_matrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors


def get_transition_matrix(m):
    res = []
    n_states = len(m)
    state_counter = 0
    for row in m:
        denominator = sum(row)
        fraction_row = []
        if denominator != 0:  # transient state
            for entry in row:
                if entry != 0:
                    f = Fraction(entry, denominator)
                else:
                    f = 0
                fraction_row.append(f)
        else:  # terminal state
            fraction_row = [1 if x == state_counter else 0 for x in range(n_states)]
        res.append(fraction_row)
        state_counter = state_counter + 1
    return res


def get_transient_states(m):
    terminal_states = get_list_terminal_states(m)
    index_transient_states = [x for x in range(len(m)) if x not in terminal_states]
    res = []
    for s in range(len(m)):
        if s in index_transient_states:
            res.append(m[s])
    return res


def get_list_terminal_states(P):
    terminal_states = []
    state_idx = 0
    for state in P:
        if state[state_idx] == 1:
            terminal_states.append(state_idx)
        state_idx = state_idx + 1
    return terminal_states


def split_into_R_and_Q(P):
    number_states = len(P)
    T = get_transient_states(P)
    number_transient = len(T)
    number_terminal = number_states - number_transient
    R = []
    Q = []
    terminals = get_list_terminal_states(P)
    order = terminals + [x for x in range(0, number_states) if x not in terminals]
    for row in T:
        old_row = row[:]  # create a copy of row
        c = 0
        for idx in order:
            row[c] = old_row[idx]
            c = c + 1
        Q.append(row[number_terminal:])
        R.append(row[:number_terminal])
    return R, Q


def calculate_F(Q):
    # F = [I - Q]^(-1)
    # First calculate [I-Q]
    I_minus_Q = []
    i = 0
    for row in Q:
        new_row = []
        j = 0
        for entry in row:
            new_row.append(1 - entry if i == j else 0 - entry)
            j = j + 1
        i = i + 1
        I_minus_Q.append(new_row)
    # Calculate the inverse of [I-Q]
    inverse = get_matrix_inverse(I_minus_Q)
    return inverse


def solution(m):
    # s0 is starting and terminal state
    if len(m) == 1:
        return [1, 1]
    P = get_transition_matrix(get_transition_matrix(m))
    R, Q = split_into_R_and_Q(P)
    F = calculate_F(Q)
    FR = multiply_matrices(F, R)
    state_0 = FR[0]

    denominators = list(map(lambda frac: frac.denominator, state_0))
    common_denominator = lcm_array(denominators, 0)
    res = []
    for f in state_0:
        res.append(f.numerator * common_denominator // f.denominator)
    res.append(common_denominator)
    return res
