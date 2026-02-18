from PIL import Image, ImageSequence

ascii_chars = "@#W$9876543210?!abc;:+=-,._ "

def frame_to_ascii(img, width=80):
    # resize
    w, h = img.size
    ratio = h / w
    img = img.resize((width, int(width * ratio * 0.55)))
    
    # grayscale
    img = img.convert("L")
    
    result = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            result += ascii_chars[pixel * len(ascii_chars) // 256]
        result += "\n"
    return result

def gif_to_ascii_animation(gif_path, output_path="animation.txt"):
    gif = Image.open(gif_path)
    frames = ImageSequence.Iterator(gif)

    with open(output_path, "w", encoding="utf-8") as f:
        for frame in frames:
            ascii_frame = frame_to_ascii(frame)
            # 화면 지우기 + 커서 초기화
            f.write("\x1b[2J\x1b[H")
            f.write(ascii_frame)
            # GIF 각 프레임 딜레이를 그대로 사용
            delay = gif.info.get("duration", 80) / 1000.0
            f.write(f"\x1b[{delay}s")
            
    print("완료: animation.txt 생성됨")

gif_to_ascii_animation("input.gif")
