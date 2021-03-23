def rgb2hex(rgb):

    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


with open(r'D:\radar\wsr88dv.rgb', 'r') as fp:
    file = fp.readlines()

xx=[i.strip().split() for i in file ]

out = []
for i in xx:
    out.append(rgb2hex(i))

print(out)
