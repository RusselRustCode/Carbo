import uuid
from datetime import datetime, timezone
from pathlib import Path
from data_pipeline.s3_client import S3Storage

def ingest_soil_csv(local_file_path: str, task_id: str | None = None) -> str:
    if not Path(local_file_path).exists():
        raise FileExistsError(f"File not found: {local_file_path}")

    if task_id is None:
        task_id = str(uuid.uuid4())

    now = datetime.now(timezone.utc)
    year = now.strftime("%Y")
    month = now.strftime("%m")

    filename = Path(local_file_path).stem
    object_key = f"bronze/lab_soil/year={year}/month={month}/task_{task_id}_{filename}_raw.csv"

    storage = S3Storage()
    storage.ensure_bucket()
    storage.upload_file(local_file_path, object_key)

    return object_key

if __name__ == "__main__":
    # Быстрый тест: загрузить файл вручную
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.ingestion <path_to_csv> [task_id]")
        sys.exit(1)

    csv_path = sys.argv[1]
    tid = sys.argv[2] if len(sys.argv) > 2 else None
    
    key = ingest_soil_csv(csv_path, tid)
    print(f"\n Bronze ingestion complete: {key}")
