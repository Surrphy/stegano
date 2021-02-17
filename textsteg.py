import requests, argparse
from PIL import Image
from io import BytesIO

MAX_BIT_VALUE = 8
MAX_COLOR_VALUE = 256

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

def encode(msg, img, n):
    width, height = img.size
    cover = img.load()
    bin_msg = to_binary(msg)
    lenght = len(bin_msg)
    print(lenght)
    data = []

    for y in range(height):
        for x in range(width):
            r, g, b = cover[x,y]
            if lenght > 0:
                f, s, t = groups_of_n(bin_msg[x], n)
                rh = rm_ls_bits(r, n)
                gh = rm_ls_bits(g, n)
                bh = rm_ls_bits(b, n)
                data.append((rh + int(f,2), gh + int(s,2), bh + int(t,2)))
                lenght -= 1
            else:
                data.append((r, g, b))
    return mk_img(data, img.size)

def decode(img, kod, n):
    width, height = img.size
    encoded = img.load()
    bin_msg = []
    lenght = kod

    for y in range(height):
        for x in range(width):
            r, g, b = encoded[x,y]

            f = get_ls_bits(r, n)
            s = get_ls_bits(g, n)
            t = get_ls_bits(b, n)

            char = to_char(f, s, t)
            if lenght > 0:
                bin_msg.append(char)
                lenght -= 1
            else:
                return bin_msg

if __name__ == '__main__':
    # img_path = 'images/unnamed.jpg'
    # encoded_path = 'images/encoded.tiff'
    # msg = 'dziobak'
    n = 2

    parser=argparse.ArgumentParser(description='Hiding in image with least significant bits')
    parser.add_argument('Mode',
                        metavar='mode',
                        type=str,
                        choices=['encode', 'decode'],
                        help='encode or decode message into/from image')
    parser.add_argument('input',
                        metavar='input',
                        type=str,
                        help='message to hide or path to image for decoding')
    parser.add_argument('-o', '--output',
                        default='out.tiff',
                        help='path to encoded image if encode')
    parser.add_argument('-c', '--cover',
                        type=str,
                        help='cover image if encode (default is random image from unsplash)')
    parser.add_argument('-r', '--resolution',
                        type=str,
                        default='800x800',
                        help='resolution of the image if you pull it from unsplash (format: widthxheight')
    parser.add_argument('-n', '--value',
                        type=int,
                        default='100',
                        help='number of characters in encoded string, if wrong not entire message will be shown, or some unwanted characters will showup')

    args = parser.parse_args()

    if args.Mode == "encode":
        if not args.cover:
            response = requests.get(f'https://source.unsplash.com/random/{args.resolution}')
            image_bytes = BytesIO(response.content)
            img = Image.open(image_bytes).convert('RGB')
        encode(args.input, img, n).save(args.output)
    else:
        encoded = Image.open(args.input)
        print(list_to_string(decode(encoded, args.value, n)))
        