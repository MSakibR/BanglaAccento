"""
# for folder wise access
import os
import subprocess

RAW_DIR = "ooo"
PROCESSED_DIR = "Others_Processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

# auto-detect regions
regions = os.listdir(RAW_DIR)

for region in regions:
    input_folder = os.path.join(RAW_DIR, region)
    output_folder = os.path.join(PROCESSED_DIR, region)

    if not os.path.isdir(input_folder):
        continue

    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file)

        # skip non-files
        if not os.path.isfile(input_path):
            continue

        # force output .wav
        filename_wo_ext = os.path.splitext(file)[0]
        output_path = os.path.join(output_folder, filename_wo_ext + ".wav")

        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ac", "1",        # mono
            "-ar", "16000",    # 16 kHz
            "-vn",             # ignore video if exists
            output_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("All audio converted successfully!")

"""

"""
project/
│
├── convert.py
│
└── raw/
      ├── Sylhet/
      │     ├── a.mp3
      │     ├── b.wav
      │
      ├── Rangpur/
      │     ├── x.m4a

Processed/
│
├── Sylhet/
│     ├── a.wav
│     ├── b.wav
│
├── Rangpur/
      ├── x.wav
"""

# for 1 folder access
import os
import subprocess

RAW_DIR = "raw"
PROCESSED_DIR = "Others_Processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

for file in os.listdir(RAW_DIR):

    input_path = os.path.join(RAW_DIR, file)

    # skip non-files
    if not os.path.isfile(input_path):
        continue

    # filename without extension
    filename_wo_ext = os.path.splitext(file)[0]

    # output wav path
    output_path = os.path.join(PROCESSED_DIR, filename_wo_ext + ".wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        "-vn",
        output_path,
    ]

    print(f"Converting: {file}")

    subprocess.run(cmd)

print("All audio converted successfully!")

"""
project/
│
├── convert.py
│
└── raw/
      ├── a.mp3
      ├── b.wav
      ├── x.m4a


Others_Processed/
│
├── a.wav
├── b.wav
├── x.wav
"""
