#!/usr/bin/python3

from time import sleep
import pifacedigitalio

quitting = False
paused = False

# Toggle the speed (fast / slow)
def toggleSpeed(event):
	global delay
	if delay == 0.01:
		delay = 0.03
	else:
		delay = 0.01

# Toggle the pattern (Knight Rider / Supercollider)
def togglePattern(event):
	global pattern
	global leds
	if pattern == 0:
		pattern = 1
		leds = [0,1,2,3,4,5,6,7,6,5,4,3,2,1]
	else:
		pattern = 0
		leds = [0,7,1,6,2,5,3,4,2,5,1,6]

# Set the "quitting" flag
def setQuitting(event):
	global quitting
	quitting = True
	
# Toggle "paused" flag (pause / resume)
def togglePaused(event):
	global paused
	paused = not paused

# Entry point
if __name__ == "__main__":

	# Initialise the PiFace interface
	pifacedigitalio.init()
	pfd = pifacedigitalio.PiFaceDigital()

	# Set the speed and the LED pattern
	toggleSpeed(None)
	togglePattern(None)
	
	# Create button listeners
	listener = pifacedigitalio.InputEventListener()
	listener.register(0, pifacedigitalio.IODIR_ON, toggleSpeed)
	listener.register(1, pifacedigitalio.IODIR_ON, togglePattern)
	listener.register(2, pifacedigitalio.IODIR_ON, togglePaused)
	listener.register(3, pifacedigitalio.IODIR_ON, setQuitting)
	listener.activate()

	# Show help
	print("Piface demonstration")
	print("")
	print("Buttons:")
	print("  1. Change speed")
	print("  2. Change pattern")
	print("  3. Pause/resume")
	print("  4. Quit")
	
	# While "quitting" flag isn't set (see button 3 listener), loop
	while not quitting:
		# Loop over LED pattern
		for i in leds:
			# Turn on LED
			pfd.leds[i].turn_on()
			# Wait
			sleep(delay)
			# Turn off LED
			pfd.leds[i].turn_off()
			# Keep sleeping while "paused", but not "quitting"
			while paused and not quitting:
				sleep(0.05)
			# Leave the LED pattern loop immediately if "qutting"
			if quitting:
				break

	# Stop button listeners
	listener.deactivate()
	
	# End program			
	quit()
