rotation_state = [[1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1]]

core_matrix = [[0, 1, 0],
               [0, 2, 0],
               [0, 0, 0]]

line_matrix = [[0, 1, 0],
               [0, 1, 0],
               [0, 1, 0]]

angle_matrix =[[0, 1, 0],
               [1, 1, 0],
               [0, 0, 0]]

triple_matrix = [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]

cross_matrix = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]

empty = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

matrix_types = {
    0: empty,
    1: core_matrix,
    2: line_matrix,
    3: angle_matrix,
    4: triple_matrix,
    5: cross_matrix,
}