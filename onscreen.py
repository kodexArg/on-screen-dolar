import os
import cv2
import json
import PIL.ImageFont
from loguru import logger


def get_price_rate():
    data = json.load(open(os.path.join("src", "prices.json")))
    return data


def draw_price_board(frame):
    font_path = os.path.join("src", "led_8x6.ttf")
    font_size = 32
    font = PIL.ImageFont.truetype(font_path, font_size)
    font_scale = 1
    color = (250, 250, 250)
    spacing_v = 50
    column_spacing = 300
    margin_left = 50
    margin_top = 20
    tickness = 2

    loc_currency = (margin_left, margin_top + (i + 1) * spacing_v)
    loc_price = (margin_left + column_spacing, margin_top + (i + 1) * spacing_v)

    data = get_price_rate()

    for i in range(4):
        currency = list(data.keys())[i]
        price = list(data.values())[i]
        # Currency
        cv2.putText(frame, currency, loc_currency, font, font_scale, color, tickness)
        # Value in ARS
        cv2.putText(frame, price, loc_price, font, font_scale, color, tickness)


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
    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def play_video_loop():
    while True:
        for cap in get_video_capture_object():  # cycle through videos in src folder
            set_video_to_full_screen(cap)
            while True:  # cycle through each video frame
                ret, frame = cap.read()
                if not ret:
                    break
                draw_price_board(frame)
                cv2.imshow("Video", frame)
                key = cv2.waitKey(30)
                if key == 27:  # Esc
                    exit()


def main():
    play_video_loop()


if __name__ == "__main__":
    main()
