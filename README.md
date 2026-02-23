# MetaboNet Processor

A data processing tool for converting **Data Use Agreement-governed datasets** into the **[MetaboNet](https://metabo-net.org/) format**.

> **Note**: All public datasets within MetaboNet are immediately available as a single consolidated file on the [MetaboNet website](https://metabo-net.org/). This processor is intended for the subset of MetaboNet that consists of Data Use Agreement-governed datasets.

## Overview

This module standardizes diabetes-related datasets into a unified format compatible with the MetaboNet ecosystem. It processes continuous glucose monitoring (CGM), insulin delivery, meal, and physiological data from multiple research datasets.

## Supported Datasets and Access

Raw datasets must be obtained through their respective data sharing agreements:

- **DiaTrend**: [Nature Scientific Data publication](https://www.nature.com/articles/s41597-023-02469-5)
- **OhioT1DM**: Available through [OhioT1DM Dataset](https://webpages.charlotte.edu/rbunescu/data/ohiot1dm/OhioT1DM-dataset.html)
- **OpenAPS**: Request access through [OpenAPS Data Commons](https://openaps.org/outcomes/data-commons/)*
- **T1DEXI**: Apply through [Vivli T1D Exercise Data RFP](https://search.vivli.org/?search=t1dexi)
- **Tidepool**: Access through [Tidepool Big Data Donation](https://www.tidepool.org/bigdata)

> **Important**: Each dataset requires separate approval. Follow institutional guidelines for data use agreements.

*This processing script is based on OpenAPS when n=181. This dataset is continuously evolving, and we cannot guarantee that this processing works for all versions of the dataset.

## Prerequisites

- **Python**: 3.9–3.11 
- **Operating System**: macOS, Linux, or Windows
- **Memory**: Minimum 4GB RAM recommended for large datasets
- **Storage**: Sufficient space for both raw and processed datasets

## Installation

### 1. Create Virtual Environment

```bash
# Create a virtual environment named 'venv' 
python -m venv venv

# Activate the virtual environment
# On macOS/Linux
source venv/bin/activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```


## Data Preparation

After obtaining raw data, organize it according to this structure:

```
metabonet_processor/
├── data/
│   ├── raw/
│   │   ├── DiaTrend/
│   │   ├── OhioT1DM/
│   │   ├── OpenAPS/
│   │   ├── t1dexi/
│   │   │   ├── T1DEXI.zip
│   │   │   └── T1DEXIP.zip
│   │   └── Tidepool/
│   └── processed/
└── run.py
```

> **Critical**: Folder names must match exactly as shown above (case-sensitive).

## Usage

### Basic Processing

Process all available datasets:

```bash
python run.py
```

The script will:
1. Automatically discover datasets in `data/raw/`
2. Parse each dataset using the appropriate parser
3. Standardize column names and data types
4. Save processed files to `data/processed/` as Parquet files

### Output

The harmonization process converts datasets into a single table with:
- **Homogeneous 5-minute intervals**: All data points are standardized to 5-minute time intervals
- **Parquet format**: Efficient storage and fast loading for analysis
- **Standardized schema**: Unified column names and data types across all datasets

For the complete list of features and schema details, see the [MetaboNet website](https://metabo-net.org/).


## Troubleshooting

### Common Issues

**"No parser available for dataset"**
- Ensure dataset name matches exactly (case-sensitive)
- Check that the dataset is uncommented in `DATASETS` list

**"FileNotFoundError"**
- Verify raw data folder structure matches requirements
- Ensure dataset folders are placed in `data/raw/`

**"Memory Error"**
- Process datasets individually by commenting others in `DATASETS`
- Increase available system memory

**"Permission Error"**
- Check file permissions on data directories
- Ensure write access to `data/processed/`

### Getting Help

For additional support:
- Check the [MetaboNet documentation](https://metabo-net.org/)
- Review dataset-specific documentation
- Contact your institutional data manager for DUA questions

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Citation

To cite this work, please use:
[LINK WILL COME WHEN MANUSCRIPT IS PUBLISHED]

---

**Note**: This tool processes sensitive health data. Ensure compliance with all applicable data use agreements and institutional policies.
