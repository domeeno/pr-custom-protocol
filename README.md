PR-CUSTOM-PROTOCOL

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

* [ ] Add request type to the message (GET PUT DELETE  etc.)

* [ ] Make the encryption smarter

* [ ] Add data chunkinator at application level

* [ ] Add to state NAK for not acknowledged

* [ ] Add error checking after dividing into chunks with chunkinator

* [ ] Reorganize JSON or data for greater verbosity

* [ ] *Optional: switch to a higher level Server

* [ ] Update how I log everything

Brief. I began to add Request types, need to finish with those. After I will just follow the list of steps

...

* [ ] Reformat code for readability and good practice

`<Choose the applcation-level protocol>`