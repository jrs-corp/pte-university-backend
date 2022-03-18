# from playsound import playsound
# playsound('song2.mp3')

marks = 0

actual_answer = 1887
print('\n'*30) # # To clear the screen
sample_answer = input("in recording, when was eifel tower created?")
if actual_answer == int(sample_answer):
    print('Right')
    marks += 1
else:
    print('Wrong')

actual_answer2 = 1387
print('\n'*30) # # To clear the screen
sample_answer2 = input("eifel tower was created by whom?")
if actual_answer2 == int(sample_answer2):
    print('Right')
    marks +=1
else:
    print('Wrong')

print('Your final marks is: ', marks)