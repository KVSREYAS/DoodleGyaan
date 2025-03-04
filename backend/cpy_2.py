"""
Comic Panel Composer (3x2 Grid + Narrator)
-------------------------------------------
This script builds a composite comic panel by:
  • Processing six individual comic panels (each with dialog text overlaid)
    arranged in a 3‑row×2‑column grid.
  • Adding a centered narrator text box at the bottom.
All functionality is maintained while the code is refactored for clarity.
"""

import cv2
import math
import textwrap
from PIL import Image, ImageOps

# ---------------------------
# Helper Functions
# ---------------------------

def add_text(image_path: str, dialog_text: str) -> int:
    """
    Overlays dialog text on top of an image and saves the result as 'dialog_panel.png'.
    Returns the height (in pixels) of the dialog text area that was added.
    """

    # # Crop the Grok-generated image to trim the black borders on the side.
    
    temp_img = cv2.imread(image_path)
    # temp_two = temp_img[10: 1535, 450: 2485] 
    height, width = temp_img.shape[:2]
    temp_two = temp_img[int(height / 16): int(13 * height / 16), 0: width]
    temp_tri = cv2.resize(temp_two, (1105, 830))
    cv2.imwrite("temp.png", temp_tri)

    # Open image (PIL) to get dimensions.

    base_img = Image.open("temp.png")
    width, height = base_img.size
    print(width, height)
    # Calculate number of text lines and dialog area height.
    dialog_rows = math.ceil(len(dialog_text) / 54) + 1
    dialog_ht = math.ceil(width * 0.06 * dialog_rows)

    # Define the text panel region that will be added on top.
    top_left = (0, 0)
    bottom_right = (int(width), dialog_ht)

    # Expand the image by adding a border on top for the text.
    expanded_img = ImageOps.expand(base_img, border=(0, dialog_ht, 0, 0), fill=0)
    expanded_img.save('temp.png')

    # Load the expanded image using OpenCV.
    cv_img = cv2.imread('temp.png')
    font_size = 0.4 * width / 272 * 2 / 3
    font_thickness = math.floor(width / 272 * 2 / 3)

    # Draw the text panel background and the overall border.
    cv2.rectangle(cv_img, top_left, bottom_right, (239, 239, 239), -1)
    cv2.rectangle(cv_img, (0, 0), (cv_img.shape[1], cv_img.shape[0]), (0, 0, 0), font_thickness * 6)
    cv2.line(cv_img, (0, dialog_ht), (cv_img.shape[1], dialog_ht), (0, 0, 0), font_thickness * 3)

    # Wrap the dialog text.
    wrapped_dialog = textwrap.wrap(dialog_text, width = 48)
    font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC

    # Overlay each line of text.
    for i, line in enumerate(wrapped_dialog):
        # Get text height for spacing.
        text_size = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = text_size[1] + int(width * 10 / 362)
        y_position = int(width * 17.5 / 362 + i * gap)
        x_position = int(height * 10 / 362)
        cv2.putText(cv_img, line, (x_position, y_position), font, font_size, (0, 0, 0),
                    font_thickness, lineType=cv2.LINE_AA)

    cv2.imwrite("dialog_panel.png", cv_img)
    return dialog_ht

def add_narrator_text(image_path: str, dialog_text: str):
    """
    Prepares the narrator text by wrapping it and calculating the required height.
    Returns a tuple: (starting y-coordinate for narrator box, wrapped text list, text box height)
    """
    pil_img = Image.open(image_path)
    width, height = pil_img.size

    dialog_rows = math.ceil(len(dialog_text) / 54)
    dialog_ht = math.ceil(width * 0.06 * dialog_rows)
    wrapped_dialog = textwrap.wrap(dialog_text, width=54)

    # The narrator box will be drawn at the bottom (starting from height - dialog_ht).
    return int(height - dialog_ht), wrapped_dialog, dialog_ht

# ---------------------------
# Composite Panel Building
# ---------------------------

