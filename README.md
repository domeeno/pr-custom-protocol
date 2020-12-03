## PR-CUSTOM-PROTOCOL

How to use: 
1. Run server
2. Run Client
    1. Card is inserted by hardcoding
    2. The pin for the card1 is 3213
    3. You will be provided with a list with transaction types, choose one and depending on the type you will be prompted also with the amount.

`requirements.txt added but I don't remember installing any unprovided by python modules.
TODO and Behind the scenes was for smoother development, I didn't put effort or in depth descriptions there.
Code is fragile with inputs, to be improved later with input validation and feedback.`

### Behind scenes
TODO: 

* [x] Read the docs and update `STEPS`

STEPS

* [x] Create UDP socket with basic transmission

* [x] Add state for 3 handshake to client

* [x] Connect client after 3 handshake.

* [x] Test clients working

* [x] Add security key generation to encode messages with and decode them

* [x] Add encrypt and decrypt RSA algorithm

* [x] Add sending data and receiving data with connection control (SYN INCREMENT)

* [x] Add the encryption and decryption to the protocol

* [x] Add message format for now JSON

* [x] Add handshake to each message

* [x] Test transmission protocol (encryption, handshakes, plausible exploits).

* [x] Add request type to the message (GET PUT DELETE  etc.)

* [x] Make the encryption smarter

* [ ] Add data chunkinator at application level

* [ ] Add to state NAK for not acknowledged

* [ ] Add error checking after dividing into chunks with chunkinator

* [x] Reorganize JSON or data for greater verbosity

* [x] *Optional: switch to a higher level Server

* [ ] Add priority I/O multiplexing to the server loop (select or poll or other)

* [x] Update how I log everything

* [x] Add ATM level application

* [x] Debug transactions

* [x] Add client states and transaction types

* [x] Make a pseudo TLS

...

* [ ] Reformat code for readability and good practice
