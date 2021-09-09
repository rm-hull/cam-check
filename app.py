from typing import List
from flask import Flask
from flask import render_template
import os
from pathlib import Path

app = Flask(__name__)


def get_videos(path: str) -> List[str]:
    return sorted(
        file
        for file in os.listdir(os.path.join("static/data", path))
        if file.endswith(".mp4") or os.path.isdir(os.path.join("static/data", path, file))
    )


@app.route('/<path:parent>/<string:file>.mp4')
def file(parent: str, file: str):
    videos = get_videos(parent)
    index = videos.index(f"{file}.mp4")
    count = len(videos)
    prev = videos[index - 1] if index > 0 else None
    next = videos[index + 1] if index + 1 < count else None
    time = f"{file[-6:-4]}:{file[-4:-2]}:{file[-2:]}"
    return render_template('file.html',
                           parent=parent,
                           index=index + 1,
                           count=count,
                           file=f"{file}.mp4",
                           time=time,
                           next=next,
                           prev=prev)


@app.route('/')
@app.route('/<path:path>/')
def folder(path: str = ''):
    parent = Path(path).parent
    return render_template('folder.html',
                           path=path,
                           parent=None if str(parent) == '.' else parent,
                           videos=get_videos(path))