def wrap_text(text, max_width, font, font_scale, thickness):
    # Use a sample string to get an approximate character width.
    sample = "A"
    (char_width, char_height), _ = cv2.getTextSize(sample, font, font_scale, thickness)
    # Estimate number of characters that can fit:
    max_chars = max(1, int(max_width // char_width))
    return textwrap.wrap(text, width=max_chars)

def make_panel(image_list: list[list[str]], output_path: str):
    # Load base sheet image.
    page = cv2.imread("plain_sheet.png")
    page_height, page_width = page.shape[0:2]

    # ---------------------------
    # Build Narrator Box
    # ---------------------------
    narrator_text = image_list[0][0].upper()
    narrator_margin_x = 50

    # Set up font info.
    font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC
    font_scale = 0.4 * page_width / 272 * 2 / 3
    font_thickness = math.floor(page_width / 272 * 2 / 3)
    
    # Determine available text width inside the rectangle.
    available_width = page_width - 2 * narrator_margin_x

    # Wrap text based on available width.
    wrapped_narrator = wrap_text(narrator_text, available_width, font, font_scale, font_thickness)

    # Calculate total text height.
    line_height = cv2.getTextSize("A", font, font_scale, font_thickness)[0][1] + int(page_width * 10 / 362)
    narrator_ht = len(wrapped_narrator) * line_height + int(page_width * 17.5 / 362)

    # ---------------------------
    # Set up grid dimensions.
    # ---------------------------
    panel_rows = 3
    panel_cols = 2
    panel_width_fixed = 773
    panel_height_fixed = 580
    horizontal_gap = 20
    vertical_gap = 20

    grid_total_width = panel_cols * panel_width_fixed + (panel_cols - 1) * horizontal_gap
    grid_total_height = panel_rows * panel_height_fixed + (panel_rows - 1) * vertical_gap

    # Calculate overall block height (grid + vertical_gap + narrator height) and center vertically.
    block_height = grid_total_height + vertical_gap + narrator_ht
    block_origin_y = (page_height - block_height) // 2
    grid_origin_x = (page_width - grid_total_width) // 2
    grid_origin_y = block_origin_y

    # Position narrator panel exactly vertical_gap below the grid.
    narrator_top = grid_origin_y + grid_total_height + vertical_gap

    # Draw narrator background and border.
    cv2.rectangle(page,
                  (narrator_margin_x, narrator_top),
                  (page_width - narrator_margin_x, narrator_top + narrator_ht),
                  (140, 238, 255), -1)
    cv2.rectangle(page,
                  (narrator_margin_x, narrator_top),
                  (page_width - narrator_margin_x, narrator_top + narrator_ht),
                  (0, 0, 0), font_thickness)

    # Overlay the wrapped narrator text within the bounds.
    for i, line in enumerate(wrapped_narrator):
        # Get the size to center the text.
        (text_width, text_height), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        x_position = narrator_margin_x + (available_width - text_width) // 2
        y_position = narrator_top + int(page_width * 17.5 / 362) + i * line_height
        cv2.putText(page, line, (x_position, y_position), font, font_scale,
                    (0, 0, 0), font_thickness, lineType=cv2.LINE_AA)

    # ---------------------------
    # Process and Overlay Each Comic Panel in a 3x2 Grid.
    # ---------------------------
    total_panels = panel_rows * panel_cols  # 6 panels total
    for idx in range(total_panels):
        row = idx // panel_cols
        col = idx % panel_cols
        x0 = grid_origin_x + col * (panel_width_fixed + horizontal_gap)
        y0 = grid_origin_y + row * (panel_height_fixed + vertical_gap)

        panel_image_path = image_list[idx + 1][0]
        panel_dialog_text = image_list[idx + 1][1].upper()

        # Add dialog text onto the panel image.
        add_text(panel_image_path, panel_dialog_text)
        panel_with_text = cv2.imread("dialog_panel.png")
        panel_resized = cv2.resize(panel_with_text, (panel_width_fixed, panel_height_fixed))
        panel_border_thickness = math.floor(panel_height_fixed / 272 * 2 / 3)
        cv2.line(panel_resized, (0, panel_height_fixed - 1),
                 (panel_width_fixed, panel_height_fixed - 1),
                 (0, 0, 0), panel_border_thickness * 10)
        page[y0:y0 + panel_height_fixed, x0:x0 + panel_width_fixed] = panel_resized

    # Save the final composite image.
    cv2.imwrite(output_path, page)

# ---------------------------
# Example Usage
# ---------------------------
# make_panel([
#     ["THE DAWN AWAKENS THE EPIC TALE OF HEROISM AND MYSTERY, SETTING THE STAGE FOR UNFORGETTABLE BATTLES."],
#     ["comics_generated/trial1.png", "THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY."],
#     ["comics_generated/trial1.png", "WITH THE MIGHT OF THE STARS, THE HERO RISES TO DEFY THE ODDS."],
#     ["comics_generated/trial1.png", "AN UNEXPECTED ALLIANCE IS FORMED UNDER THE SILVER GLEAM OF THE MOON."],
#     ["comics_generated/trial1.png", "ANCIENT PROPHECIES WHISPER OF BATTLES YET TO COME."],
#     ["comics_generated/trial1.png", "THROUGH STORMS OF FATE, THE CHOSEN ONE FORGES AHEAD."],
#     ["comics_generated/trial1.png", "ANCIENT PROPHECIES WHISPER OF BATTLES YET TO COME.",]
# ])

# add_text("grok_sample.png", "THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY.")
