import requests
import re
import os
import sys

class Grabber:
    def __init__(self) -> None:
        self.full_regex = re.compile("http(s)?([^\s]+)reddit\.com\/r\/([^\s]+)\/comments\/([^\s]+)\/([^\s]+)")
    
    def validate_link(self, link:str)->bool:
        return True
    
    def get_media_links(self, link:str) -> tuple[str, str, str]:
        link_json = link + '.json'
        res = requests.get(link_json, headers={'User-Agent':'hehe'})
        res_json = res.json()
        post_info = res_json[0]['data']['children'][0]['data']
        video_url = post_info['secure_media']['reddit_video']['fallback_url']
        audio_url = post_info['url']+'/DASH_audio.mp4'
        out = post_info[id]
        return (video_url, audio_url, out)

    def download(self, link:str, outfile:str) -> None:
        if not self.validate_link(link):
            raise Exception("invalid reddit link")
        video_url, audio_url, out = self.get_media_links(link)
        os.system('ffmpeg -i {} -i {} -c copy {}'.format(video_url, audio_url, out))

test_case = "https://reddit.com/r/PublicFreakout/comments/oey7po/iranian_woman_not_wearing_a_hijab_is_harrassed_by/"

if __name__ == '__main__':
    link = sys.argv[1]
    f = sys.argv[2]

    if not f.endswith('.mp4'):
        f+='.mp4'
        
    g = Grabber()
    try:
        g.download(link, f)
    except Exception as e:
        print(e)