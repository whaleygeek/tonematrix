# Protocol Specification

Pi is responsible for sending the beats at the appropriate rate. It sends a column

Note a recent change, to make this easier to implement in PXT which has comparisons
but not positional indexing in strings

on radio rx:
        if string matches “A” + “,” + myX + “,” + myY + “1”
etc

# Changelog

0.2
* Add the provisioning section
* Change the format for row/column size changes to allow a blocks-only implementation in PXT
* Clarify rows and columsn mapping to music

# Message Format

## TxBit

1. State changes are sent via the radio.
2. State changes come in as acknowledgements (could re-send on timeout)
3. Beat syncs come in, and are processed by their column

### State Change

    TxBit sends: (only on change)

    C,{0-8},{0-8},(1,0)             state change message

    format:
        C,%d,%d,%d\n

### State Change Ack

    TxBit receives:

    If Pi receives a C message, acks with with

    A,{0-8},{0-8},(1,0)             ack state change message

    format:
        A,%d,%d,%d\n

### Beat Sync

    TxBit receives:
    
    B,NN
    
    format:
        B,%d\n


## BRIDGEBIT

1. Sends all incoming radio messages over serial.
2. Sends all incomingserial messages over radio.
3. Buttons used to change grid size (send via serial)
4. Buttons used to change BPM (send via serial)

### Grid Size Change

    Bridge sends serial:
       rows:N
       or 
       cols:N

    format:
        {rows,cols},%d\n
        
### BPM Change

    Bridge sends serial:
        speed:N 
        
    format:
        speed,%d\n

N is in beats per minute

## PI

1. Handles grid size changes
2. Handles BPM changes
3. Handles state changes of TxBits, with acknowledgement
4. Generates beat timing
5. Generates chords on speaker
6. (Optionally) Handles provisiioning of micro:bits if they are turned on 1-by-1

### Grid size change

    Pi receives:
        S,NN,NN                         size of grid change

    format:
        S,%d,%d\n


### BPM Change

    Pi receives:
        T,NNN                           time in BPM

    format:
        T,%d\n

### State change

    Pi receives:
        C,NN,NN,N
        
    format:
        C,%d,%d,%d
        
    Pi transmits (ack)
        A,{0-8},{0-8},(1,0)             ack state change message

    format:
        A,%d,%d,%d\n

### Provisioning

    Pi receives:
    	"??"

    Pi response:
    	two separate messages, each just numbers, the next number in the grid to be filled
	X
	Y

    format:
    	%01d

# Grid to music mapping

Rows are pitch, columns are beats in a bar

# Provisioning flow

When a node micro:bit is first turned on, it sends "??" which is a request for the Pi to tell it
the next available slot in the grid.

If the Pi responds, it should respond with two messages, each a single character between 0-9.

The grid should fill up along the rows first, then down to the next column.


