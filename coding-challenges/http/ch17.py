import base64, subprocess, cStringIO
from PIL import Image
import ringzer

# def chall_func(img_string):
#     data = base64.b64decode(img_string[32:-4])
#     open('ch17.png', 'wb').write(data)
#     subprocess.call('convert -threshold 98%% ch17.png ch17b.png', shell=True)
#     return subprocess.check_output('gocr -i ch17b.png', shell=True).strip()

def chall_func(img_string):
    data = base64.b64decode(img_string[32:-4])
    im = Image.open(cStringIO.StringIO(data))
    pix = im.load()
    w, h = im.size
    black, white = ((0, 0, 0), (255, 255, 255))
    for y in range(h):
        for x in range(w):
            if pix[x,y] != white:
                pix[x,y] = white
            else:
                pix[x,y] = black
    im = im.resize((int(round(w*2, 2)), int(round(h*2, 2))), Image.ANTIALIAS)
    im.save("ch17.ppm")
    return subprocess.check_output(['ocrad', 'ch17.ppm']).strip()

ringzer.Challenge(17, chall_func, chall_repeat=5)
