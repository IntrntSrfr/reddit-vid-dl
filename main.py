import os
import re
import sys

import requests

full_regex = re.compile("^http(s)?([^\s]+)reddit\.com\/r\/([^\s]+)\/comments\/([^\s]+)\/([^\s]+)")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def validate_link(link: str) -> bool:
    return True


def validate_json(j: str) -> bool:
    pass


def get_media_links(url: str) -> tuple[str, str, str]:
    link_json = url + '.json'
    res = requests.get(link_json, headers={'User-Agent': user_agent})

    # if request failed
    if not res.ok:
        raise requests.HTTPError

    res_json = res.json()

    post = res_json[0]['data']['children'][0]['data']

    if not post['is_video']:
        raise ValueError('post does not contain video')

    if not post['is_reddit_media_domain']:
        raise ValueError('post is not Reddit video')

    media = post['secure_media']

    if 'reddit_video' not in media:
        raise ValueError('post is not Reddit video')

    video_url = media['reddit_video']['fallback_url']
    audio_url = post['url'] + '/DASH_audio.mp4'
    out = post['id']+'.mp4'

    return video_url, audio_url, out


def download(url: str, **kwargs) -> None:

    if not validate_link(url):
        raise Exception("invalid reddit link")

    # get the links and outfile
    video_url, audio_url, out = get_media_links(url)

    # if there is an outfile specified, just override the name from the post
    if 'outfile' not in kwargs:
        out = kwargs['outfile']

    # use ffmpeg to save file
    os.system('ffmpeg -i {} -i {} -c copy {}'.format(video_url, audio_url, out))


def main():
    if len(sys.argv) < 2:
        return
    inp_url = sys.argv[1]
    f = ''
    if len(sys.argv) >= 3:
        f = sys.argv[2]

    if not f.endswith('.mp4'):
        f += '.mp4'

    try:
        download(inp_url, outfile='weed.mp4')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
