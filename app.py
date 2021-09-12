import os
import time
from typing import Dict, List
from flask import Flask, request, render_template, redirect
from pathlib import Path

app = Flask(__name__)


def get_files(path: str) -> List[Dict[str, str]]:
    return [
        dict(filename=file, stat=os.stat(os.path.join("static/data", path, file)))
        for file in sorted(os.listdir(os.path.join("static/data", path)))
        if file.endswith(".mp4")
        or os.path.isdir(os.path.join("static/data", path, file))
    ]


def index_of(arr: List[Dict[str, str]], filename) -> int:
    return [item["filename"] for item in arr].index(filename)


@app.route("/<path:parent>/<string:file>.mp4")
def file(parent: str, file: str):
    files = get_files(parent)
    index = index_of(files, f"{file}.mp4")
    count = len(files)
    prev = files[index - 1]["filename"] if index > 0 else None
    next = files[index + 1]["filename"] if index + 1 < count else None
    time = f"{file[-6:-4]}:{file[-4:-2]}:{file[-2:]}"
    return render_template(
        "file.html",
        parent=parent,
        index=index + 1,
        count=count,
        file=f"{file}.mp4",
        time=time,
        next=next,
        prev=prev,
    )


@app.route("/")
@app.route("/<path:path>/")
def folder(path: str = ""):
    parent = Path(path).parent
    return render_template(
        "folder.html",
        path=path,
        parent=None if str(parent) == "." else parent,
        videos=get_files(path),
    )


@app.route("/delete-file", methods=["POST"])
def delete_file():
    file = request.form["file"]
    path = os.path.join("static/data", file)
    basename = os.path.basename(path)

    parent = Path(file).parent
    files = get_files(parent)
    index = index_of(files, basename)
    count = len(files)
    if index + 1 < count:
        next = files[index + 1]["filename"]
    elif index > 0:
        next = files[index - 1]["filename"]
    else:
        next = None

    print(f"Deleting file: {path}")
    os.rename(path, f"static/data/trash/{basename}")

    return redirect(f"/{parent}/{next}" if next else f"/{parent}", code=302)


@app.template_filter("ctime")
def timectime(s):
    return time.ctime(s)  # datetime.datetime.fromtimestamp(s)
