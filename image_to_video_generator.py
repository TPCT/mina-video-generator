from configparser import ConfigParser
from sys import platform
from multiprocessing import freeze_support
from requests import post
from os import listdir, makedirs
import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile
import uuid


config_parser = ConfigParser()
config_parser.read('Settings.ini')

IMAGES_PER_VIDEO = config_parser.getint('GENERIC', 'IMAGES_PER_VIDEO')
VIDEOS_COUNT = config_parser.getint("GENERIC", "VIDEOS_COUNT")
VIDEO_LENGTH = config_parser.getint("GENERIC", "VIDEO_LENGTH")

USERNAME = config_parser.get('LICENCE', 'USERNAME')

if platform.startswith('win'):
    freeze_support()

APPLICATION_NAME = "videos_generator"
APPLICATION_VERSION = "1"
mac_address = uuid.getnode()
mac_address_hex = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])

print(r"""
 _   _ ___________ _____ _____ _____   _____  _____ _   _  ___________  ___ _____ ___________ 
| | | |_   _|  _  \  ___|  _  /  ___| |  __ \|  ___| \ | ||  ___| ___ \/ _ \_   _|  _  | ___ \
| | | | | | | | | | |__ | | | \ `--.  | |  \/| |__ |  \| || |__ | |_/ / /_\ \| | | | | | |_/ /
| | | | | | | | | |  __|| | | |`--. \ | | __ |  __|| . ` ||  __||    /|  _  || | | | | |    / 
\ \_/ /_| |_| |/ /| |___\ \_/ /\__/ / | |_\ \| |___| |\  || |___| |\ \| | | || | \ \_/ / |\ \ 
 \___/ \___/|___/ \____/ \___/\____/   \____/\____/\_| \_/\____/\_| \_\_| |_/\_/  \___/\_| \_|

DEV: TPCT
FACEBOOK: https://www.facebook.com/taylor.ackerley.9/
MOBILE: +201094950765
""")

domain = "https://licence.shiftcodes.net"

message_response = post(f'{domain}/api/v1/add_application', data={
    'username': USERNAME,
    'server_mac_address': mac_address_hex,
    'application_name': APPLICATION_NAME,
    'application_version': APPLICATION_VERSION,
}).json()

if post(f'{domain}/api/v1/check_verification', data={
    'username': USERNAME,
    'server_mac_address': mac_address,
    'application_name': APPLICATION_NAME,
    'application_version': APPLICATION_VERSION,
}).status_code != 200:
    print(message_response['message']) if message_response['show_message'] else None
    input("Contact Developer")
    exit(0)

images = []
# audios = []

for file in listdir("./images"):
    images.append("./images/" + file)


# for file in listdir("./audios"):
#     audios.append("./audios/" + file)

image_index = 0
video_index = 0
makedirs('./videos', exist_ok=True)

ImageFile.LOAD_TRUNCATED_IMAGES = True


def generateVideo():
    global image_index, video_index
    accumulated_length = 0
    video_images = []

    while accumulated_length < VIDEO_LENGTH:
        start_index = image_index
        for i in range(IMAGES_PER_VIDEO):
            image_path = images[start_index % len(images)]
            image = Image.open(image_path)
            image = image.resize((640, 480))
            image.save(image_path)
            video_images.extend([image_path for i in range(30)])
            accumulated_length += 1
            start_index += 1

    image_index = start_index

    video_index += 1
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(video_images, fps=30)
    clip.write_videofile(f"./videos/{video_index}.mp4")


for i in range(VIDEOS_COUNT):
    generateVideo()