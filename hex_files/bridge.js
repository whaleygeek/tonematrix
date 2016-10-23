let serialMessage = ""
let colsMax = 9
let cols = 8
let rowsMax = 9
let rows = 5
radio.setGroup(99)
	serial.writeLine("Hello, this is your bridge speaking")
	control.inBackground(() => {
		    basic.forever(() => {
			            serialMessage = serial.readUntil(serial.delimiters(Delimiters.NewLine))
			            radio.sendString(serialMessage)
			            serial.writeLine(serialMessage)
			        })
	})
input.onButtonPressed(Button.B, () => {
	    rows += 1
	    serial.writeValue("rows", rows)
	    basic.showNumber(rows)
	    if (rows >= rowsMax) {
		            rows = 0
	    }
})
input.onButtonPressed(Button.A, () => {
	    cols += 1
	    serial.writeValue("cols", cols)
	    basic.showNumber(cols)
	    if (cols >= colsMax) {
		            cols = 0
	    }
})
basic.forever(() => {
	    basic.showLeds(`
		            # # # . .
		            # . . # .
		            # # # . .
		            # . . # .
		            # # # . .
		            `)
})
radio.onDataReceived(() => {
	    serial.writeLine(radio.receiveString())
	    basic.showLeds(`
		            # # # . .
		            # . . # .
		            # # # . .
		            # . # . .
		            # . . # .
		            `)
	        basic.pause(100)
})

