import os
import cv2
import json
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from loguru import logger


def get_prices_from_json() -> str:
    """Returns a single string with the prices from 'src/prices.json' file"""
    prices_dict = json.load(open(os.path.join("src", "prices.json")))
    return "          ".join(
        [f"{key}: {value.replace(' ', '')}" for key, value in prices_dict.items()]
    )


def set_video_to_full_screen(video_capture_object):
    # REMOVER ESTO:
    return
    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# Iterator for the background video frames
def get_background_video_frames() -> np.array:
    src_dir = "src"
    video_files = os.listdir(src_dir)
    for video_file in video_files:
        if video_file.endswith(".mp4"):
            video_file_path = os.path.join(src_dir, video_file)
            logger.info(f"Loading {video_file_path}")
            cap = cv2.VideoCapture(video_file_path)
            if not cap.isOpened():
                raise RuntimeError(f"Error opening video file '{video_file_path}'")
            try:
                # Main Loop cycling through frames of the video
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    yield frame  # np.array()
            finally:
                cap.release()


# Iterator for the marquee
def draw_marquee_frames(width: int, height: int) -> np.array:
    # Image and Draw context
    image = Image.fromarray(np.zeros((height, width, 4), dtype=np.uint8))
    draw = ImageDraw.Draw(image)

    # Text and font
    text = get_prices_from_json()
    font = ImageFont.truetype(os.path.join("src/fonts", "LEDBDREV.TTF"), 32)
    text_width, text_height = draw.textsize(text, font)
    # Initial position and speed
    x, y = width, (height - text_height) // 2  # center of screen (x,y)
    speed = 1

    while True:
        # Move the text
        x -= speed
        if x < -text_width:
            x = width

        # Draw the marquee and yield each step
        draw.rectangle((0, 0, width, height), fill=(0, 0, 0, 255))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        yield np.array(image)


def play_video_loop():
    video_iter = get_background_video_frames()
    first_frame = next(video_iter)
    marquee_iter = draw_marquee_frames(first_frame.shape[1], first_frame.shape[0])

    while True:
        frame_bg = next(video_iter)
        frame_marquee = next(marquee_iter)[..., :3]

        # Combine the two frames
        frame =  cv2.bitwise_or(frame_marquee, frame_bg)

        # Show the frame
        cv2.imshow("Video", frame)

        #  Exit on Esc key press
        if cv2.waitKey(1) == 27:
            exit()


def main():
    play_video_loop()


if __name__ == "__main__":
    main()
