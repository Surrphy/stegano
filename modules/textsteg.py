import requests, argparse
from modules.defi import mk_img, rm_ls_bits, get_ls_bits, groups_of_n, to_binary, to_char, list_to_string
from PIL import Image
from io import BytesIO

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

def decode(img, l, n):
    width, height = img.size
    encoded = img.load()
    bin_msg = []
    lenght = l

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
                return list_to_string(bin_msg)