# GFXExport-8

This is a simple command line script that extracts the sprite data from a [PICO-8](http://www.lexaloffle.com/pico-8.php) cartridge into a png file.

Note that at the moment, the reverse operation (importing graphics from a png into a .p8) is not supported. Check out [Terry Cavanagh's compiler](https://twitter.com/terrycavanagh/status/634123273299619840) which is able to do that. I might add this feature in the near future if there is need for it.

## Installation
This script should support Windows, Linux and Mac (not tested)

You will need Python (any recent version, 2 or 3, should be fine). It is preinstalled under Mac and Linux. For Windows, download it [on python.org](https://www.python.org/downloads/).

Simply download the release archive and extract both .py files into a folder easily accessible by command line.

## Usage
**This script supports only .p8 cartridges, not .p8.png !!**

In a command line prompt, run `python gfxexport-8.py <cart name>`. The sprites will be extracted in output.png.

Do not put the whole path to the catridge, the default for your system is automatically used. If you need to change it, use the -d flag (see below). Adding .p8 after the catridge name is not needed as it will be appended automatically.

With command line flags, you can upscale the output image, change the output filename and change the cartridge directory
```
  -d DIRECTORY, --directory DIRECTORY
                        pico-8 carts directory (default:
                        system dependant)
  -o OUTPUT, --output OUTPUT
                        Output filename (default: output.png)
  -u UPSCALE, --upscale UPSCALE
                        Upscale factor (e.g 2=2*2 pixels) (default: 1)
```
