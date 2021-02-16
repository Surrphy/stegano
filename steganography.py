import argparse
from PIL import Image

MAX_BIT_VALUE = 8
MAX_COLOR_VALUE = 256

def append_0s(value, n):
    return value << MAX_BIT_VALUE - n

def get_ls_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n

def get_ms_bits(value, n):
    return value >> MAX_BIT_VALUE - n

def rm_ls_bits(value, n):
    value = value >> n
    return value << n

def mk_img(data, resolution):
    image = Image.new('RGB', resolution)
    image.putdata(data)
    return image

def encode(img_hide, img_cover, n):
    width, height = img_hide.size

    hide = img_hide.load()
    cover = img_cover.load()

    data = []

    for y in range(height):
        for x in range(width):
            r_h, g_h, b_h = hide[x,y]

            r_h = get_ms_bits(r_h, n)
            g_h = get_ms_bits(g_h, n)
            b_h = get_ms_bits(b_h, n)

            r_c, g_c, b_c = cover[x,y]

            r_c = rm_ls_bits(r_c, n)
            g_c = rm_ls_bits(g_c, n)
            b_c = rm_ls_bits(b_c, n)

            data.append((r_h + r_c,
                        g_h + g_c,
                        b_h + b_c))

    return mk_img(data, img_hide.size)

def decode(img_encoded, n):
    width, height = img_encoded.size
    encoded = img_encoded.load()

    data = []

    for y in range(height):
        for x in range(width):
            r_e, g_e, b_e = encoded[x,y]

            r_e = get_ls_bits(r_e, n)
            g_e = get_ls_bits(g_e, n)
            b_e = get_ls_bits(b_e, n)

            r_e = append_0s(r_e, n)
            g_e = append_0s(g_e, n)
            b_e = append_0s(b_e, n)
            
            data.append((r_e, g_e, b_e))

    return mk_img(data, img_encoded.size)

if __name__ == '__main__':
    img_hide_path = 'images/1.tiff'
    img_cover_path = 'images/2.tiff'
    img_encoded_path = 'images/encoded.tiff'
    img_decoded_path = 'images/decoded.tiff'
    n = 2

    img_hide = Image.open(img_hide_path).convert('RGB')
    img_cover = Image.open(img_cover_path).convert('RGB')

    encode(img_hide, img_cover, n).save(img_encoded_path)

    img_encoded = Image.open(img_encoded_path)
    decode(img_encoded, n).save(img_decoded_path)
