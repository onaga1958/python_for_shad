def clip(sequence, min_value, max_value):
    result = []
    for value in sequence:
        clipped = min(max(value, min_value), max_value)
        result.append(clipped)
    return result

print clip([1, 2, 3, 4, 5], 0, 3)
print clip([1, -2, 3, -4, 5, -6], 0, 100)
