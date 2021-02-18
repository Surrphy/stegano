from PIL import Image

MAX_BIT_VALUE = 8
MAX_COLOR_VALUE = 256

### IMAGESTEG ###
def append_0s(value, n):
    return value << MAX_BIT_VALUE - n

def get_ms_bits(value, n):
    return value >> MAX_BIT_VALUE - n

### TEXTSTEG ###

def groups_of_n(string, n):
    groups = [string[i:i+n] for i in range(0, len(string), n)]
    return [groups[0], groups[1], groups[2]]

def to_binary(text):
    byte_array = bytearray(text, 'utf-8')
    byte_list = []

    for byte in byte_array:
        binary = bin(byte)
        byte_list.append(binary.removeprefix('0b1'))
    return byte_list

def to_char(f, s , t):
    prefix = '01'
    f = bin(f).removeprefix('0b').zfill(2)
    s = bin(s).removeprefix('0b').zfill(2)
    t = bin(t).removeprefix('0b').zfill(2)

    return chr(int(f'{prefix}{f}{s}{t}', 2))

def list_to_string(list):
    string = ''
    for char in list:
        if char == "@":
            string += ' '
        else:
            string += char
    return string

### SHARED ###

def mk_img(data, resolution):
    image = Image.new('RGB', resolution)
    image.putdata(data)
    return image

def rm_ls_bits(value, n):
    value = value >> n
    return value << n

def get_ls_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n