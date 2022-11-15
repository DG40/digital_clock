# Use the class for the DS1302 RTC chip.
import RTC_DS1302
import time
import cv2
import numpy as np

from rpi_ws281x import *
from variables import order, clear, d0, d1, d2, d3, d4, d5, d6, d7, d8, d9

# Create an instance of the RTC class.
ThisRTC = RTC_DS1302.RTC_DS1302()

# LED strip configuration:
LED_COUNT      = 4096      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812W_STRIP
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)


# Variables:
DateTime = { "Year":0, "Month":0, "Day":0, "DayOfWeek":0, "Hour":0, "Minute":0, "Second":0 }
Time = []
TimeLast = []
Hours = 0
Minutes = 0
Seconds = 0
pxls = [[(0, 0, 0) for y in range(32)] for x in range(32)]
boolpxls = [[False for y in range(32)] for x in range(32)] # Black/White
	

# Functions:

def printleds():
	for i in range(32):
		for j in range(32):
			strip.setPixelColor(order[i*32+j], Color(pxls[i][j][0], pxls[i][j][1], pxls[i][j][2], 0))
	strip.show()

def checktime():
	Data = ThisRTC.ReadRAM()
	Data = ThisRTC.ReadDateTime(DateTime)
	num_list = []
	num = ''
	for char in Data:
		if char.isdigit():
			num = num + char
		else:
			if num != '':
				num_list.append((num))
				num = ''
	if num != '':
		num_list.append((num))
	return num_list


def setsymbol(symbol, startX, startY):
	for i in range(7):
		for j in range(6):
			if symbol[i][j] == 0:
				boolpxls[startX+i][startY+j] = False # black
			else:
				boolpxls[startX+i][startY+j] = True # white

def SetTimeOnPxls(time):
	
	setsymbol(DigitCase(int(time[3][0])), 2, 9)	# H
	setsymbol(DigitCase(int(time[3][1])), 2, 17) # H
	setsymbol(DigitCase(int(time[4][0])), 12, 9) # M
	setsymbol(DigitCase(int(time[4][1])), 12, 17) # M
	setsymbol(DigitCase(int(time[5][0])), 22, 9) # S
	setsymbol(DigitCase(int(time[5][1])), 22, 17) # S
	
	boolpxls[1][6] = 1
	boolpxls[1][26] = 1
	boolpxls[29][6] = 1
	boolpxls[29][26] = 1
	
	boolpxls[1][7] = 1
	boolpxls[1][25] = 1
	boolpxls[29][7] = 1
	boolpxls[29][25] = 1
	
	boolpxls[2][6] = 1
	boolpxls[2][26] = 1
	boolpxls[28][6] = 1
	boolpxls[28][26] = 1

def DigitCase(digit):
	if digit == 0:
		paint = d0
	if digit == 1:
		paint = d1
	if digit == 2:
		paint = d2
	if digit == 3:
		paint = d3
	if digit == 4:
		paint = d4
	if digit == 5:
		paint = d5
	if digit == 6:
		paint = d6
	if digit == 7:
		paint = d7
	if digit == 8:
		paint = d8
	if digit == 9:
		paint = d9
	return paint


# Main program logic follows:

if __name__ == '__main__':
	print ('Press Ctrl-C to quit.')
	
	# Intialize the library (must be called once before other functions).
	strip.begin()

	while True:
		Time = checktime()
		
		
		if Time != TimeLast:
			
			Hours = int(Time[3][0]+Time[3][1])
			Minutes = int(Time[4][0]+Time[4][1])
			Seconds = int(Time[5][0]+Time[5][1])
			print(Hours)
			print(Minutes)
			print(Seconds)
			print()
			
			TimeLast = Time
			SetTimeOnPxls(Time)	# (boolbpxl)
			for k in range(6):
				for i in range(32):
					for j in range(32):
						
						if k == 0:
						# IN SECONDS:
							# S < 30 sec:
							if Seconds < 30: 
								if boolpxls[i][j] == True:
									if Seconds < 18:
										pxls[i][j] = (255, 255, 255)
									if Seconds >= 18 and Seconds < 20:
										pxls[i][j] = (int(255*(20-Seconds)/2), int(255*(20-Seconds)/2), int(255*(20-Seconds)/2)) # Clock
								else:
									pxls[i][j] = (int(i*5*Seconds/30), 0, int(j*5*Seconds/30))	# Background
							
							# S > 30 sec:
							else:
								if boolpxls[i][j] == True:
									pxls[i][j] = (255, i*8, 0) # Clock
								else:
									pxls[i][j] = (int(i*5*(60-Seconds)/30), 0, int(j*5*(60-Seconds)/30))	# Background
								
						else:
						# BETWEEN SECONDS:	
							# S < 30 sec:
							if Seconds < 30: 
								if boolpxls[i][j] == True:
									if Seconds < 18:
										pxls[i][j] = (255, 255, 255)
									if Seconds >= 18 and Seconds < 20:
										pxls[i][j] = (int(255*(20-(Seconds+k/6))/2), int(255*(20-(Seconds+k/6))/2), int(255*(20-(Seconds+k/6))/2)) # Clock
										
									
								else:
									pxls[i][j] = (int(i*5*(Seconds+k/6)/30), 0, int(j*5*(Seconds+k/6)/30))	# Background
							
							# S > 30 sec:
							else:
								if boolpxls[i][j] == True:
									pxls[i][j] = (255, i*8, 0) # Clock
								else:
									pxls[i][j] = (int(i*5*(60-(Seconds+k/6))/30), 0, int(j*5*(60-(Seconds+k/6))/30))	# Background
							
						
				printleds()
				
				
