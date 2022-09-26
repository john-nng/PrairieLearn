from functools import reduce

#Helper library
def generate_values(variant_id, keeps):
    """
    Description: a helper function that generating parameters' values
                 based on variant id and parameter constrains (keeps).
    Input:
        variant_id: id of the variant.
        keeps: a list of constrains for each parameter.
    Output:
        return a list that contains the value of each parameter.
        also returns a number for total number of variants
    """
    result = []
    ranges = [len(k) for k in keeps]
    for i in range(len(keeps) - 1):
        ranges_product = reduce((lambda x, y: x * y), ranges[i+1:])
        result.append(keeps[i][(variant_id//ranges_product)%len(keeps[i])])
    result.append(keeps[-1][variant_id%ranges[-1]])
    n_variant = reduce((lambda x, y: x * y), [len(k) for k in keeps])
    return result, n_variant

#After using our library
def generate(data):
    paramValues, numOfVariants = generate_values(data['variant_number'],[range(3,5), range(10,12)])
    data['total_num_variants'] = numOfVariants
    # Put these two integers into data['params']
    data['params']['a'] = paramValues[0]
    data['params']['b'] = paramValues[1]
    # Compute the sum of these two integers
    c = paramValues[0] + paramValues[1]
    # Put the sum into data['correct_answers']
    data['correct_answers']['c'] = c
