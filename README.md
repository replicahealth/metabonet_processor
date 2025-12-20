# Process Data

This module supports processing **Data Use Agreement-governed datasets** into the **MetaboNet format**.

The following datasets are supported:

- DiaTrend
- OhioT1DM
- OpenAPS
- T1DEXI
- Tidepool Data Donation

---


## 1. Install Dependencies

First, create and activate a **virtual environment** using the desired Python version.

### Using Python 3.9–3.11:

```bash
# Create a virtual environment named 'venv' 
python -m venv venv

# Activate the virtual environment
# On macOS/Linux
source venv/bin/activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

## 1. Install dependencies

Make and activate virtual environment.

```
pip install -r requirements.txt
```



## 2. Prepare the Raw Data

Raw datasets must be accessed through their respective application processes. After obtaining the raw data, move the dataset folders into the data/raw directory. Make sure that the raw data folders are renamed to match the following folder structure:
```
    process_data/
    ├── data/
    │   └── raw/
    │       └── DiaTrend
    │       └── OhioT1DM
    │       └── OpenAPS
    │       └── t1dexi
    │           └── T1DEXI.zip
    │           └── T1DEXIP.zip
    │       └── Tidepool
    └── run.py
```
> **Important:** Ensure that the folder names match exactly as shown above.

## 3. Run Processing 

Run the main processing script:
```
python run.py 
```
The script will process all datasets located in `data/raw` and save the output to `data/processed`.

## Citation

To cite this work please use:
[LINK WILL COME WHEN MANUSCRIPT IS PUBLISHED]

