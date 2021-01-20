# Project: Communication between Circuits

In this project you will explore how two circuits can communicate. You will first implement a simple protocol for sending a small number of binary values and debug it at low speeds using a direct electrical connection.  Next, you will speed up the communication 100 times and implement a higher-level layer for sending text messages.  Finally, you replace the direct electrical connection with a wireless infra-red connection.

## Build the Transmitter

In this project, you will use both M4: one to transmit and one to receive.  Only one M4 can be connected to the Mu editor at once, with convenient debugging with print statements, and the
other will be powered and running independently using a 9VDC supply.

Connect one M4 to the Mu editor and set it up to transmit using the following program:
```
import time
import array
import board
import digitalio

# Define the idle state during a period with no communication.
IDLE_VALUE = False
ACTIVE_VALUE = not IDLE_VALUE

# Define the duration of a single bit in seconds.
BIT_DURATION = 0.5
HALF_BIT_DURATION = BIT_DURATION / 2

# Define the length of a message in bits.
MSG_BITS = 4

# Minimum number of idle bits before a start bit.
MIN_IDLE_BITS = MSG_BITS + 1

# Configure the transmit digital output.
TX = digitalio.DigitalInOut(board.D1)
TX.direction = digitalio.Direction.OUTPUT
TX.value = IDLE_VALUE # Initially idle

# Initialize the internal red LED for diagnostics.
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT
LED.value = False # Initially off

while True:
    transmit([1,0,1,0])
```
Although this is a simple communication protcol, there are still a few things we need to specify:
 - What is the state of the "bus" (communication channel) when there is no activity?
 - What is the duration of each bit?
 - How many bits are sent together as a single message?
 - How is each message "framed", i.e. how can a receiver identify the start of a new message?

Study the code above and make a note of your answers to each question.

We use the on-board red LED (connected to D13) to monitor the transmitter. Note its activity when this program is running. Make sure you understand why the code produces the sequence of flashes you observe before proceeding to the next step of this project.

Untether your transmitter with the following steps:
 - Eject the CIRCUITPY usb drive from your computer.
 - Disconnect the USB cable at the M4.
 - Plug in the 9VDC to a wall socket and connect to your M4.
 - Make sure the DC_JACK switch is ON.

You should now see the red LED flashing the same sequence.

## Build the Receiver

Instead of writing a separate receiver program, we will add receiving capability to the transmitter program and re-use the same protocol specification.

Connect the second M4 to the USB cable and download the same transmitter program to get started. Check that the red LEDs on both M4s are flashing the same sequence (although not in synch with each other).

We first need to configure the receiver's digital input by adding these lines:
```
# Configure the receive digital input.
RX = digitalio.DigitalInOut(board.D0)
RX.direction = digitalio.Direction.INPUT
RX.pull = digitalio.Pull.UP if IDLE_VALUE else digitalio.Pull.DOWN # Idle when disconnected
```

Next, make the electrical connection that constitutes our "bus":
 - Connect the GND of one M4 to the GND of the other using a black jumper wire.
 - Connect the transmitter D1 (TX) to the receiver D0 (RX).
Note that we are using D0 and D1 for this project since these are already labeled RX and TX on the  M4 circuit board, but any pair of digital pins would work equally well.

Next, paste the following skeleton receive function:
```
def receive():
    # Allocate an efficient array of the received bits.
    bits_array = array.array('B', [0] * MSG_BITS)
    # Loop until we find a valid start bit.
    while True:
        # Wait for the bus to be idle.
        # ...
        print('idle start')
        # Wait for the minimum idle period.
        wait_until = time.time() + MIN_IDLE_BITS * BIT_DURATION
        # ...
        print('min idle completed')
        # Wait for a start bit.
        # ...
        print('got start bit')
        break
    # Delay for half a bit.
    time.sleep(HALF_BIT_DURATION)
    # Sample each bit at its nominal center time.
    for i in range(MSG_BITS):
        time.sleep(BIT_DURATION)
        bits_array[i] = (RX.value == ACTIVE_VALUE)
        print(bits_array[i])
    return bits_array
```
Why does the code sleep for a `HALF_BIT_DURATION` before sampling each bit of the message? You will need to fill in the three `...` sections before this code will work.  You will also need to change the main loop:
```
while True:
    # Uncomment the first line in the transmitter or the second in the receiver.
    #transmit([1,0,1,0])
    print(receive())
```

