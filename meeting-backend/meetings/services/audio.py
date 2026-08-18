import subprocess


class InvalidAudioError(Exception):
    pass


def validate_audio_with_ffprobe(file_path):
    print("===== VALIDATION AUDIO APPELEE =====")
    print("FICHIER :", file_path)

    probe_command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]

    probe_result = subprocess.run(
        probe_command,
        capture_output=True,
        text=True,
    )

    print("FFPROBE CODE :", probe_result.returncode)
    print("FFPROBE OUTPUT :", probe_result.stdout)
    print("FFPROBE ERROR :", probe_result.stderr)

    codec = probe_result.stdout.strip()

    if probe_result.returncode != 0 or not codec:
        raise InvalidAudioError(
            "Le fichier fourni n'est pas un audio valide."
        )

    decode_command = [
        "ffmpeg",
        "-v",
        "error",
        "-i",
        str(file_path),
        "-t",
        "5",
        "-f",
        "null",
        "-",
    ]

    decode_result = subprocess.run(
        decode_command,
        capture_output=True,
        text=True,
    )

    print("FFMPEG CODE :", decode_result.returncode)
    print("FFMPEG ERROR :", decode_result.stderr)

    if decode_result.returncode != 0:
        raise InvalidAudioError(
            "Le fichier est corrompu ou ne contient pas un audio valide."
        )

    return True


def get_audio_duration(file_path):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise InvalidAudioError(
            "Impossible de déterminer la durée du fichier audio."
        )

    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise InvalidAudioError(
            "Durée audio invalide."
        ) from exc