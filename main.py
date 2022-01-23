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

def check_in(x, y, rad, centerx=500, centery=250):
    return ((x-centerx)**2 + (y-centery)**2) < (rad**2)

def check_ring(x, y, radx, rady, ring_width, ring_angle):
    inner_ring_x = (min(200,radx-ring_width)) if not ring_angle else radx-ring_width
    inner_ring_y = (min(200,rady-ring_width)) if ring_angle else rady-ring_width
    inside_outer_ring = (((x-500)**2) / (radx**2) + ((y-250)**2) / (rady**2)) < 1
    inside_inner_ring = (((x-500)**2) / (inner_ring_x**2) + ((y-250)**2) / (inner_ring_y**2)) < 1
    return inside_outer_ring and (not inside_inner_ring)

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
            if check_in(i, j, 200):
                pixel_map[i, j] = pl_color

    print('place planet ... done')

    pl_secondary = hex_to_rgb(keyed_hash[18:24])

    print('pick planet secondary ... done')

    secondary_visited = set()
    spawn_probability = min(0.9375, int(keyed_hash[-2], 16) / 16)
    continuation_probability = min(0.9375, (int(keyed_hash[-1], 16) / 16) ** 0.5)

    for j in range(500):
        for i in range(1000):
            if check_in(i, j, 200):
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
                            if check_in(pos[0], pos[1], 200) and t > continuation_probability and pos not in secondary_visited:
                                q.append(pos)
                                secondary_visited.add(pos)

    print('color planet secondary ... done')

    pl_tertiary = hex_to_rgb(keyed_hash[24:30])

    print('pick planet tertiary ... done')

    for j in range(500):
        for i in range(1000):
            if check_in(i, j, 200):
                k = random.random()
                if k > 0.995:
                    pixel_map[i, j] = pl_tertiary

    print('color planet tertiary ... done')

    colors_so_far = set([pl_tertiary, pl_secondary, pl_color])
    moon_colors = set([])

    moon_bool = int(keyed_hash[-3], 16) > 11

    print('decide moon ... done')

    if moon_bool:
        moon_vert_pos = int(keyed_hash[30], 16) * 16 + 122
        moon_hori_pos = int(keyed_hash[31], 16) * 32 + 244
        moon_size = int(keyed_hash[32], 16) * 5 + 20

        moon_color = hex_to_rgb(keyed_hash[33:39])
        moon_secondary = hex_to_rgb(keyed_hash[39:45])

        moon_secondary_prob = int(keyed_hash[46], 16) / 16

        colors_so_far.add(moon_secondary)
        colors_so_far.add(moon_color)

        moon_colors.add(moon_secondary)
        moon_colors.add(moon_color)

        for j in range(500):
            for i in range(1000):
                if check_in(i, j, moon_size, moon_hori_pos, moon_vert_pos):
                    pixel_map[i,j] = moon_color

        for j in range(500):
            for i in range(1000):
                if check_in(i, j, moon_size, moon_hori_pos, moon_vert_pos):
                    if random.random() > moon_secondary_prob:
                        pixel_map[i,j] = moon_secondary

        print('add moon ... done')

    ring_bool = int(keyed_hash[-4], 16) > 11

    print('decide ring ... done')

    if ring_bool:
        ring_angle = False #int(keyed_hash[-5], 16) > 7
        ring_vert_size = int(keyed_hash[47], 16) * 5 + 64
        ring_hori_size = int(keyed_hash[48], 16) * 10 + 200

        ring_width = ring_hori_size - (200 + int(keyed_hash[48], 16)*random.randrange(0,5)*2)
        if ring_angle:
            ring_vert_size, ring_hori_size = ring_hori_size, ring_vert_size

        ring_color = hex_to_rgb(keyed_hash[49:55])

        for j in range(500):
            for i in range(1000):
                if check_ring(i, j, ring_hori_size, ring_vert_size, ring_width, ring_angle):
                    if not ring_angle:
                        if j < 250:
                            if pixel_map[i,j] not in colors_so_far:
                                pixel_map[i,j] = ring_color
                        else:
                            if pixel_map[i,j] not in moon_colors:
                                pixel_map[i,j] = ring_color
                    if ring_angle:
                        if i < 500:
                            if pixel_map[i,j] not in colors_so_far:
                                pixel_map[i,j] = ring_color
                        else:
                            if pixel_map[i,j] not in moon_colors:
                                pixel_map[i,j] = ring_color


        print('add ring ... done')

    img.save(s_in + '.png')

    print('save png ... done')

    s_in = input('type input here: ')