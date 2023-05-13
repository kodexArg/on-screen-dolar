import os
import cv2
import json
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from loguru import logger



def get_prices_from_json() -> str:
    """ Returns a single string with the prices from 'src/prices.json' file """
    prices_dict = json.load(open(os.path.join("src", "prices.json")))
    return  "          ".join([f"{key}: {value.replace(' ', '')}" for key, value in prices_dict.items()])



def draw_price_board(frame):
    print(type(frame))
    """ raws the price board on the frame
    Args:
        frame (np.array): a frame of the background video
    Yields:
        np.array: a frame with the price board
    """
    # Image and Draw context
    width, height = frame.shape[1], frame.shape[0]
    image = Image.fromarray(np.zeros((height, width, 4), dtype=np.uint8))
    draw = ImageDraw.Draw(image)

    # Text and font
    text = get_prices_from_json()
    font = ImageFont.truetype(os.path.join("src", "led_8x6.ttf"), 32)
    text_width, text_height = draw.textsize(text, font)

    # Initial position and speed
    x, y = width, (height - text_height) // 2  # center of screen (x,y)
    speed = 8

    while True:
        # Move the text
        x -= speed
        if x < -text_width:
            x = width

        # Draw the marquee and yield each step
        draw.rectangle((0, 0, width, height), fill=(0, 0, 0, 0))
        draw.text((x, y), text, font=font, fill=(250, 250, 250))
        transparent_image_np = np.array(image)
        transparent_frame = np.zeros((height, width, 4), dtype=np.uint8)
        transparent_frame[:, :, 3] = 255  # set alpha channel to fully opaque
        transparent_frame[:, :, :3] = frame[:, :, :3]  # set background

        # Paste the transparent image with the text onto the transparent frame
        transparent_frame = Image.fromarray(transparent_frame)
        transparent_frame.paste(
            Image.fromarray(transparent_image_np),
            (0, 0),
            Image.fromarray(transparent_image_np),
        )
        yield np.array(transparent_frame)


def get_video_capture_object():
    """iterator for background video (return: cap)"""
    src_dir = "src"
    video_files = os.listdir(src_dir)
    for video_file in video_files:
        if video_file.endswith(".mp4"):
            video_file_path = os.path.join(src_dir, video_file)
            logger.info(f"Loading {video_file_path}")
            cap = cv2.VideoCapture(video_file_path)
            if not cap.isOpened():
                raise RuntimeError(f"Error opening video file '{video_file_path}'")
            yield cap


def set_video_to_full_screen(video_capture_object):
    # REMOVER ESTO:
    return
    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def play_video_loop():
    for cap in get_video_capture_object():  # cycle through videos in src folder
        set_video_to_full_screen(cap)
        price_board = draw_price_board(cap.read()[1])
        
        while True:  # cycle through each video frame
            ret, frame = cap.read()
            if not ret:
                break

            # Draw the price board
            frame = next(price_board)

            cv2.imshow("Video", frame)
            key = cv2.waitKey(30)
            if key == 27:  # Esc
                exit()


def main():
    play_video_loop()


if __name__ == "__main__":
    main()
