"""
Comic Panel Composer
--------------------
This script reads a base sheet (plain_sheet.png) and several comic panels,
then overlays text and composes them together into a final output file "sheet_output.png".
All functionality is maintained; only formatting and commenting have been updated for clarity.
"""

import cv2
import math
import textwrap
from PIL import Image, ImageOps

# ---------------------------
# Helper functions
# ---------------------------

def add_text(image_path: str, dialog_text: str) -> int:
    """
    Reads an image, adds a dialog text panel on top, and saves the result as 'dialog_panel.png'.
    Returns the height of the dialog text area.
    """
    # Open image with PIL to get size
    base_img = Image.open(image_path)
    width, height = base_img.size

    # Calculate the number of lines and dialog panel height
    dialog_rows = math.ceil(len(dialog_text) / 54)
    dialog_ht = math.ceil(width * 0.06 * dialog_rows)

    # Define top-left and bottom-right corners for the text panel
    top_left = (0, 0)
    bottom_right = (int(width), dialog_ht)

    # Expand image for the text area (adds border on the top)
    expanded_img = ImageOps.expand(base_img, border=(0, dialog_ht, 0, 0), fill=(0, 0, 0))
    expanded_img.save('temp.png')

    # Read the expanded image with OpenCV for further processing
    cv_img = cv2.imread('temp.png')
    font_size = 0.4 * width / 272 * 2 / 3
    font_thickness = math.floor(width / 272 * 2 / 3)
    
    # Fill the text panel with a light color
    cv2.rectangle(cv_img, top_left, bottom_right, (239, 239, 239), -1)
    # Draw a thick outer border
    cv2.rectangle(cv_img, (0, 0), (cv_img.shape[1], cv_img.shape[0]), (0, 0, 0), font_thickness * 6)
    # Draw a separator line between dialog and image
    cv2.line(cv_img, (0, dialog_ht), (cv_img.shape[1], dialog_ht), (0, 0, 0), font_thickness * 3)

    # Wrap dialog text into multiple lines
    wrapped_dialog = textwrap.wrap(dialog_text, width=54)
    font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC

    # Place the text lines onto the image
    for i, line in enumerate(wrapped_dialog):
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = textsize[1] + int(width * 10 / 362)
        y_position = int(width * 17.5 / 362 + i * gap)
        x_position = int(height * 10 / 362)
        cv2.putText(cv_img, line, (x_position, y_position), font, font_size, (0, 0, 0),
                    font_thickness, lineType=cv2.LINE_AA)

    # Save the modified image containing the dialog panel
    cv2.imwrite("dialog_panel.png", cv_img)
    return dialog_ht

def add_narrator_text(image_path: str, dialog_text: str):
    """
    Prepares narrator text details.
    Returns a tuple of (starting y-coordinate for text, wrapped text lines, dialog text height).
    """
    # Open image using PIL to get dimensions
    pil_img = Image.open(image_path)
    width, height = pil_img.size

    # Calculate required rows and height for the dialog text
    dialog_rows = math.ceil(len(dialog_text) / 54)
    dialog_ht = math.ceil(width * 0.06 * dialog_rows)

    # Wrap dialog text into multiple lines
    wrapped_dialog = textwrap.wrap(dialog_text, width=54)
    # Return the starting y-coordinate (bottom minus dialog height) along with wrapped text and height
    return int(height - dialog_ht), wrapped_dialog, dialog_ht

# ---------------------------
# Main composite panel creation
# ---------------------------
# ---------------------------

def crop_to_aspect_ratio(image, target_aspect_ratio=4/3):
    """
    Crops the image only vertically (from the bottom) so that the top portion fits
    the 4:3 ratio. This means we keep the top and remove pixels from the bottom if needed.
    """
    height, width = image.shape[:2]
    required_height = int(width / target_aspect_ratio)
    if height > required_height:
        # Keep the top portion; drop extra pixels at the bottom.
        return image[0:required_height, :]
    return image

def process_panel_image(image_path, dialog_text, final_width=773, final_height=580):
    """
    Loads a panel image, overlays its dialog text (via add_text),
    crops it (only from the bottom) to a 4:3 aspect ratio, and
    finally resizes it to the target dimensions.
    """
    # Write the image with the dialog text added.
    dialog_ht = add_text(image_path, dialog_text)  
    # (Assumes add_text saves the output to "dialog_panel.png")
    panel_with_text = cv2.imread("dialog_panel.png")
    # Crop vertically (only remove bottom pixels) to 4:3:
    cropped_panel = crop_to_aspect_ratio(panel_with_text, target_aspect_ratio=4/3)
    # Finally, resize to the fixed 773 x 580 resolution.
    resized_panel = cv2.resize(cropped_panel, (final_width, final_height), interpolation=cv2.INTER_AREA)
    return resized_panel