When your receiver code is working, you should see the following repeated sequence of print output in the Mu editor Serial window:
```
idle start
min idle completed
got start bit
1
0
1
0
array('B', [1, 0, 1, 0])
```

## Warp Speed

The protocol configuration we used above is deliberately slow to allow individual bits to be traced with the red LED and print output.

Now, speed up your code 100 times by setting:
```
BIT_DURATION = 0.005
```
Also, double the message size, to a "byte" or 8 bits, since this is convenient for later adding higher-level protocol layers:
```
MSG_BITS = 8
```
Finally, remove (or comment out) the `print` calls in your `receive` function (since they would
slow us down now) and update the main loop:
```
while True:
    # Uncomment the first line in the transmitter or the second in the receiver.
    transmit([1,0,1,0,0,1,1,0]); time.sleep(1)
    #print(receive())
```

After you download this code, your slow receiver is now a fast transmitter. Note the different
sequence of red LED flashes.  Although this protocol transmits each message 100 times faster, we added a one second delay between messages in the main loop so you can distinguish see individual messages.

Repeat the untethering steps above to power your fast transmitter from the 9VDC supply. Connect the second M4 (the original slow transmitter) to usb and download the same program with one change to make it a fast receiver:
```
while True:
    # Uncomment the first line in the transmitter or the second in the receiver.
    #transmit([1,0,1,0,0,1,1,0]); time.sleep(1)
    print(receive())
```
Since you are swapping the transmitter and receiver roles, you will also need to rewire the jumper wire connecting TX to RX (by swapping D0 and D1 at each M4).

You should now see this print output repeated in the Mu editor serial window:
```
array('B', [1, 0, 1, 0, 0, 1, 1, 0])
```
In case you don't see this, close and re-open the serial window then double check your code and connections.  If the high speed protocol is still not working, you may have discovered a flaw
in your receiver code that only affects high-speed operation.  To test this theory, try
different speeds by changing `BIT_DURATION`.  Remember that you need to update both the receiver and transmitter whenever you make a change to the protocol parameters.

## Another Layer

## Wireless

Although the term "wireless" usually implies communication via electromagnetic waves with wavelengths measured in centimeters (microwaves), this is just one of many non-electrical channels available. We will use infrared radiation with a wavelength of about 1 micron, but you could also use sound waves, etc.

To establish our wireless "bus", we will point a pair of IR transmit-receive pairs at each other on the breadboard:
![IR bus circuit](https://raw.githubusercontent.com/dkirkby/E4S/main/projects/img/IRbus.jpg)

Note that there is no longer any direct electrical connection between the M4s (not even a common ground).  The transmitter's TX now drives the IR LED of one pair (through a 1K series resistor) and the receiver's RX listens to the IR phototransistor of the other pair (using an internal pull-up resistor).

Before building this circuit, you will need to carefully bend the leads of each IR pair following these steps:
![IR lead bending](https://raw.githubusercontent.com/dkirkby/E4S/main/projects/img/IRleads.jpg)

Here is a closeup of one IR pair inserted into the breadboard, with green labels identifying which rows of the breadboard are connected to the GND, RX and TX of the IR pair, and green arrows showing the locations of the IR sensor and emitter:
![IR pair closeup](https://raw.githubusercontent.com/dkirkby/E4S/main/projects/img/IRcloseup.jpg)

Going wireless does not require any changes to your transmitter code, but there is a simple change required for the receiver:
```
IDLE_VALUE = True
```
Why is this change required and why does the protocol work when the transmitter and receiver have different defintions of the idle state?

Check that your wireless setup gives the same results as your previous wired setup.

Verify that blocking the light path between the IR pairs suspends the communication (but note that you will need a lot more than a sheet of paper to block this relatively bright emitter).
