import os
import shutil

def remove_pycache(start_dir='.'):
    for dirpath, dirnames, filenames in os.walk(start_dir):
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")

# Call the function to remove all __pycache__ directories
remove_pycache()
