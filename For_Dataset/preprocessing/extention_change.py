import os
import subprocess
import re

folder = "data/Others"
out_folder = "data/Others/pre"

os.makedirs(out_folder, exist_ok=True)

for file in os.listdir(folder):

    # match .1 .2 .3 etc
    if re.search(r"\.\d+$", file):

        input_path = os.path.join(folder, file)

        base_name = re.sub(r"\.\d+$", "", file)  # chi_cate_8

        version = file.split(".")[-1]  # 1,2,3

        output_name = f"{base_name}_{version}.wav"

        output_path = os.path.join(out_folder, output_name)

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

        subprocess.run(cmd)

print("Done")
