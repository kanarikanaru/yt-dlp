import yt_dlp
import json
import sys

# Patch to log API responses
orig_extract_response = yt_dlp.extractor.youtube._base.YoutubeBaseInfoExtractor._extract_response

def debug_extract_response(self, *args, **kwargs):
    print("\n[DEBUG] _extract_response query:", json.dumps(kwargs.get('query'), ensure_ascii=False), file=sys.stderr)
    res = orig_extract_response(self, *args, **kwargs)
    keys = list(res.keys()) if isinstance(res, dict) else type(res)
    print("[DEBUG] _extract_response got keys:", keys, file=sys.stderr)
    return res

yt_dlp.extractor.youtube._base.YoutubeBaseInfoExtractor._extract_response = debug_extract_response

# Patch to log daterange checks
orig_match_entry = yt_dlp.YoutubeDL._match_entry

def debug_match_entry(self, info_dict, *args, **kwargs):
    result = orig_match_entry(self, info_dict, *args, **kwargs)
    date = info_dict.get('upload_date')
    print(f"[DEBUG] match_entry id={info_dict.get('id')} upload_date={date} result={result}", file=sys.stderr)
    return result

yt_dlp.YoutubeDL._match_entry = debug_match_entry

channel_id = sys.argv[1] if len(sys.argv) > 1 else 'UCqwNLpNEtNf7PYc_Kh7SOMw'

# Use a wide daterange to demonstrate dateafter
ydl_opts = {
    'skip_download': True,
    'quiet': False,
    'verbose': True,
    'dateafter': '20230101',  # example start date
    'lazy_playlist': True,
    'break_on_reject': True,
    'extract_flat': True,
    'extractor_args': {'youtubetab': {'approximate_date': ['true']}},
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'https://www.youtube.com/channel/{channel_id}'])
