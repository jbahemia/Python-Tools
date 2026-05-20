# ClearLineLocks.py

> **Dependency:** `clear_HIPS_line_locks.exe` (developed by Teledyne CARIS)

This tool clears **HIPS line locks** on all `.hips` files in folders within a specified project directory.

### How it works:
- User is prompted to input:
  - The **parent project folder**
  - The path to **clear_HIPS_line_locks.exe**
- The script processes all `.hips` folders found within the project
- Outputs a **results text file** in the parent directory

---

## csar_band_stats.py

> **Requirements:** Python 3.11, NumPy, CARIS API

This tool uses the **CARIS API** (path configured near the top of the script) to process CSAR files.

### Functionality:
- Loads CSAR files from a specified folder
- Converts data into **NumPy arrays**
- Calculates statistics for **predefined bands**
- Exports results to a **text file**
``
