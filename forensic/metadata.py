from pymediainfo import MediaInfo
import os


def metadata_check(file):

    media = MediaInfo.parse(file)

    result = {}


    file_size = os.path.getsize(file)


    result["file_size_mb"] = round(
        file_size / (1024 * 1024),
        2
    )


    for track in media.tracks:


        if track.track_type == "General":

            if track.format:

                result["format"] = (
                    track.format
                )


            if track.overall_bit_rate:

                try:

                    result["bitrate_kbps"] = round(
                        float(
                            track.overall_bit_rate
                        ) / 1000,
                        2
                    )

                except:

                    pass


        elif track.track_type == "Video":

            result["codec"] = (
                track.codec_id
                or
                track.format
                or
                "-"
            )


            result["resolution"] = (
                f"{track.width}x{track.height}"
            )


            if track.frame_rate:

                result["frame_rate"] = (
                    track.frame_rate
                )


            if track.duration:

                try:

                    result["duration_seconds"] = round(
                        float(track.duration)
                        / 1000,
                        2
                    )

                except:

                    pass


        elif track.track_type == "Audio":

            result["audio_codec"] = (
                track.codec_id
                or
                track.format
                or
                "-"
            )


            if track.sampling_rate:

                result["sample_rate"] = (
                    track.sampling_rate
                )


            if track.channel_s:

                result["audio_channels"] = (
                    track.channel_s
                )


    return result