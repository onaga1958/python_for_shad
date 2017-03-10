numbers = ['Ten', 'Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two', 'One', 'No']
one = "green bottle"
many = one + "s"
end = "hanging on the wall"

for i in range(len(numbers) - 1):
    s_1 = " {} {},".format(one if i == 9 else many, end)
    print(numbers[i] + s_1)
    print(numbers[i] + s_1)
    print("And if {} {} should accidentally fall,".format(numbers[-2].lower(), one))
    print("There'll be {} {} {}.".format(numbers[i + 1].lower(), one if i == 8 else many, end))
