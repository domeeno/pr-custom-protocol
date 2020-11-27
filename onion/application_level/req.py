from enum import Enum
# Handshake status


class REQ_TYPE(Enum):
    GET = 0
    PUT = 1
    UPDATE = 2
    DELETE = 3
    GET_BUT_MORE_IMPORTANT = 4
    PUT_BUT_MORE_IMPORTANT = 5
    UPDATE_BUT_MORE_IMPORTANT = 6
    DELETE_BUT_MORE_IMPORTANT = 7
