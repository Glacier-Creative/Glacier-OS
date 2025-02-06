# Glacier-OS
Open-source, highly portable mobile OS

## About the Glacier Communicator
The Glacier Communicator (better name pending) is my second attempt at building an open-source mobile phone. It features a 2.7" E-Paper display, a 4G modem, 12-button keypad with 4 
function keys, and currently exists as a messy (but nearly fully functional!) mess of glued-together dev boards on my desk.

### Hardware Roadmap
- Development boards << Complete
- Custom development board (singular) << In progress
- Phone-shaped object
- Phone

### Hardware Goal
The goal is to have the device be fully modular, with the CPU, modem, and human interface portions of the phone separated from one another. The current vision is to have daughterboards for the modem and CPU attach to one "I/O Board" with the screen, keypad, battery, and case. The I/O board and modem board will both feature SPI ROM chips to store hardware information.

### What to Expect
I am designing this phone very specifically to serve as a communication device. I'm intentionally sacrificing the ability to have certain features (for example, voice memos or music playback) to gain the modularity that will hopefully keep these devices usable for *decades*. As much as I'd love to just make a "do everything" pocket computer, that will unfortunately have to come later. 

If this first device works out how I'm planning, going from a dumb phone to a feature phone won't be a new device - it'll be an upgrade card you can install yourself in a matter of minutes.

## About this software
This software is written in MicroPython. While this does unfortunately lose a lot of perfomance compared to raw C, this does have benefits. It's easier for me (and any potential contributors) to work on functionality without wasting time working on low-level code (which, quite frankly, I'm mediocre at) and it makes the modularity goal much easier to achieve. The end goal is to have drivers on each module's SPI ROM chips so any module that follows the set standard will be able to work with any combination of other hardware - Python makes this quite easy to achieve *and* makes them naturally cross-platform. 

### Road to Beta
The following core features are not yet implemented (but most have the core underlying components in place):
- Triple-Click keypad input
- Dialer
- Messages
- Contacts

The following core features are mostly implemented and require only minor work:
- Cellular driver (Calls and SMS work great, but the modem can get out of sync with the OS)
- E-Paper driver (Works great, but more modern panels support partial refresh and will be needed for a better experience)
- Hardware keypad (Works great, but debouncing is not implemented)