def wrap_text(text, max_width, font, font_scale, thickness):
    # Use a sample character to estimate the width per character.
    sample = "A"
    (char_width, _), _ = cv2.getTextSize(sample, font, font_scale, thickness)
    max_chars = max(1, int(max_width // char_width))
    return textwrap.wrap(text, width=max_chars)

def make_panel(image_list: list[list[str]]):
    # Load base sheet image.
    page = cv2.imread("plain_sheet.png")
    page_height, page_width = page.shape[:2]

    # ---------------------------
    # Build Narrator Box
    # ---------------------------
    narrator_text = image_list[0][0].upper()
    narrator_margin_x = 50

    # Set up font info.
    font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC
    font_scale = 0.4 * page_width / 272 * 2 / 3
    font_thickness = math.floor(page_width / 272 * 2 / 3)

    # Calculate available text width inside the narrator rectangle.
    available_width = page_width - 2 * narrator_margin_x

    # Pre-wrap narrator text so that each line fits inside available width.
    wrapped_narrator = wrap_text(narrator_text, available_width, font, font_scale, font_thickness)

    # Calculate the line height and the total height required for the narrator text.
    line_height = cv2.getTextSize("A", font, font_scale, font_thickness)[0][1] + int(page_width * 10 / 362)
    narrator_ht = len(wrapped_narrator) * line_height + int(page_width * 17.5 / 362)

    # ---------------------------
    # Set up grid dimensions (2×2 panels)
    # ---------------------------
    panel_rows = 2
    panel_cols = 2
    panel_width_fixed = 773
    panel_height_fixed = 580
    horizontal_gap = 20
    vertical_gap = 20

    grid_total_width = panel_cols * panel_width_fixed + (panel_cols - 1) * horizontal_gap
    grid_total_height = panel_rows * panel_height_fixed + (panel_rows - 1) * vertical_gap

    # Center the entire block (panels + vertical gap + narrator) vertically.
    block_height = grid_total_height + vertical_gap + narrator_ht
    block_origin_y = (page_height - block_height) // 2
    grid_origin_x = (page_width - grid_total_width) // 2
    grid_origin_y = block_origin_y

    # Position narrator directly below the grid.
    narrator_top = grid_origin_y + grid_total_height + vertical_gap

    # Draw narrator box background and border.
    cv2.rectangle(page,
                  (narrator_margin_x, narrator_top),
                  (page_width - narrator_margin_x, narrator_top + narrator_ht),
                  (140, 238, 255), -1)
    cv2.rectangle(page,
                  (narrator_margin_x, narrator_top),
                  (page_width - narrator_margin_x, narrator_top + narrator_ht),
                  (0, 0, 0), font_thickness)

    # Overlay the wrapped narrator text (center-aligned horizontally).
    for i, line in enumerate(wrapped_narrator):
        (text_width, _), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        x_position = narrator_margin_x + (available_width - text_width) // 2
        y_position = narrator_top + int(page_width * 17.5 / 362) + i * line_height
        cv2.putText(page, line, (x_position, y_position), font, font_scale,
                    (0, 0, 0), font_thickness, lineType=cv2.LINE_AA)

    # ---------------------------
    # Process and Overlay Each Comic Panel in a 2×2 Grid.
    # ---------------------------
    total_panels = panel_rows * panel_cols  # 4 panels total
    for idx in range(total_panels):
        row = idx // panel_cols
        col = idx % panel_cols
        x0 = grid_origin_x + col * (panel_width_fixed + horizontal_gap)
        y0 = grid_origin_y + row * (panel_height_fixed + vertical_gap)

        panel_image_path = image_list[idx + 1][0]
        panel_dialog_text = image_list[idx + 1][1].upper()

        # Add panel dialog text via the add_text helper (assumed to save "dialog_panel.png").
        add_text(panel_image_path, panel_dialog_text)
        panel_with_text = cv2.imread("dialog_panel.png")
        # Scale panel image to fixed dimensions.
        panel_resized = cv2.resize(panel_with_text, (panel_width_fixed, panel_height_fixed))
        panel_border_thickness = math.floor(panel_height_fixed / 272 * 2 / 3)
        cv2.line(panel_resized, (0, panel_height_fixed - 1),
                 (panel_width_fixed, panel_height_fixed - 1),
                 (0, 0, 0), panel_border_thickness * 10)
        # Paste the panel into the composite sheet.
        page[y0:y0 + panel_height_fixed, x0:x0 + panel_width_fixed] = panel_resized

    # Save the final composite image.
    cv2.imwrite("sheet_output.png", page)
# Execution: Build the composite comic panel
# ---------------------------

make_panel([
    ["THE DAWN AWAKENS THE EPIC TALE OF HEROISM AND MYSTERY, SETTING THE STAGE FOR UNFORGETTABLE BATTLES."],
    ["image_1.png", "THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY. THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY."],
    ["image_2.png", "WITH THE MIGHT OF THE STARS, THE HERO RISES TO DEFY THE ODDS."],
    ["image_3.png", "AN UNEXPECTED ALLIANCE IS FORMED UNDER THE SILVER GLEAM OF THE MOON."],
    ["image_4.png", "THE VILLAIN LAUGHS, NAIVELY THINKING DEFEAT IS UNAVOIDABLE."]])