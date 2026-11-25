# Generates icon-192.png / icon-512.png (dark tile, blue Boom-style line, red spike ring). Stdlib only.
import zlib, struct, os

def png(path, n):
    S = n / 512
    pts = [(p[0] * S, p[1] * S) for p in [(70, 330), (200, 390), (200, 150), (330, 215), (440, 270)]]
    ring = (200 * S, 150 * S, 34 * S)
    def seg_d(x, y, a, b):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
        return ((x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2) ** 0.5
    rows = []
    for y in range(n):
        row = bytearray([0])
        for x in range(n):
            c = (11, 18, 25)
            if min(seg_d(x, y, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) < 16 * S: c = (63, 182, 255)
            if abs(((x - ring[0]) ** 2 + (y - ring[1]) ** 2) ** 0.5 - ring[2]) < 9 * S: c = (255, 77, 77)
            row += bytes(c)
        rows.append(bytes(row))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', n, n, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(data)

here = os.path.dirname(os.path.abspath(__file__))
for n in (192, 512): png(os.path.join(here, f'icon-{n}.png'), n)
print('icons ok')
