import subprocess


def check_ffmpeg() -> None:
    subprocess.run(["ffmpeg", "-version"])
