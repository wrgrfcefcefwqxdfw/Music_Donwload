def validate_youtube_link(link):
    if link.startswith("https://www.youtube.com/") or link.startswith('https://youtu.be/'):
        return True
    else:
        return False
