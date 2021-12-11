from PIL import Image, ImageDraw, ImageFilter
import random
import os

def paste_on_background(qr_img, num, bg_range=4):
    nth_background = random.choice(range(0, bg_range))
    background_img = Image.open(f"./background_images/bg_{nth_background+1}.jpg")

    row_pos = random.choice(range(background_img.size[0]//2))
    col_pos = random.choice(range(background_img.size[1]//2))

    copied_img = background_img.copy()
    copied_img.paste(qr_img, (row_pos, col_pos))
    copied_img.save(f"./qrs_with_background/qr_over_bg{num}.jpg")

def main():
    num = 1
    for qr_img_path in os.listdir("./generated_qrs"):
        qr_img = Image.open("./generated_qrs/" + qr_img_path)
        paste_on_background(qr_img, num)
        num += 1

if __name__=="__main__":
    main()