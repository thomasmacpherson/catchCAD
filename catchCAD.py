import pifacecad
from time import sleep
from pifacecad.tools.question import LCDQuestion
cad = pifacecad.PiFaceCAD()

cad.lcd.backlight_on()
cad.lcd.cursor_off()
cad.lcd.blink_off()

limit_decrease = 50
time_floor = 60

playing = True
while playing:
	position = 2
	pressed = 0
	direction = 1
	time_limit = 500
	timer = 499
	score = 0
	cad.lcd.set_cursor(8,1)
	cad.lcd.write("+")

	gameOver = False

	while not gameOver:
		timer += 1
		if timer == time_limit:
			#time limit reached
			oldPosition = position
			position+=direction
			timer = 0
			if position == 8:
				# over target
				pressed = 0
				if time_limit > time_floor*2:
					time_limit -= limit_decrease
				else:
					time_limit = time_floor

			if (position == 9 and direction==1)or (position == 7 and direction==-1):
				# should've been pressed
				if not pressed:
					# but was not pressed
					gameOver = True
					break

			if position == 15:
				# hit right wall
				position == 14
				direction = -1
			
			elif position == -1:
				# hit left wall
				position = 1
				direction = 1
			cad.lcd.set_cursor(oldPosition,0)
			cad.lcd.write(" ")
			cad.lcd.set_cursor(position,0)
			cad.lcd.write("+")

		if cad.switches[0].value:
			# button pressed
			if position == 8:
				if not pressed:
					# pressed when over target
					pressed = 1
					score += 1
			else:
				# pressed when not over target
				gameOver = True
				break

	printString = "Game over, your score was: {score}".format(score=score)
	print(printString)
	cad.lcd.clear()
	cad.lcd.write("Game Over!")
	cad.lcd.set_cursor(0,1)
	cad.lcd.write("Your score: {score}".format(score=score))
	sleep(2)
	answers=["Yes","No"]
	question = LCDQuestion(question="Play again?", answers=answers)
	playing = question.ask()==answers.index("Yes")
	cad.lcd.clear()


