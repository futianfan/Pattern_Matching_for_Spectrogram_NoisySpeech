import numpy as np 
from time import time
np.random.seed(1)
pi = np.pi 
#### generate sine curve: 
#### n => - pi / 2 * cos(1/T * x) + pi / 2   for x = 1,...,200
#### length is the length of sequence.
def generate_sine_sequence(T, length = 200):
    output = np.array(range(length)) + 1  #### 1,..., 200 
    output = -pi / 2 * np.cos(2 * pi * output / T) + pi / 2
    return output

### the function pi_abs
def pi_abs(x):
    assert x >= 0 and x <= 2 * pi
    if x > pi:
        x = 2 * pi - x
    return x

### vectorize the function pi_abs
pi_abs_vec = np.vectorize(pi_abs)

#### generate polyline curve:         *******polyline*******
def generate_polyline_sequence(T, length = 200):
    k = 2 * pi / T 
    n_seq = np.array(range(length)) + 1
    output = k * n_seq
    output = output % (2 * pi)
    output = pi_abs_vec(output)
    return output

#### search local maximum
def search_local_maximum(input_array):
    leng = input_array.shape
    leng = leng[0]
    input_array = input_array.reshape(leng,)
    index_list = []
    if input_array[0] > input_array[1]:
        index_list.append(0)
    for i in range(1,leng-1):
        if max(input_array[i], input_array[i - 1], input_array[i + 1]) == input_array[i]:
            index_list.append(i)
    if input_array[leng - 1] > input_array[leng - 2]:
        index_list.append(leng-1)
    return index_list


#### search maximum/minimum slope          *******polyline*******
def find_maximum_minimum_slope(input_array):
    leng = input_array.shape
    leng = leng[0]
    input_array = input_array.reshape(leng,)  
    minimum_v = np.inf
    maximum_v = 0
    for i in range(leng):
        slope = input_array[i] / (i + 1)
        if slope > maximum_v:
            maximum_v = slope
        if slope < minimum_v:
            minimum_v = slope 
    return 2 * pi / minimum_v, 2 * pi / maximum_v


#### traverse all the possible value
def search_all(input_array, stepsize = 0.01, search_type = 'sine'):
    leng = input_array.shape
    leng = leng[0]
    input_array = input_array.reshape(leng,)

    #### searching range
    if search_type == 'sine':
        local_maximum_list = search_local_maximum(input_array)
        max_T = 2 * local_maximum_list[-1]
        min_T = 2 * local_maximum_list[0]
    elif search_type == 'polyline':
        max_T, min_T = find_maximum_minimum_slope(input_array)
    #### searching range
    print('T ranges from ' + str(min_T) + ' to ' + str(leng * 2))
    ###T = max_T
    T = leng * 2 #### if max_T > T, polyline reduces to a line.
    minimum_error = np.inf 
    while T > min_T:
        ##print(T)
        ### compute the fitting error(L2 norm) of the proposal T, if the error decreases, then do the gradient descent. else break. 
        if search_type == 'sine':
            proposal_sequence = generate_sine_sequence(T, leng)
        elif search_type == 'polyline':
            proposal_sequence = generate_polyline_sequence(T,leng)
        error = np.sum((proposal_sequence - input_array)**2)  ### L2 error 
        if error <= minimum_error:
            optimal_n = T
            minimum_error = error
        T -= stepsize

    ####  here we fit the line, instead of polyline or sine. 
    ### an assumption is that the T is greater than 200 * 2.
    ### in this case, we use a straight line to fit the sequence. 
    n_seq = np.array(range(leng)) + 1
    kk = np.sum(input_array * n_seq) / np.sum(n_seq**2)
    proposal_sequence = kk * n_seq
    error = np.sum((input_array - proposal_sequence)**2)
    if error <= minimum_error:
        optimal_n = pi / kk * 2

    return optimal_n

