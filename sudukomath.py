def solve(eq):
    solv = solv_empty(eq)
    if not solv:
        return True
    else:
        row, col = solv
    for i in range(1,10):
        if valid(eq, i, (row, col)):
            eq[row][col] = i
            if solve(eq):
                return True
            eq[row][col] = 0
    return False

def valid(eq, num, pos):
    # Check row
    for i in range(len(eq[0])):
        if eq[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(eq)):
        if eq[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if eq [i][j] == num and (i,j) != pos:
                return False
    return True

def print_board(eq):
    for i in range(len(eq)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(eq[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(eq[i][j])
            else:
                print(str(eq[i][j]) + " ", end="")

def solv_empty(eq):
    for i in range(len(eq)):
        for j in range(len(eq[0])):
            if eq[i][j] == 0:
                return (i, j)  # row, col
    return None
