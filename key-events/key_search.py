import select, os, time, struct

with open('/dev/input/event0', 'rb') as event0:
    while True:
        time.sleep(1)
        r, w, e = select.select([event0], [], [], 0)
        while event0 in r:
            data = os.read(event0.fileno(), 16)
            time_info = struct.unpack('ll', data[:8])
            event_info = struct.unpack('HHI', data[8:])
            print(time_info, event_info)
            r, w, e = select.select([event0], [], [], 0)
        else:
            print('Nothing!')
