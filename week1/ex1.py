#write a program to convert minutes into days, hours, and minutes
time = int(input("Enter minutes: "))
Days = time//1440
timeleft = time -(Days*1440)
Hours = timeleft//60
minleft = timeleft - (Hours*60)


print("Day: ",Days)
print("Hour: ",Hours)
print("Minutes: ",minleft)