import os
import cv2
import json
import time
import numpy as np
import configuration as cfg
from PIL import Image, ImageDraw, ImageFont
from loguru import logger


def get_ms() -> int:
    return int(round(time.time() * 1000))


def get_prices_from_json() -> str:
    """Returns a single string with the prices from 'src/prices.json' file"""
    prices_dict = json.load(open(os.path.join("src", "prices.json")))
    return "     ".join([f"{key}: {value}" for key, value in prices_dict.items()])


def set_video_to_full_screen(video_capture_object) -> None:
    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def draw_bg_video_iter() -> np.array:
    """Returns an iterator with the background video frames in bgr format.

    Raises:
        RuntimeError: Error opening video file

    Yields:
        Iterator[np.array]: a frame of the movie
    """
    src_dir = "src"
    video_files = os.listdir(src_dir)
    for video_file in video_files:
        if not video_file.endswith(".mp4"):
            continue

        video_file_path = os.path.join(src_dir, video_file)
        logger.info(f"Loading {video_file_path}")
        cap = cv2.VideoCapture(video_file_path)

        if not cap.isOpened():
            raise RuntimeError(f"Error opening video file '{video_file_path}'")
        try:
            # Get the width and height of the video
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Create an empty RGBA image
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

            # Main Loop cycling through frames of the video
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert the frame from BGR to RGBA
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                yield frame  # np.array()
        finally:
            cap.release()


def draw_marquee_frames_iter(width: int, height: int) -> np.array:
    # Image and Draw context
    image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Text and font
    text = get_prices_from_json()
    font = ImageFont.truetype(cfg.FONT, cfg.FONT_SIZE)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Initial position and speed
    x, y = width, (height - text_height - cfg.TEXT_BOTTOM)
    speed = cfg.SPEED

    while True:
        starting_time = get_ms()

        # Move the text
        x -= speed
        if x < -text_width:
            x = width

        # Clear
        draw.rectangle((0, 0, width, height), fill=0)

        # Creates a new image in grayscale ("L") and fill white color
        text_image = Image.new("L", (text_width, text_height), color=0)

        # Drawing context for text_image and creates the text
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), text, font=font, fill=255)

        # Combine text with background
        image.paste(text_image, (x, y), text_image)

        # Sleep until next frame is ready. FPS default 25 ms
        finish_time = get_ms()
        if starting_time + cfg.FPS > finish_time:
            time.sleep((starting_time + cfg.FPS - finish_time) / 1000.0)

        # Marquee frame in a 4 dmiension array
        yield np.array(image)


def play_video_loop() -> None:
    # TODO: timer for every frame
    video_iter = draw_bg_video_iter()
    first_frame = next(video_iter)
    height, width = first_frame.shape[:2]

    marquee_iter = draw_marquee_frames_iter(width, height)
    set_video_to_full_screen(first_frame)

    while True:
        frame_bg = next(video_iter)
        frame_marquee = next(marquee_iter)

        # Band of marquee size
        band_top = height - cfg.BAND_BOTTOM
        band_low = height - cfg.BAND_TOP

        frame_bg[band_low: band_top] = frame_bg[band_low: band_top] * .5


        # Alpha blending

        frame = cv2.addWeighted(frame_bg, 1, frame_marquee, 1, 0)

        # Show the frame
        cv2.imshow("Video", frame)

        #  Exit on Esc key press
        if cv2.waitKey(1) == 27:
            exit()


def main() -> None:
    play_video_loop()


if __name__ == "__main__":
    main()
