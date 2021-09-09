# Cam-check

Quick-n-dirty Flask app that shows a catalog of video (.mp4) files with the 
ability to preview each one, and cull it if not very interesting.

I have 4.5Tb of unwatched video footage from the garden wildlife camera.

## Starting

1. Install dependencies with [pipenv]():

```console
$ pipenv install
```

2. Link the file location where the videos are to `static/data`, eg:

```console
$ ln -s /export/media/Camera/ftp-uploads static/data
````

3. For development, ensure you are running inside a `venv`, with something like:

```console
$ pipenv shell
$ FLASK_ENV=development flask run
```

4. Browse to http://localhost:5000/. Note: For the .mp4 files my camera produces,
   only Safari seems to correctly display the video files. 