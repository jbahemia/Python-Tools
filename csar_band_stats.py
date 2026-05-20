import sys
import os
import numpy as np

# Add CARIS Python API to sys.path
sys.path.append(r"C:\Program Files\CARIS\HIPS and SIPS\11.4\python\3.11")

from caris.coverage import Raster




# Prompt for surface type
surface_type = input("Type CUBE or SDTP to select surface type: ").strip().upper()
if surface_type == "CUBE":
    bands_to_check = ["Depth", "Uncertainty", "Std_Dev"]
    print("CUBE selected. Bands: Depth, Uncertainty, Std_Dev")
elif surface_type == "SDTP":
    bands_to_check = [
        "Depth",
        "Density",
        "Depth_TPU",
        "Position_TPU",
        "Depth_TPU_Compliance",
        "Position_TPU_Compliance",
        "Std_Dev"
    ]
    print("SDTP selected. Bands: Depth, Density, Depth_TPU, Position_TPU, Depth_TPU_Compliance, Position_TPU_Compliance, Std_Dev")
else:
    print("Invalid selection. Please run the script again and type CUBE or SDTP.")
    exit(1)

# Prompt for folder
csar_folder = input("Enter the folder path containing CSAR files: ").strip()
summary_path = os.path.join(csar_folder, "csar_band_stats_summary.csv")

with open(summary_path, "w") as summary:
    summary.write("File,Band,Min,Max,Mean,StdDev\n")
    for fname in os.listdir(csar_folder):
        if fname.lower().endswith(".csar"):
            csar_path = os.path.join(csar_folder, fname)
            print(f"Processing {fname}")
            try:
                raster = Raster(csar_path)
                # Only process the bands for the selected surface type
                for band_name in bands_to_check:
                    try:
                        arr = np.array(raster.read(band_name=band_name, area=((0,0), raster.dims), level=raster.highest_level), dtype=float)
                        arr = arr[~np.isnan(arr)]
                        # Exclude very large values (likely NoData/fill values)
                        # Try to get NoData value from raster or band
                        no_data = None
                        for attr in ["no_data_value", "nodata", "nodata_value", "noDataValue"]:
                            if hasattr(raster, attr):
                                no_data = getattr(raster, attr)
                                break
                        if no_data is None and hasattr(raster, "metadata"):
                            meta = getattr(raster, "metadata")
                            if isinstance(meta, dict):
                                for k in meta:
                                    if "nodata" in k.lower():
                                        no_data = meta[k]
                                        break
                        if no_data is None:
                            no_data = 1e30
                        arr = arr[arr != no_data]
                        arr = arr[arr < 1e30]  # still filter out huge values just in case
                        # Special handling for Density band: always filter 4294967295 and -9999
                        if band_name.lower() == "density":
                            arr = arr[(arr != 4294967295) & (arr != -9999)]
                        # Only invert z-axis for Depth band
                        if band_name.lower() == "depth":
                            arr = -arr
                        if arr.size > 0:
                            min_val = np.min(arr)
                            max_val = np.max(arr)
                            mean_val = np.mean(arr)
                            stddev_val = np.std(arr)
                            # Format to 3 decimal places
                            min_val = f"{min_val:.3f}"
                            max_val = f"{max_val:.3f}"
                            mean_val = f"{mean_val:.3f}"
                            stddev_val = f"{stddev_val:.3f}"
                        else:
                            min_val = max_val = mean_val = stddev_val = 'NaN'
                        summary.write(f"{fname},{band_name},{min_val},{max_val},{mean_val},{stddev_val}\n")
                    except Exception as band_e:
                        print(f"  Band {band_name} not found or could not be read in {fname}: {band_e}")
                # Write separator after each surface
                summary.write("---\n")
            except Exception as e:
                print(f"Failed to process {fname}: {e}")

print(f"Summary written to {summary_path}")
