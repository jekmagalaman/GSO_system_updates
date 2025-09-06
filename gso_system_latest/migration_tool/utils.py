import pandas as pd

def process_migration(file_path, target_model):
    """
    Reads Excel/CSV and inserts data into the target model.
    """
    # Auto-detect file type
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Insert each row into the target model
    for _, row in df.iterrows():
        target_model.objects.create(**row.to_dict())
