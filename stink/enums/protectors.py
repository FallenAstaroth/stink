from enum import Enum


class Protectors(Enum):
    processes = "Processes"
    mac_address = "Mac address"
    computer = "Computer"
    user = "User"
    hosting = "hosting"
    http_simulation = "HTTP simulation"
    virtual_machine = "Virtual machine"
    disable = "Disable"
    all = "All"
