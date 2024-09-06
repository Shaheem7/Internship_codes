import random 


listt = ["Buy", "Don't"]


# random.choice() method to select random
# element from the list
print(random.choice(listt))


# choose 10 times then print the result which came how many times
buy = 0
dont = 0
for i in range(100):
    if random.choice(listt) == "Buy":
        buy += 1
    else:
        dont += 1
        
print("Buy: ", buy)

print("Don't: ", dont)