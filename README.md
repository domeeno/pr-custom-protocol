PR-CUSTOM-PROTOCOL

TODO: 

* [ ] Read the docs and update `STEPS

* [ ] Choose the project to be made

Choice - `<To be added>`

STEPS:

* [x] Create local and remote repo

* [ ] Server side:

    * [ ] Make the library for the server
    
    * [ ] Define the 3 module stack of the library
    
    * [ ] Define the API with a layered architecture
    
* [ ] Client side:

    * [ ] Make the library for the client
    
    * [ ] Define the 3 module stack of the library
    
    * [ ] Define the API with a layered architecture
    
    
Implement a protocol atop UDP, with error checking and retransmissions. Limit the number of retries for retransmission.

Make the connection secure, using CA to get the public key of the receiver and encrypt data or using Diffie-Helman to get a shared connection key between client and server. Ensure that the traffic is encrypted.

`<Choose the applcation-level protocol>`