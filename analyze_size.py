import os
from PIL import Image

runners = {
    "greatdane": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_v3_1768206694965.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_run_cycle_1768207148512.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame2_1768207182907.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame3_1768207201174.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\great_dane_frame4_1768207235134.png"
    ],
    "chihuahua": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_v3_1768206711526.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_frame1_1768207254335.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_frame2_1768207273398.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_frame3_1768207299405.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\chihuahua_frame4_1768207322100.png"
    ],
    "frilledlizard": [
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_v3_1768206728322.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame1_1768207342135.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame2_1768207370634.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame3_1768207388453.png",
        r"C:\Users\addra\.gemini\antigravity\brain\6f463817-4d96-4e56-9a6d-69041dd65eee\frilled_lizard_frame4_1768207406874.png"
    ]
}

def analyze():
    for name, frames in runners.items():
        print(f"--- {name} ---")
        for i, path in enumerate(frames):
            img = Image.open(path).convert("RGBA")
            # Make white transparent for bounding box calc
            datas = img.getdata()
            new_data = []
            for item in datas:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            
            bbox = img.getbbox()
            if bbox:
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                print(f"Frame {i}: bbox={bbox} size={w}x{h}")
            else:
                print(f"Frame {i}: Empty")

if __name__ == "__main__":
    analyze()
