import argparse, requests
from modules import append_0s, get_ms_bits, mk_img, rm_ls_bits, get_ls_bits
from PIL import Image
from io import BytesIO

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
