
# GENERAL
CONTENT_PATH = './content'
CONTENT_IMAGES_PATH = CONTENT_PATH + '/images'
CONTENT_SOUND_PATH = CONTENT_PATH + '/music'
CONTENT_DEFAULT_PATH = CONTENT_PATH + '/default'
CREDENTIALS_PATH = "./credentials"

# FOR CONTENT
MAX_SENTENCES_TO_FETCH = 5
WIKIPEDIA_MAIN_URL = "https://{}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&exlimit=1&titles={}&explaintext=1&formatversion=2&media=1"

# FOR VIDEO
VIDEO_INTRODUCTION_TEXT = "Robby\napresenta..."
VIDEO_SCREENSIZE = (1920,1080)
VIDEO_TEXT_COLOR_DEFAULT = 'white'
VIDEO_TEXT_FONT_DEFAULT = 'helvetica'
VIDEO_FONT_SIZE_DEFAULT = 50
VIDEO_TEXT_POSITION_DEFAULT = 'center'
VIDEO_FRAME_DURATION_DEFAULT = 4
VIDEO_TEXT_KERNING_DEFAULT = 5
VIDEO_CODEC_DEFAULT = 'mpeg4'
VIDEO_FPS_DEFAULT = 30

# FOR YOUTUBE
YOUTUBE_CATEGORY_LIST = [
        (1, 'Film & Animation'),
        (2, 'Autos & Vehicles'),
        (10, 'Music'),
        (15, 'Pets & Animals'),
        (17, 'Sports'),
        (18, 'Short Movies'),
        (19, 'Travel & Events'),
        (20, 'Gaming'),
        (21, 'Videoblogging'),
        (22, 'People & Blogs'),
        (23, 'Comedy'),
        (24, 'Entertainment'),
        (25, 'News & Politics'),
        (26, 'Howto & Style'),
        (27, 'Education'),
        (28, 'Science & Technology'),
        (29, 'Nonprofits & Activism'),
        (30, 'Movies'),
        (31, 'Anime/Animation'),
        (32, 'Action/Adventure'),
        (33, 'Classics'),
        (34, 'Comedy'),
        (35, 'Documentary'),
        (36, 'Drama'),
        (37, 'Family'),
        (38, 'Foreign'),
        (39, 'Horror'),
        (40, 'Sci-Fi/Fantasy'),
        (41, 'Thriller'),
        (42, 'Shorts'),
        (43, 'Shows'),
        (44, 'Trailers')
    ]