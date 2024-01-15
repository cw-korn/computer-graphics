#write a program to find the maximum of numbers

max = 0
while True:
    i = int(input("Enter integer number: "))
    if (i>max):
        max = i
    elif (i==0):
        break

print ("Maximum number is ",max) 