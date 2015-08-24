# coding: utf-8

from __future__ import division, absolute_import, print_function,\
    unicode_literals

"""
  GfxExport-8 v 1.0.0
  Sprite extractor for PICO-8 carts

  Copyright (c) 2015 FrozenTux <frozentux@frozentux.fr>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.


  Uses PyPNG, Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
  licensed under MIT licence (see png.py)

"""

__version__ = '1.0.0'

import argparse
import sys
import os

import png

# PICO-8 palette, rgb
PALETTE = [(0, 0, 0),           # 0 Black
           (29, 43, 83),        # 1 Dark blue
           (126, 37, 83),       # 2 Dark purple
           (0, 135, 81),        # 3 Dark Green
           (171, 82, 54),       # 4 Brown
           (95, 87, 79),        # 5 Dark Gray
           (194, 195, 199),     # 6 Light Gray
           (255, 241, 232),     # 7 White (kinda)
           (255, 0, 77),        # 8 Red
           (255, 163, 0),       # 9 Orange
           (255, 255, 39),      # A Yellow
           (0, 231, 88),        # B Light Green
           (41, 173, 255),      # C Light Blue
           (131, 118, 156),     # D Light Purple
           (255, 119, 168),     # E Dark Pink
           (255, 204, 170)      # F Light Pink
           ]

print('GFXExport-8 v{0}\n'.format(__version__))

# Default cart folder for windows, mac, linux
if sys.platform.startswith('win32'):
    cart_dir = os.path.join(os.environ['APPDATA'], 'pico-8', 'carts')
elif sys.platform.startswith('linux'):
    cart_dir = os.path.expanduser(os.path.join('~', '.lexaloffle',
                                  'pico-8', 'carts'))
elif sys.platform.startswith('darwin'):
    cart_dir = os.path.expanduser(os.path.join('~', 'Library',
                                  'Application Support', 'pico-8', 'carts'))
else:
    print('Warning : Unsupported platform. Set your cart directory manually'
          'with -d.')
    cart_dir = 'MUST BE SET'

# Initialization of argument paring
parser = argparse.ArgumentParser(description='Extract sprite data from a p8 '
                                 'cartridge into a png file.\nDoes '
                                 'not support .p8.png',
                                 formatter_class=argparse
                                 .ArgumentDefaultsHelpFormatter)
# Optional
parser.add_argument('-d', '--directory',
                    help='pico-8 carts directory',
                    default=cart_dir)
parser.add_argument('-o', '--output',
                    help='Output filename',
                    default='output.png')
parser.add_argument('-u', '--upscale', type=int,
                    help='Upscale factor (e.g 2=2*2 pixels)',
                    default=1)

# Positional
parser.add_argument('cart_name',
                    help='Name of the cartridge (no need to add .p8)')

args = parser.parse_args()

# Sanity checks
# Cart folder has been set on supported platforms
if args.directory == 'MUST BE SET':
    print('Error : Unsupported platform. Set your cart directory manually'
          'with -d.')
    sys.exit(1)

# Add .p8 after file name
if not args.cart_name.endswith('.p8'):
    args.cart_name += '.p8'

# File actually exists
path = os.path.join(args.directory, args.cart_name)
if not os.path.isfile(path):
    print('Error : File {0} not found'.format(path))
    sys.exit(1)

print('Extracting GFX from {0} into {1}...'.format(path, args.output))

# Begin the actual extraction
with open(path, 'r') as rf:
    skip = True
    # Skip lines until the gfx block
    while skip:
        line = rf.readline()
        if line.startswith('__gfx__'):
            skip = False

    pixels = []
    while True:
        # Read lines until the next block
        line = rf.readline().strip()
        if line.startswith('__'):
            break

        # Repeat lines to upscale
        for i in range(args.upscale):
            pxline = []
            for char in line:
                # Convert from hex to integer
                idx = int(char, 16)
                # Repeat pixels to upscale
                for j in range(args.upscale):
                    pxline.append(idx)

            pixels.append(pxline)

    writer = png.Writer(len(pixels[0]), len(pixels), palette=PALETTE)

    with open(args.output, 'wb') as wf:
        writer.write(wf, pixels)

print('Done')
