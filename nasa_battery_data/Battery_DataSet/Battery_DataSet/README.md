# Battery_DataSet (Unified)

This folder is a unified copy of the NASA battery aging dataset files used in this project.

## What Is In This Folder

- MAT files: `B0005.mat` through `B0056.mat` (available battery IDs in this collection).
- Group README files: experiment descriptions by battery group.
- `source.md`: source overview file from the dataset package.

## Important Note

The MAT file internal data structure is consistent across groups, but experiment conditions differ by group (temperature, discharge profile/current, cutoff voltages, and stop criteria). Use the group README files for metadata.

## Group Documentation Files

- `README_05_06_07_18.txt`
- `README_25_26_27_28.txt`
- `README_29_30_31_32.txt`
- `README_33_34_36.txt`
- `README_38_39_40.txt`
- `README_41_42_43_44.txt`
- `README_45_46_47_48.txt`
- `README_49_50_51_52.txt`
- `README_53_54_55_56.txt`

## Suggested Starting Workflow

1. Keep this folder as the canonical input path for all scripts.
2. Build a manifest table (`battery_id`, `file_path`, `group_readme`, key test conditions).
3. Parse MAT files into cycle-level tabular data (charge/discharge/impedance).
4. Add metadata from the matching group README to every parsed record.
5. Save cleaned outputs to a separate processed folder (for example, `data_processed/`).
6. Start modeling only after metadata joins are complete.


