let row = 0
let col = 0
let on_state = 99 // 99 means unset
let rxString = ""
let myIndex = "1,1"
let provisioning = 1
radio.setGroup(99)
radio.sendString("??")
radio.onDataReceived(() => {
    rxString = "test"
    if (rxString == "test") {
        serial.writeLine("test fired")
    }
    if (provisioning == 1) {
        row = strtonum(radio.receiveString())
        serial.writeNumber(row)
        provisioning += 1
    } else if (provisioning == 2) {
        col = strtonum(radio.receiveString())
        myIndex = row + "," + col
        on_state = 0
        provisioning = 0
    } else {
        rxString = radio.receiveString()
        serial.writeLine("--A," + row + "," + col + ",1")
        serial.writeLine(rxString)
        if (rxString == "B," + col + "\r") {
            playBeat()
        } else if (rxString == "A," + row + "," + col + ",1\r") {
            on_state = 1
        } else if (rxString == "A," + row + "," + col + ",0\r") {
            on_state = 0
        } else {
            serial.writeLine("no match")
        }
    }
})
basic.forever(() => {
    if (on_state == 1) {
        basic.showLeds(`
            . . . . .
            . # # # .
            . # # # .
            . # # # .
            . . . . .
            `)
    } else if (on_state == 0) {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            `)
    } else {
        basic.showLeds(`
            . # # # .
            . . . # .
            . . # # .
            . . . . .
            . . # . .
            `)
    }
})
input.onButtonPressed(Button.A, () => {
    //on_state = 0
    //radio.sendString("Off")
    sendUpdate(0)
})
input.onButtonPressed(Button.B, () => {
    //on_state = 1
    //radio.sendString("On")
    sendUpdate(1)
})
input.onPinPressed(TouchPin.P0, () => {
    on_state = 99;
    col += 1
    basic.showNumber(col)
    basic.pause(200)
})
input.onPinPressed(TouchPin.P1, () => {
    on_state = 99;
    row += 1
    basic.showNumber(row)
    basic.pause(200)
})
input.onPinPressed(TouchPin.P2, () => {
    on_state = 99;
    row = 0
    col = 0
    provisioning = 0
    basic.showNumber(0)
})
input.onShake(() => {
    //Toggle state
    if (on_state == 1) {
        sendUpdate(0)
    } else {
        sendUpdate(1)
    }
})
function playBeat() {
    serial.writeLine("Playing a beat!")
    if (on_state == 1) {
        basic.showLeds(`
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            `)
        basic.pause(100)
    } else if (on_state == 0) {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . # . .
            . . . . .
            . . . . .
            `)
        basic.pause(100)
    }
}
function sendUpdate(new_state = 0) {
    radio.sendString("C," + row + "," + col + "," + new_state)
}
function strtonum(str = "") {
    //Extremely naive string to number conversion. Hooray for <10.
    return (str.charCodeAt(0) - 48)
}
