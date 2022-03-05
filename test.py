'''
Over weeks and months, malnutrition can result in specific diseases, like anemia when people don't get enough iron or beriberi if they don't get adequate thiamine. A 
(Answer: severe) lack of food for a prolonged period — not enough calories of any sort to keep up with the body's energy needs — is starvation. The body's reserve resources are 
(Answer: depleted) .
'''


print('''
Over weeks and months, malnutrition can result in specific diseases, like anemia when people don't get enough iron or beriberi if they don't get adequate thiamine. A [1] (Answer: severe) lack of food for a prolonged period — not enough calories of any sort to keep up with the body's energy needs — is starvation. The body's reserve resources are [2] (Answer: depleted) .
''')

answer1 = input('Enter for question 1: ')
answer2 = input('Enter for question 2: ')

backend_answer1 = 'severe'
backend_answer2 = 'depleted'

points = 0
if answer1 == backend_answer1:
    points += 1
if answer2 == backend_answer2:
    points += 1

print('Your final marks is: ', points)

