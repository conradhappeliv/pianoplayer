import settings

def generate_command(command, timing, *args):
    command_string = b''
    command_string += settings.MAPPINGS[command].to_bytes(1, byteorder='big')
    command_string += timing.to_bytes(3, byteorder='big')
    for arg in args:
        command_string += arg.to_bytes(1, byteorder='big')
    if len(command_string) < settings.MSG_LENGTH:
        for i in range(settings.MSG_LENGTH - len(command_string)):
            command_string += (0).to_bytes(1, byteorder='big')
    return command_string


def decode_command(command_string):
    return {
        'command': settings.MAPPINGS(command_string[0]),
        'timing' : int.from_bytes(command_string[1:4], byteorder='big'),
        'data'  : [
            command_string[4],
            command_string[5],
            command_string[6],
            command_string[7]
        ]
    }
