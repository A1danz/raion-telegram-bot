def convert_cost(cost):
    count = 0
    result = cost
    for ind in range(len(result) - 1, -1, -1):
        if count == 3:
            result = result[:ind + 1] + "." + result[ind + 1:]
            count = 0
        count += 1
    return result

# 1.001.234
# 10.001.234

input = "12345623"
print(convert_cost(input))