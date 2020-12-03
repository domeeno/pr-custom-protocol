from enum import Enum


class HSHAKE_STATUS(Enum):
    C_HELLO = 1
    S_HELLO = 2
    CERTIFICATE = 3
    S_KEY_EXCHANGE = 4
    S_HELLO_DONE = 5
    C_KEY_EXCHANGE = 6
    CHANGE_TO_CYPHER = 7
    AUTHENTICATED = 8
