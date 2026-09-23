import os
import numpy as np
import parselmouth
from parselmouth.praat import call
from scipy.signal import iirfilter, sosfilt

# PATH CONFIGURATION

INPUT_ROOT_DIR = r"D:\.Restricted .file\Code\Thesis\demo\dataset"
OUTPUT_ROOT_DIR = r"D:\.Restricted .file\Code\Thesis\demo\Pitch_Changed_Dataset"

TARGET_SR = 16000


# ANONYMIZATION HYPERPARAMETERS

RHO_1_FORMANT = 1.08  # Formant shift
RHO_2_PITCH = 1.05  # Pitch scale


def apply_parametric_eq(data, sr=16000):
    sos_hp = iirfilter(
        N=2, Wn=80, fs=sr, btype="highpass", ftype="butter", output="sos"
    )
    filtered = sosfilt(sos_hp, data)

    sos_notch = iirfilter(
        N=1,
        Wn=[280, 320],
        fs=sr,
        btype="bandstop",
        ftype="butter",
        output="sos",
    )
    filtered = sosfilt(sos_notch, filtered)

    # Presence/Clarity Boost
    sos_peak = iirfilter(
        N=2,
        Wn=[3000, 4000],
        fs=sr,
        btype="bandpass",
        ftype="butter",
        output="sos",
    )
    presence_band = sosfilt(sos_peak, filtered)

    # Clarity Boost Blend
    output = filtered + (presence_band * 0.25)

    # Peak Normalization
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.95

    return output


# SINGLE FILE ANONYMIZATION
def anonymize_single_audio(input_file, output_file):
    sound = parselmouth.Sound(input_file)

    if sound.get_number_of_channels() > 1:
        sound = call(sound, "Convert to mono")

    if sound.sampling_frequency != TARGET_SR:
        sound = sound.resample(TARGET_SR)

    modified_sound = call(
        sound,
        "Change gender",
        75,
        600,
        RHO_1_FORMANT,
        0,
        RHO_2_PITCH,
        1.0,
    )

    audio_data = modified_sound.values[0]  # Mono Channel Data Array

    eq_audio_data = apply_parametric_eq(audio_data, sr=TARGET_SR)

    final_sound = parselmouth.Sound(eq_audio_data, sampling_frequency=TARGET_SR)
    final_sound.save(output_file, "WAV")


# BATCH DIRECTORY PROCESSING SCRIPT
def process_audio_directory(input_root, output_root):
    processed_count = 0
    failed_count = 0

    print("Starting processing with 16kHz Mono Formant Shift + Pitch Scaling + EQ...\n")

    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.lower().endswith(".wav"):
                input_file_path = os.path.join(root, file)

                relative_path = os.path.relpath(input_file_path, input_root)
                output_file_path = os.path.join(output_root, relative_path)

                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                try:
                    anonymize_single_audio(input_file_path, output_file_path)
                    processed_count += 1
                    print(f"[PROCESSED - 16kHz Mono] -> {relative_path}")

                except Exception as e:
                    failed_count += 1
                    print(f"[ERROR] Failed {relative_path}: {e}")

    print("\n-------------------------------------------")
    print("Batch Processing Complete!")
    print(f"Total Files Processed Successfully: {processed_count}")
    print(f"Total Files Failed: {failed_count}")
    print(f"Output Directory: {output_root}")


if __name__ == "__main__":
    process_audio_directory(INPUT_ROOT_DIR, OUTPUT_ROOT_DIR)
