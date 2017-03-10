data = list(map(lambda x: int(x), input().split(" ")))

prev = data[0]
for i in data[1:]:
    if i < prev:
        print(data)
        break
    else:
        prev = i
else:
    print("OK")
