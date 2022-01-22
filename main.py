from PIL import Image
import hashlib
import random

s_in = input('type input here: ')

RGBMAX = 255
RGBMIN = 0

def hex_to_rgb(s_hex):
    r = int(s_hex[:2], 16)
    g = int(s_hex[2:4], 16)
    b = int(s_hex[4:], 16)
    return (r,g,b)

def get_star_color(rgb_tup):
    r = (rgb_tup[0] + 5 * RGBMAX) / 6
    g = (rgb_tup[1] + 5 * RGBMAX) / 6
    b = (rgb_tup[2] + 5 * RGBMAX) / 6

    return (int(r), int(g), int(b))

def get_sky_color(rgb_tup, dark_factor=4):
    r = (rgb_tup[0]) / dark_factor
    g = (rgb_tup[1]) / dark_factor
    b = (rgb_tup[2]) / dark_factor

    return (int(r), int(g), int(b))

def variate(rgb_tup, bottom, top):
    r = random.randrange(bottom,top) + rgb_tup[0]
    g = random.randrange(bottom,top) + rgb_tup[1]
    b = random.randrange(bottom,top) + rgb_tup[2]

    return (min(RGBMAX,r), min(RGBMAX,g), min(RGBMAX,b))

def check_in_pl(x, y):
    return ((x-500)**2 + (y-250)**2) < 40000

while s_in != 'qqq':
    initial_hash = hashlib.sha256(s_in.encode('utf-8')).hexdigest()

    print('initial hash ... done')

    random_key = random.randrange(0, 1000000000)

    print('random key selection ... done')

    keyed_hash = hashlib.sha256((initial_hash + str(random_key)).encode('utf-8')).hexdigest()

    print('secondary hash ... done')

    img = Image.new('RGB', [1000, 500], 0)

    pixel_map = img.load()

    print('pixel map initialize ... done')

    bg_color = get_sky_color(hex_to_rgb(keyed_hash[:6]))

    print('choose background ... done')

    sr_color = get_star_color(hex_to_rgb(keyed_hash[6:12]))

    print('choose star color ... done')

    for j in range(500):
        for i in range(1000):
            pixel_map[i, j] = bg_color

    print('fill background ... done')

    for j in range(500):
        for i in range(1000):
            k = random.random()
            if k > 0.999:
                variate_star_color = variate(sr_color,-20,30)

                variate_star_card = get_sky_color(variate_star_color, 2)

                variate_star_diag = get_sky_color(variate_star_color, 1.5)

                pixel_map[i, j] = variate_star_color

                extension = int((k - 0.9993) * 10000)

                for e_inc in range(1,extension):
                    if i > e_inc:
                        pixel_map[i-e_inc, j] = variate_star_card

                    if j > e_inc:
                        pixel_map[i, j-e_inc] = variate_star_card

                    if i < 999 - e_inc:
                        pixel_map[i+e_inc, j] = variate_star_card

                    if j < 499 - e_inc:
                        pixel_map[i, j+e_inc] = variate_star_card

                for e_inc in range(1,int(extension/2)):
                    if i > e_inc and j > e_inc:
                        pixel_map[i-e_inc, j-e_inc] = variate_star_diag

                    if i < 999 - e_inc and j > e_inc:
                        pixel_map[i+e_inc, j-e_inc] = variate_star_diag

                    if i < 999 - e_inc and j < 499 - e_inc:
                        pixel_map[i+e_inc, j+e_inc] = variate_star_diag

                    if i > e_inc and j < 499 - e_inc:
                        pixel_map[i-e_inc, j+e_inc] = variate_star_diag

    print('place stars ... done')

    pl_color = hex_to_rgb(keyed_hash[12:18])

    print('pick planet color ... done')

    for j in range(500):
        for i in range(1000):
            if check_in_pl(i, j):
                pixel_map[i, j] = pl_color

    print('place planet ... done')

    pl_secondary = hex_to_rgb(keyed_hash[18:24])

    print('pick planet secondary ... done')

    secondary_visited = set()
    spawn_probability = min(0.9375, int(keyed_hash[-2], 16) / 16)
    continuation_probability = min(0.9375, int(keyed_hash[-1], 16) / 16)

    for j in range(500):
        for i in range(1000):
            if check_in_pl(i, j):
                k = random.random()
                if k > spawn_probability:
                    q = [(i,j)]

                    while len(q) > 0:
                        currpos = q.pop(0)

                        secondary_visited.add(currpos)

                        pixel_map[currpos[0], currpos[1]] = pl_secondary

                        up = (currpos[0], currpos[1] - 1)
                        do = (currpos[0], currpos[1] + 1)
                        ri = (currpos[0] + 1, currpos[1])
                        le = (currpos[0] - 1, currpos[1])

                        surrounds = [up, do, ri, le]

                        for pos in surrounds:
                            t = random.random()
                            if check_in_pl(pos[0], pos[1]) and t > continuation_probability and pos not in secondary_visited:
                                q.append(pos)
                                secondary_visited.add(pos)

    print('color planet secondary ... done')

    pl_tertiary = hex_to_rgb(keyed_hash[24:30])

    print('pick planet tertiary ... done')

    for j in range(500):
        for i in range(1000):
            if check_in_pl(i, j):
                k = random.random()
                if k > 0.995:
                    pixel_map[i, j] = pl_tertiary

    print('color planet tertiary ... done')

    img.save(s_in + '.png')

    print('save png ... done')

    s_in = input('type input here: ')