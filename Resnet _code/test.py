import numpy as np

# Define the initial matrix
# matrix = np.array([
#     [0, 10000, 6000, 0],
#     [500, 0, 0, 1000],
#     [6000, 0, 0, 100],
#     [0, 500, 200, 0]
# ])

matrix = np.array([
    [0, 2, 200, 2],
    [2, 0, 0, 40],
    [150, 0, 0, 80],
    [2, 80, 40, 0]
])

# Define the distance matrix D for the given matrix size
def calculate_distance_matrix(size):
    """
    Create the distance matrix D based on the squared distance from the main diagonal.
    """
    D = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            D[i, j] = (i - j) ** 2
    return D

# Redefine the cost metric (cm) function to incorporate the distance matrix
def cm_with_distance(matrix, distance_matrix):
    """
    Calculate the cluster measure (cm) based on the given matrix and distance matrix.
    """
    return np.sum(matrix * distance_matrix)

# Updated optimization algorithm with the new cm calculation
def optimize_matrix_with_distance(matrix):
    number_of_blocks = matrix.shape[0]
    distance_matrix = calculate_distance_matrix(number_of_blocks)
    current_cm = cm_with_distance(matrix, distance_matrix)

    print("current_cm:", current_cm)

    for i in range(number_of_blocks - 1):
        for j in range(i, number_of_blocks):
            # Swap rows i and j
            matrix[[i, j], :] = matrix[[j, i], :]
            # Swap columns i and j
            matrix[:, [i, j]] = matrix[:, [j, i]]

            new_cm = cm_with_distance(matrix, distance_matrix)

            if new_cm < current_cm:
                current_cm = new_cm  # Keep the new matrix
            else:
                # Swap back if no improvement
                matrix[[i, j], :] = matrix[[j, i], :]
                matrix[:, [i, j]] = matrix[:, [j, i]]

    return matrix, current_cm

# Apply the updated optimization algorithm
optimized_matrix, final_cm = optimize_matrix_with_distance(matrix)

# Output the results
print("Optimized Pivoted Data Transfer Matrix:")
print(optimized_matrix)
print("\nOptimal cm value:")
print(final_cm)
