import os
import re
import sys

import requests

full_regex = re.compile("http(s)?([^\s]+)reddit\.com\/r\/([^\s]+)\/comments\/([^\s]+)\/([^\s]+)")


def validate_link(link: str) -> bool:
    return True


def get_media_links(url: str) -> tuple[str, str, str]:
    link_json = url + '.json'
    res = requests.get(link_json, headers={'User-Agent': 'hehe'})
    res_json = res.json()
    post_info = res_json[0]['data']['children'][0]['data']
    video_url = post_info['secure_media']['reddit_video']['fallback_url']
    audio_url = post_info['url'] + '/DASH_audio.mp4'
    out = post_info[id]+'.mp4'
    return video_url, audio_url, out


def download(url: str, **kwargs) -> None:
    if not validate_link(url):
        raise Exception("invalid reddit link")
    video_url, audio_url, out = get_media_links(url)
    if 'outfile' not in kwargs:
        out = kwargs['outfile']
    os.system('ffmpeg -i {} -i {} -c copy {}'.format(video_url, audio_url, out))


test_case = "https://reddit.com/r/PublicFreakout/comments/oey7po/iranian_woman_not_wearing_a_hijab_is_harrassed_by/"

if __name__ == '__main__':
    inp_url = sys.argv[1]
    f = sys.argv[2]

    if not f.endswith('.mp4'):
        f += '.mp4'

    try:
        download(inp_url, f)
    except Exception as e:
        print(e)
