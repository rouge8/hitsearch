def initialize_authority(pages):
    return dict(zip(pages.keys(), [1]*len(pages)))

def initialize_L_matrices(pages):
    L_matrix = pages
    Lt_matrix = {}
    for page in pages:
        Lt_matrix[page] = []
    for page in pages:
        for link in pages[page]:
            Lt_matrix[link].append(page)
    return L_matrix, Lt_matrix

def multiply_matrix_vector(matrix, vector):
    result_matrix = {}
    for row in matrix:
        result_matrix[row] = 0
        for item in matrix[row]:
            result_matrix[row] += vector[item]
    return result_matrix        
            
def normalize(vector):
    max = 0
    for component in vector:
        if vector[component] > max:
            max = vector[component]
    for component in vector:
        vector[component] = float(vector[component]) / max
    return vector
        
def vector_difference(vector1, vector2):
    if not (vector1 and vector2): return float("inf")
    total = 0
    for component in vector1:
        total += abs(vector1[component] - vector2[component])
    return total        

def HITS(pages):
    authority_old = None
    authority = initialize_authority(pages)
    (L_matrix, Lt_matrix) = initialize_L_matrices(pages)
    while vector_difference(authority_old, authority) > 0:
        authority_old = authority
        hubbiness = normalize(multiply_matrix_vector(L_matrix, authority))
        authority = normalize(multiply_matrix_vector(Lt_matrix, hubbiness))
    return authority, hubbiness

def main():
    pages = {"a":["b", "c"], "b":["c"], "c":["b", "e"], "d":["b"], "e":["c"]}
    (authority, hubbiness) = HITS(pages)
    print authority
    print hubbiness

if __name__ == "__main__":
    main()