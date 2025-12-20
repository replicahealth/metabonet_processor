from glupredkit.parsers.diatrend import Parser as DiaTrendParser
from glupredkit.parsers.ohio_t1dm import Parser as OhioT1DMParser
from glupredkit.parsers.open_aps import Parser as OpenAPSParser
from glupredkit.parsers.t1dexi import Parser as T1DEXIParser
from glupredkit.parsers.tidepool_dataset import Parser as TidepoolParser
from pathlib import Path
import pandas as pd

DATASETS = ["DiaTrend",
            "OhioT1DM",
            "OpenAPS",
            "t1dexi",
            "Tidepool",
            ]
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

def discover_available_datasets(raw_dir: Path = RAW_DIR):
    found = []
    for folder in raw_dir.iterdir():
        if folder.is_dir() and folder.name in DATASETS:
            found.append(folder.name)
    return found


def get_parser(dataset_name: str):
    parsers = {
        "DiaTrend": DiaTrendParser,
        "OhioT1DM": OhioT1DMParser,
        "OpenAPS": OpenAPSParser,
        "t1dexi": T1DEXIParser,
        "Tidepool": TidepoolParser,
    }
    if dataset_name not in parsers:
        raise ValueError(f"No parser available for dataset: {dataset_name}")
    return parsers[dataset_name]()


def postprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names and ordering.
    Adjust this based on your expected schema.
    """
    expected_order = [
        'CGM', 'absorption_time', 'acceleration', 'age', 'air_temp', 'basal', 'bolus', 'calories_burned',
        'carbs', 'cgm_device', 'context_description_cache', 'date', 'galvanic_skin_response', 'heartrate',
        'height', 'id', 'insulin', 'insulin_delivery_algorithm', 'insulin_delivery_device',
        'insulin_delivery_modality', 'insulin_type_basal', 'insulin_type_bolus', 'is_pregnant', 'is_test',
        'meal_label', 'scheduled_basal', 'skin_temp', 'source_file', 'steps', 'tag', 'weight',
        'workout_duration', 'workout_intensity', 'workout_label', 'treatment_group', 'randomization_date',
        'extension_date', 'gender', 'age_of_diagnosis', 'TDD', 'ethnicity'
    ]

    print(df.head())

    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()

        # Ensure the new column is named "date"
        if df.columns[0] != "date":
            df = df.rename(columns={df.columns[0]: "date"})

        print("Finished processing datetime index into date column: ", df.head())

    # Ensure all expected columns exist (or fill with NaN)
    for col in expected_order:
        if col not in df.columns:
            df[col] = pd.NA

    # Reorder
    df = df[expected_order]

    # Sort by timestamp, remove duplicates, etc.
    df = df.sort_values("date").drop_duplicates()

    return df.reset_index(drop=True)


def main():
    datasets = discover_available_datasets()
    print(f"Found datasets: {datasets}")
    for ds in datasets:
        parser = get_parser(ds)
        if ds in ['DiaTrend', 'OhioT1DM']:
            raw_path = RAW_DIR
        else:
            raw_path = RAW_DIR / ds
        print(f"Parsing {ds} from {raw_path} ...")

        if ds == 'Tidepool':
            for prefix in ['HCL150', 'SAP100', 'PA50']:
                raw_path_str = str(raw_path) + "/"
                df = parser(file_path=raw_path_str, prefix=prefix)
                df = postprocess_df(df)

                processed_path = (PROCESSED_DIR / f"{ds}-JDRF-{prefix}").with_suffix(".parquet")
                df.to_parquet(processed_path)
                print(f"Saved processed {ds}-{prefix} to {processed_path}.")
        elif ds == 'OhioT1DM':
            ids_2018 = ['559', '563', '570', '575', '588', '591']
            ids_2020 = ['540', '544', '552', '567', '584', '596']

            merged_df = pd.DataFrame()

            def add_subject_to_df(subject_id, year):
                parsed_data = parser(file_path=raw_path, subject_id=subject_id, year=year)
                parsed_data['id'] = subject_id
                return pd.concat([parsed_data, merged_df], ignore_index=False)

            for subject_id in ids_2018:
                merged_df = add_subject_to_df(subject_id, '2018')

            for subject_id in ids_2020:
                merged_df = add_subject_to_df(subject_id, '2020')

            merged_df = postprocess_df(merged_df)
            processed_path = (PROCESSED_DIR / ds).with_suffix(".parquet")
            merged_df.to_parquet(processed_path)
            print(f"Saved processed {ds} to {processed_path}.")
        elif ds == 't1dexi':
            suffixes = ["T1DEXIP.zip", "T1DEXI.zip"]
            files = [
                file
                for file in raw_path.iterdir()
                if file.is_file() and file.name.endswith(tuple(suffixes))
            ]
            for file_path in files:
                file_path_str = str(file_path)
                df = parser(file_path=file_path_str)
                df = postprocess_df(df)

                file_name = 'T1DEXI' if 'T1DEXI.zip' in file_path else 'T1DEXIP'
                processed_path = (PROCESSED_DIR / file_name).with_suffix(".parquet")
                df.to_parquet(processed_path)
                print(f"Saved processed {ds} to {processed_path}.")
        else:
            df = parser(file_path=str(raw_path) + "/")
            df = postprocess_df(df)
            processed_path = (PROCESSED_DIR / ds).with_suffix(".parquet")
            df.to_parquet(processed_path)
            print(f"Saved processed {ds} to {processed_path}.")

    return


if __name__ == "__main__":
    results = main()
    print("Completed parsing.")

