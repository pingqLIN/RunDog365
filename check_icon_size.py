import struct

def get_icon_dimensions(icon_path):
    try:
        with open(icon_path, 'rb') as f:
            # ICONDIR header: 2 bytes reserved, 2 bytes type (1=icon), 2 bytes count
            header = f.read(6)
            if len(header) < 6:
                return "Invalid/Empty file"
            
            reserved, type_, count = struct.unpack('<HHH', header)
            if type_ != 1:
                return "Not an icon file"
            
            print(f"File: {icon_path}")
            print(f"Image count: {count}")
            
            # Read ICONDIRENTRY for each image
            for i in range(count):
                # 1 byte width, 1 byte height, 1 byte color count, 1 byte reserved
                # 2 bytes planes, 2 bytes bit count, 4 bytes size, 4 bytes offset
                entry = f.read(16)
                if len(entry) < 16:
                    break
                    
                width = entry[0]
                height = entry[1]
                # 0 means 256
                if width == 0: width = 256
                if height == 0: height = 256
                
                print(f"  Image {i+1}: {width}x{height}")
                
    except Exception as e:
        print(f"Error reading {icon_path}: {e}")

get_icon_dimensions(r'c:\Dev\Projects\RunDog365\RunCat365\resources\runners\cat\dark_cat_0.ico')
get_icon_dimensions(r'c:\Dev\Projects\RunDog365\RunCat365\resources\runners\horse\dark_horse_0.ico')
