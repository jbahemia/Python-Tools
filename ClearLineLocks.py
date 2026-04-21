import os
import subprocess
from tkinter import Tk, filedialog

# Hide the main tkinter window
Tk().withdraw()

# Prompt user to select the parent folder
parent_folder = filedialog.askdirectory(title="Select the parent folder to search for .hips files")
if not parent_folder:
    print("No folder selected. Exiting.")
    exit(1)

# Prompt user to select the exe file
exe_path = filedialog.askopenfilename(title="Select the .exe file to run", filetypes=[("Executable files", "*.exe")])
if not exe_path:
    print("No exe selected. Exiting.")
    exit(1)

# Output file for collated results
output_file = os.path.join(parent_folder, "hips_processing_output.txt")

# Find all .hips files
hips_files = []
for root, dirs, files in os.walk(parent_folder):
    for file in files:
        if file.lower().endswith('.hips'):
            hips_files.append(os.path.join(root, file))

if not hips_files:
    print("No .hips files found.")
    exit(0)

with open(output_file, 'w', encoding='utf-8') as out_f:
    total_files = len(hips_files)
    for idx, hips_file in enumerate(hips_files, 1):
        print(f"Processing file {idx} of {total_files}: {hips_file}")
        out_f.write(f"\n--- Output for: {hips_file} ---\n")
        try:
            # Pass the .hips file path as a plain argument (no extra quotes)
            result = subprocess.run([exe_path, hips_file], capture_output=True, text=True, check=False)
            out_f.write(result.stdout)
            if result.stderr:
                out_f.write("\n[stderr]:\n" + result.stderr)
        except Exception as e:
            out_f.write(f"\n[Exception running {hips_file}]: {e}\n")
        out_f.write("\n--- End of output ---\n")

print(f"Processing complete. Output saved to: {output_file}")
