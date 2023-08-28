from typing import Any

import ffmpeg
from recall_me.logging import logger


class Ogg2WavConverter:
    def __init__(self) -> None:
        self.ffmpeg_process = (
            ffmpeg.input("pipe:", format="ogg")
            .output("pipe:", format="wav")
            .run_async(pipe_stdin=True, pipe_stdout=True)
        )

    def __str__(self) -> str:
        return "[Ogg2Wav]"

    def __enter__(self) -> "Ogg2WavConverter":
        return self

    def __exit__(self, *_args: Any) -> None:
        self.ffmpeg_process.stdin.close()

    def convert(self, ogg_bytearray: bytearray) -> bytes:
        out_buf, _ = self.ffmpeg_process.communicate(bytes(ogg_bytearray))
        logger.debug(f"{self}: wav buffer size: {len(out_buf)} bytes")
        return out_buf
        # wav_buf = BytesIO()
        # for chunk in self._convert(ogg_bytearray):
        #     wav_buf.write(chunk)

        # wav_buf.seek(0)
        # return bytes(wav_buf.getbuffer())

    # def _convert(self, ogg_bytearray: bytearray) -> Iterator[bytes]:
    # chunk_size = (
    #     1024  # Define chunk size to 1024 bytes (the exacts size is not important).
    # )
    # ogg_len: int = len(ogg_bytearray)
    # n_chunks = (
    #     ogg_len // chunk_size
    # )  # Number of chunks (without the remainder smaller chunk at the end).
    # remainder_size = (
    #     ogg_len % chunk_size
    # )  # Remainder bytes (assume total size is not a multiple of chunk_size).

    # logger.debug(f"{self}: {chunk_size = }, {n_chunks = }, {remainder_size = }")

    # for i in range(n_chunks):
    #     logger.debug(f"{self}: stdin: write {i} chunk")
    #     self.ffmpeg_process.stdin.write(
    #         ogg_bytearray[i * chunk_size : (i + 1) * chunk_size]
    #     )  # Write chunk of data bytes to stdin pipe of FFmpeg sub-process.
    #     self.ffmpeg_process.stdin.flush()
    #     logger.debug(f"{self}: stdout: read {i} chunk")
    #     yield self.ffmpeg_process.stdout.read(1024)

    # if remainder_size > 0:
    #     logger.debug(f"{self}: stdin: write {remainder_size} bytes")
    #     self.ffmpeg_process.stdin.write(
    #         ogg_bytearray[chunk_size * n_chunks :]
    #     )  # Write remainder bytes of data bytes to stdin pipe of FFmpeg sub-process.
    #     self.ffmpeg_process.stdin.flush()
    #     logger.debug(f"{self}: stdout: read {remainder_size} bytes")
    #     yield self.ffmpeg_process.stdout.read(remainder_size)

    # rem = self.ffmpeg_process.communicate()[0]
    # if rem:
    #     logger.debug(f"{self}: very last stdout bytes: {len(rem)}")
    #     yield rem
    #     # rem = self.ffmpeg_process.stdout.read()
