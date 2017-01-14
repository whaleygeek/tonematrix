let serialMessage = ""
let colsMax = 9
let cols = 8
let rowsMax = 9
let rows = 5
let currentRow = 0
let currentCol = 0
let BPM = 100
radio.setGroup(99)
basic.forever(() => {
    basic.showLeds(`
        # # # . .
        # . . # .
        # # # . .
        # . . # .
        # # # . .
        `)
})
control.inBackground(() => {
    basic.forever(() => {
        serialMessage = serial.readUntil(serial.delimiters(Delimiters.NewLine))
        if (serialMessage != "") {
            radio.sendString(serialMessage)
        }
    })
})
radio.onDataReceived(() => {
    serialMessage = radio.receiveString()
    if (serialMessage == "??") {
        radio.sendNumber(currentRow)
        basic.showNumber(currentRow)
        basic.pause(200)
        radio.sendNumber(currentCol)
        basic.showNumber(currentCol)
        currentCol += 1
        if (currentCol >= cols) {
            currentRow += 1
            if (currentRow >= rows) {
                currentRow = 0
            }
            currentCol = 0
        }
    } else {
        serial.writeLine(serialMessage)
        basic.showLeds(`
            # # # . .
            # . . # .
            # # # . .
            # . # . .
            # . . # .
            `)
    }
    basic.pause(100)
})
input.onButtonPressed(Button.B, () => {
    BPM += 5
    serial.writeValue("bpm", BPM)
    basic.showNumber(BPM)
})
input.onButtonPressed(Button.A, () => {
    BPM += -5
    serial.writeValue("bpm", BPM)
    basic.showNumber(BPM)
})
input.onPinPressed(TouchPin.P0, () => {
    rows += 1
    serial.writeValue("rows", rows)
    basic.showNumber(rows)
    if (rows >= rowsMax) {
        rows = 0
    }
})
input.onPinPressed(TouchPin.P1, () => {
    cols += 1
    serial.writeValue("cols", cols)
    basic.showNumber(cols)
    if (cols >= colsMax) {
        cols = 0
    }
})

