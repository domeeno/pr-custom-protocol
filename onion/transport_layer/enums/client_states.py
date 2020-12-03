from enum import Enum


class CLIENT_STATE(Enum):
    CARD_INSERTED = 1,
    REQ_PIN = 2,
    ERROR_PIN = 3,
    SUCCESS_PIN = 4,
    CLIENT_NOT_FOUND = 5,
    ON_CLIENT_SESSION = 6


class REQUEST_TYPE(Enum):
    NO_REQUEST = 0,
    BALANCE = 1,
    WITHDRAW = 2,
    DEPOSIT = 3
