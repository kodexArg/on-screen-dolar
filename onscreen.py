import os
import cv2
import PIL.ImageFont
from loguru import logger


def get_price_rate():
    # should be imported from prices.json
    data = {
        "dolar oficial": "$238.00",
        "euro oficial": "$329.19",
        "pesos chilenos": "$3.09",
        "dolar informal": "$411.00",
    }
    return data


# draw the exchange rate board using cv2 and PIL TrueType fonts
def draw_price_board(frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (250, 250, 250)
    spacing_v = 50
    spacing = 300
    margin_left = 50
    margin_top = 20
    tickness = 2

    data = get_price_rate()

    for i in range(4):
        currency = list(data.keys())[i]
        price = list(data.values())[i]
        cv2.putText(frame, currency, (margin_left, margin_top + (i + 1) * spacing_v), font, font_scale, color, tickness)
        cv2.putText(
            frame, price, (margin_left + spacing, margin_top + (i + 1) * spacing_v), font, font_scale, color, tickness
        )


# iterator for background video (return: cap)
def get_video_capture_object():
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
        for video_capture_object in get_video_capture_object():  # cycle through all the backgrounds videos
            while True:  # cycle through frames
                ret, frame = video_capture_object.read()
                if not ret:
                    break

                draw_price_board(frame)
                cv2.imshow("Video", frame)

                key = cv2.waitKey(30)
                if key == 27:
                    exit()


def main():
    play_video_loop()


if __name__ == "__main__":
    main()
