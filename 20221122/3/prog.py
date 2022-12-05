import sys
import struct

HEADER = "4si4s4sihhiihh4si"

name = sys.stdin.read().strip()
if not name.endswith('.wav'):
	print('NO')
else:
	with open(name, 'rb') as f:
		data = f.read()
		if len(data) < 44:
			print('NO')
		else:
			ff, file_s, ff, ff, ff, typef, chan, rate, ff, ff, bps, ff, data_s = struct.unpack(HEADER, data[:44])
			print(f'Size={file_s}, Type={typef}, Channels={chan}, Rate={rate}, Bits={bps}, Data size={data_s}')


	    