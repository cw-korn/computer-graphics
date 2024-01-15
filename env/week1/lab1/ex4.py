#write a program to find the average of numbers
sum = 0
count = 0
while True:
    i = int(input("Enter integer number: "))
    if i>=0:
        sum = sum + i
        count = count + 1
       
    else:
        avg = sum/count
        break

print("Average of %d/%d is %.2f" % (sum, count, avg))

