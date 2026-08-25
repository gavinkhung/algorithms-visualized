def push(array, value):
    n, s = array.n_elements, array.size_of_allocation
    if n == s:
        new_data = request region of size 2*(n+1)
        copy n elements from array.data into new_data
        release array.data; array.data = new_data
        array.size_of_allocation = 2*(n+1)
    array.data[n] = value
    array.n_elements = n + 1