def gradient_search(input_array, optimal_T, search_type = 'GD', step_size = 1e-2, max_iter = 100):
    ### search_type = 'GD' or "Newton"
    freq = 1.0 / optimal_T
    leng = input_array.shape
    leng = leng[0]
    n_seq = np.array(range(leng)) + 1
    if search_type == 'GD':
        for i in range(max_iter):
            ### compute the gradient of frequence for each data for i = 1,...,200
            f_grad = pi**2 * n_seq * ( (pi - 2 * input_array) * np.sin(2 * pi * n_seq * freq) - pi / 2 * np.sin(4 * pi * n_seq * freq) )
            ### sum up the gradient to a scalar
            f_grad = np.sum(f_grad)
            f0 = freq
            seq_0 = generate_sine_sequence(1.0/f0, leng)
            err_0 = np.sum((seq_0 - input_array)**2)
            freq -= step_size * f_grad
            seq = generate_sine_sequence(1.0/freq, leng)
            err = np.sum((seq - input_array)**2)
            print('new error is *****' + str(err) + '*****, old error is ******' + str(err_0) + '*****')
            if err > err_0:  ### check the error, if error increase, then we break. 
                return f0
            print(freq)
        return freq


def gradient_descent_polyline(input_array, optimal_T, search_type = 'GD', step_size = 1e-2, max_iter = 100):    
    freq = 1.0 / optimal_T
    leng = input_array.shape
    leng = leng[0]
    n_seq = np.array(range(leng)) + 1    
    if search_type == 'GD':
        for i in range(max_iter):
            T = 1.0 / freq 
            grad = 0
            for j in range(1,1+leng):  # 1,...,200
                C = int(j / T) * T
                m = j - C
                if m <= 0.5 * T:
                    ### y =  2pi / T * (x - C) = 2pi f * (x - C)
                    difference = 2 * pi * freq * (j - C) - input_array[j - 1]
                    grad += difference * 2 * pi * (j - C)
                else:
                    ### y = - 2 * pi / T * (x - C - T) = - 2 * pi * f * (x + C + T)
                    difference = - 2 * pi / T * (j - C - T) - input_array[j - 1]
                    grad += difference * (-2 * pi * (j - C - T))
            f0 = freq
            T = 1.0 / f0
            seq_0 = generate_polyline_sequence(T,leng)
            err_0 = np.sum((seq_0 - input_array)**2)
            freq -= step_size * grad
            T = 1.0 / freq
            seq = generate_polyline_sequence(T,leng)
            err = np.sum((seq - input_array)**2)
            print('new error is *****' + str(err) + '*****, old error is ******' + str(err_0) + '*****')
            if err >= err_0:
                return f0
        return freq 


def two_step(input_array, stepsize1, stepsize2 = 1e-5, max_iter = 100, search_type = 'sine', gradient_type = 'GD'):
    if search_type == 'sine':
        #### traverse all the possible value
        optimal_T = search_all(input_array, stepsize = stepsize1, search_type='sine')
        print(optimal_T)
        #### gradient descent 
        optimal_f = gradient_search(input_array, optimal_T = optimal_T, search_type = gradient_type, step_size = stepsize2, max_iter = max_iter )
        return 1.0 / optimal_f
    elif search_type == 'polyline':
        optimal_T = search_all(input_array, stepsize = stepsize1, search_type = 'polyline') 
        #### traverse all the possible value
        optimal_f = gradient_descent_polyline(input_array, optimal_T = optimal_T, search_type = gradient_type, step_size = stepsize2, max_iter = max_iter)
        #### gradient descent 
        return 1.0 / optimal_f

if __name__=='__main__':
    N = 200
    T0 = 12.3435
    #T0 = 36.8438
    #T0 = 473.23
    ##T0 = 1236.8438
    
    print('===========Evaluating sine curve==================')
    print('target T is ' + str(T0))
    ###y = -pi / 2 * np.cos(2 * pi * n_seq / T) + pi / 2
    y = generate_sine_sequence(T0, N)
    y *= 0.1
    t1 = time()
    T = two_step(y, stepsize1 = 1.0, stepsize2 = 1e-9,  max_iter = 50, search_type='sine', gradient_type = 'GD')
    t2 = time()
    str_time = '{:.2f}'.format(t2 - t1)
    print('search procedure cost ' + str_time + ' seconds. Estimated T is ' +  str(T), end = '\n\n')
    

    print('===========Evaluating polyline curve==================')
    print('target T is ' + str(T0))
    y = generate_polyline_sequence(T0, N)
    t1 = time()
    T = two_step(y, stepsize1 = 1e-1, stepsize2 = 1e-15,  max_iter = 100, search_type='polyline')
    t2 = time()
    str_time = '{:.2f}'.format(t2 - t1)
    print('search procedure cost ' + str_time + ' seconds. Estimated T is ' +  str(T))




