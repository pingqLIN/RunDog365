import os
from PIL import Image, ImageOps

# Define source mapping
runners = {
    "greatdane": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_v3_1768206694965.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_run_cycle_1768207148512.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame2_1768207182907.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame3_1768207201174.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame4_1768207235134.png"
    ],
    "chihuahua": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_pixel_art_v2_1768206406891.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_v2_frame1_new_1768210252320.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_v2_frame2_new_1768210269059.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_v2_frame3_new_1768210288135.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_v2_frame4_new_1768210308170.png"
    ],
    "frilledlizard": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_v3_1768206728322.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame1_1768207342135.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame2_1768207370634.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame3_1768207388453.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame4_1768207406874.png"
    ]
}

base_path = r"c:\Dev\Projects\RunDog365\RunCat365\resources\runners"

def convert_and_save():
    for runner_name, frames in runners.items():
        runner_dir = os.path.join(base_path, runner_name)
        if not os.path.exists(runner_dir):
            os.makedirs(runner_dir)

        for i, frame_path in enumerate(frames):
            try:
                img = Image.open(frame_path).convert("RGBA")
                
                # 1. Make white transparent
                datas = img.getdata()
                new_data = []
                for item in datas:
                    if item[0] > 200 and item[1] > 200 and item[2] > 200:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                img.putdata(new_data)

                # 2. Crop to content bounding box
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                
                # 3. Resize to fit 32x32 max, maintaining aspect ratio
                TARGET_SIZE = 32
                w, h = img.size
                scale = min(TARGET_SIZE / w, TARGET_SIZE / h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                
                # Use Lanczos for high quality downscaling
                if hasattr(Image, 'Resampling'):
                     resample_method = Image.Resampling.LANCZOS
                else:
                     resample_method = Image.LANCZOS

                img = img.resize((new_w, new_h), resample_method)
                
                # 4. Center on 32x32 canvas
                final_img = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
                paste_x = (TARGET_SIZE - new_w) // 2
                paste_y = (TARGET_SIZE - new_h) // 2
                final_img.paste(img, (paste_x, paste_y))
                
                img = final_img

                # 5. Save Light Theme Icon
                light_icon_path = os.path.join(runner_dir, f"light_{runner_name}_{i}.ico")
                img.save(light_icon_path, format='ICO')
                print(f"Saved {light_icon_path}")

                # 6. Save Dark Theme Icon (Inverted)
                r, g, b, a = img.split()
                r = ImageOps.invert(r)
                g = ImageOps.invert(g)
                b = ImageOps.invert(b)
                dark_img = Image.merge('RGBA', (r, g, b, a))
                
                dark_icon_path = os.path.join(runner_dir, f"dark_{runner_name}_{i}.ico")
                dark_img.save(dark_icon_path, format='ICO')
                print(f"Saved {dark_icon_path}")

            except Exception as e:
                print(f"Error processing {runner_name} frame {i}: {e}")

if __name__ == "__main__":
    convert_and_save()
