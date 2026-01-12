from PIL import Image, ImageOps
import os

# Configuration
INPUT_IMAGE_PATH = r"C:/Users/addra/.gemini/antigravity/brain/98a5c45f-b6bc-44a8-b1c3-41120cfb853e/frilled_lizard_sheet_8frames_1768211074429.png"
OUTPUT_DIR = r"c:\Dev\Projects\RunDog365\RunCat365\resources\runners\frilledlizard"
FRAME_COUNT = 8
FRAME_WIDTH = 32
FRAME_HEIGHT = 32

def process_sprites():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Error: Output directory {OUTPUT_DIR} does not exist.")
        return

    try:
        img = Image.open(INPUT_IMAGE_PATH).convert("RGBA")
        print(f"Loaded image: {img.size}")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Auto-crop to content
    # Invert to make black content white (so we can use getbbox on non-zero pixels)
    # The image is Black on White. We want to find the Black parts.
    # Gray: Black=0, White=255.
    # Inverted: Black=255, White=0.
    gray = img.convert("L")
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    
    if bbox:
        print(f"Content found at: {bbox}")
        content_img = img.crop(bbox)
    else:
        print("No content found (image is blank?)")
        return

    # Confirm we have a strip. Assume horizontal.
    c_width, c_height = content_img.size
    print(f"Cropped content size: {c_width}x{c_height}")

    # Calculate frame width
    frame_width = c_width // FRAME_COUNT
    print(f"Calculated frame width: {frame_width}")

    for i in range(FRAME_COUNT):
        # Crop frame
        left = i * frame_width
        right = left + frame_width
        # Determine height crop - center it or take full height
        # If the strip is very diverse in height, taking full cropped height is safe.
        # But we want to preserve aspect ratio when resizing to 32x32?
        # Ideally, each frame is roughly square.
        
        box = (left, 0, right, c_height)
        frame = content_img.crop(box)
        
        # Resize to 32x32, maintaining aspect ratio and padding if necessary?
        # Or just stretch fit?
        # Given "Maximize size" requirement and 32x32 target, standard resizing is usually best 
        # for pixel art if headers are close to square.
        # But let's do a "contain" resize to be safe (preserve aspect ratio).
        
        # Create a new blank 32x32 canvas
        # Determine the scaling factor
        src_w, src_h = frame.size
        ratio = min(32/src_w, 32/src_h)
        new_w = int(src_w * ratio)
        new_h = int(src_h * ratio)
        
        frame_resized = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center on 32x32 canvas
        canvas = Image.new("RGBA", (32, 32), (255, 255, 255, 0)) # Start transparent
        # Wait, if we are making a mask, transparency doesn't matter for the source paste,
        # but matters for the output.
        
        paste_x = (32 - new_w) // 2
        paste_y = (32 - new_h) // 2
        canvas.paste(frame_resized, (paste_x, paste_y))
        
        # Now convert to ICOs
        gray_frame = canvas.convert("L")
        
        # 1. Light Theme (Black Icon)
        black_icon = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        # Mask: Invert Gray (so Black pixels become White/Opaque in mask)
        # Note: If canvas background was Transparent, Gray conversion makes it Black? 
        # No, convert("L") from RGBA: Transparent (0 alpha) -> usually black or white depending on implementation.
        # Better approach: Extract Alpha channel? 
        # The source image was Black on White. 
        # Our 'frame_resized' has Black on White (or Transparent if we cropped well).
        # Let's check the source again. It was "Solid black silhouette on white background".
        # So it's likely opaque. 'canvas' has transparent background where we padded.
        # 'frame_resized' has content.
        
        # Let's rely on the color values. Dark pixels = Content.
        # Create a mask based on luminance.
        # Pixel < 128 => Content (Opaque). Pixel > 128 => Background (Transparent).
        
        mask = Image.new("L", (32, 32), 0)
        # iterate pixels? Slow. Use point op.
        # Invert gray so Dark is High Value.
        inverted_gray = ImageOps.invert(gray_frame)
        # Threshold.
        mask = inverted_gray.point(lambda p: 255 if p > 100 else 0)
        
        # Apply mask to Black Image
        black_icon.paste((0, 0, 0, 255), (0, 0), mask)
        
        # Apply mask to White Image
        white_icon = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        white_icon.paste((255, 255, 255, 255), (0, 0), mask)
        
        # Save files
        light_filename = f"light_frilledlizard_{i}.ico"
        dark_filename = f"dark_frilledlizard_{i}.ico"
        
        light_path = os.path.join(OUTPUT_DIR, light_filename)
        dark_path = os.path.join(OUTPUT_DIR, dark_filename)
        
        black_icon.save(light_path, format='ICO', sizes=[(32, 32)])
        white_icon.save(dark_path, format='ICO', sizes=[(32, 32)])
        
        print(f"Saved frame {i}")

if __name__ == "__main__":
    process_sprites()
