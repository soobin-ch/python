from sympy.concrete.guess import guess

rst = 0

for i in range(1,100):
    if(i % 3 ==0):
        rst += i

print(rst)

rst2= 0

for i in range(1,100):
    if(i % 3 ==0 and  i % 2 != 0):
        rst2 += i
print(rst2)

rst3 =0
sign = -1

for i in range(1,100):
    rst3 += sign * i
    sign *= -1
print(rst3)


for i in range(1,5):
    for j in range(1,i+1):
        print('*',end='')
    print()


dan =2

print(f'{dan}단')
for i in range(1,9):
    print(f'{dan} x {i} = {dan * i}')

dan =5
print(f'{dan}단')
for i in range(1,9):
    print(f'{dan} x {i} = {dan * i}')




rst4 =0
for i in range(1,100):
    if i % 3 == 0 and i % 5 == 0:
       rst4 += i
print(rst4)


import random
answer = random.randint(1,10)

while True:
    guess = int(input('Guess a number: '))

    if guess == answer:
        print('Correct!')
        break

    else:
        if guess > answer:
            print('Incorrect! Guess lower.')
        else:
            print('Incorrect! Guess higher.')