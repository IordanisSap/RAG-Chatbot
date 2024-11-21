def call_in_batches(func, array, batch_size=1):
    result = []
    for i in range(0, len(array), batch_size):
        batch = array[i:i + batch_size]
        tmp = func(batch)
        result.extend(tmp)
        print(f"({min((i+batch_size), len(array))}/{len(array)})")
    return result

