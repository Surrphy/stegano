import requests, argparse, modules.imagesteg, modules.textsteg
from io import BytesIO
from PIL import Image

n = 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple steganography tool to hide in image, text or another picture.')
    parser.add_argument('Mode',
                        metavar='mode',
                        type=str,
                        choices=['encode','decode'],
                        help='decode or encode')
    parser.add_argument('Type',
                        metavar='type',
                        choices=['text', 'image'],
                        help='encode/decode text or image')
    parser.add_argument('input',
                        metavar='input',
                        type=str,
                        help='picture to decode/encode (image type) or text to encode/image to decode (text type)')
    parser.add_argument('-o', '--output',
                        default='out.tiff',
                        help='path to output file (out.tiff default)')
    parser.add_argument('-c', '--cover',
                        type=str,
                        help='cover image if encode (default is random image from unsplash)')
    parser.add_argument('-r', '--resolution',
                        type=str,
                        default='800x800',
                        help='resolution of the image if you pull it from unsplash (format: /width/x/height/)')
    parser.add_argument('-l', '--length',
                        type=int,
                        default='100',
                        help='number of characters in encoded string, if wrong not entire message will be shown, or some unwanted characters will show')

    args = parser.parse_args()

    if args.Mode == 'encode':
        ### encoding
        if args.Type == 'image':
            img = Image.open(args.input)

            if not args.cover:
                w, h = img.size

                response = requests.get(f'https://source.unsplash.com/random/{w}x{h}')
                image_bytes = BytesIO(response.content)
                cover = Image.open(image_bytes).convert('RGB')

            modules.imagesteg.encode(img, cover, n).save(args.output)
        else:

            if not args.cover:
                response = requests.get(f'https://source.unsplash.com/random/{args.resolution}')
                image_bytes = BytesIO(response.content)
                cover = Image.open(image_bytes).convert('RGB')
            else:
                cover = Image.open(args.cover)

            modules.textsteg.encode(args.input, cover, n).save(args.output)
    else:
        ### decoding
        if args.Type == 'image':
            modules.imagesteg.decode(Image.open(args.input), n).save(args.output)
        else:
            print(modules.textsteg.decode(Image.open(args.input), args.length, n))

