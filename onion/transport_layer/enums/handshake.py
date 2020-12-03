from enum import Enum
# Handshake status


class HSHAKE_STATUS(Enum):
    SYN = 1
    SYN_ACK = 2
    ACK = 3
    ERROR = 4
