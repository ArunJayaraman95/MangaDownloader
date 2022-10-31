import shutil
import os
import time

srcPath = r"C:\Users\ripar\Desktop\LuckyTemplate"
worldPath = r"C:\Users\ripar\AppData\Roaming\.minecraft\saves\LuckyWorld"

# shutil.copytree(src_path, test_path)
# shutil.move(src_path, test_path, copy_function = shutil.copytree)

# Deletes used world
shutil.rmtree(worldPath)
time.sleep(1) # Delay just for debugging

# Copies lucky block template to minecraft world
shutil.copytree(srcPath, worldPath)

print("HI")
