import os
import re

folder = r"output_chunks\Pending\ran_cate_19"

files = os.listdir(folder)

rename_list = []

for file in files:

    match = re.match(r"chunk_(\d+)(\.\w+)", file)

    if match:
        num = int(match.group(1))
        ext = match.group(2)

        if num >= 29:  # -----------------------------------
            rename_list.append((num, ext, file))

# STEP 1: temp rename
for num, ext, old_file in rename_list:

    old_path = os.path.join(folder, old_file)
    temp_path = os.path.join(folder, f"temp_{num}{ext}")

    os.rename(old_path, temp_path)

# STEP 2: final rename (SAFE overwrite)
for num, ext, _ in rename_list:

    temp_path = os.path.join(folder, f"temp_{num}{ext}")

    new_num = num - 1  # -----------------------------------
    new_path = os.path.join(folder, f"chunk_{new_num}{ext}")

    # ⚠️ important fix
    if os.path.exists(new_path):
        os.remove(new_path)

    os.rename(temp_path, new_path)

    print(f"chunk_{num} → chunk_{new_num}")

print("Done!")
