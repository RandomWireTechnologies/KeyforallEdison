import kwikset

kwikset.setup_serial()

kwikset.setup_arduinobreakout_pins()

if(input("What do you want to do?") == "lock"):
    kwikset.lock()
else:
    kwikset.unlock()