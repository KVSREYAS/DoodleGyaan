import cv2, math, textwrap, os
from PIL import Image, ImageOps
def add_text(image_path: str, dialog_text: str):
    img = Image.open(image_path)
    width, height = img.size
    dialog_rows = math.ceil(float(len(dialog_text) / 54))
    dialog_ht = math.ceil(float(width * 0.06 * dialog_rows))
    tl = 0, 0
    br = (int(width), dialog_ht)
    bordered = ImageOps.expand(img, border=(0,dialog_ht,0,0), fill=(0,0,0))
    bordered.save('temp.png')
    img = cv2.imread('temp.png')
    os.remove('temp.png')
    font_size = (0.4 * width / 272 * 2 / 3)
    font_thickness = math.floor(width / 272 * 2 / 3)
    cv2.rectangle(img, tl, br, (0, 255, 255), -1)
    cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), (0, 0, 0), font_thickness * 6)
    cv2.line(img, (0, int(dialog_ht)), (img.shape[1], int(dialog_ht)), (0, 0, 0), font_thickness * 3)
    wrapped_dialog = textwrap.wrap(dialog_text, width = 54)
    font =  cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC
    for i, line in enumerate(wrapped_dialog):   
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = textsize[1] + int(width * 10 / 362)
        y = int((width * 17.5 / 362) + i * (gap))
        x = int(int(height * 10 / 362))
        cv2.putText(img, line, (x, y), font, font_size, (0,0,0), font_thickness, lineType = cv2.LINE_AA)
    cv2.imwrite("output.png", img)
    return

add_text("input.png", "AND I, AM IRON MAN.")