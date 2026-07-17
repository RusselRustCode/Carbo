"""
Интеграция Контура данных с Контуром управления.

Демонстрирует полный цикл:
1. Получение task_id из API (или эмуляция)
2. Загрузка сырых данных в Bronze с привязкой к task_id
3. ETL в Silver
4. Валидация результата
"""
import uuid
from data_pipeline.ingestion import ingest_soil_csv
from data_pipeline.etl import process_bronze_to_silver
from data_pipeline.validation import validate_silver


def run_full_pipeline(csv_path: str, task_id: str | None = None) -> dict:
    """
    Полный пайплайн: Bronze → Silver → Validation.

    Args:
        csv_path: Путь к локальному CSV файлу
        task_id: UUID задачи из Контура управления.
                 Если None — генерируется автоматически.

    Returns:
        dict с ключами: task_id, bronze_key, silver_key
    """
    if task_id is None:
        task_id = str(uuid.uuid4())
        print(f"Generated task_id: {task_id}")
    else:
        print(f"Using existing task_id: {task_id}")

    print("\n" + "=" * 60)
    print("STEP 1: INGESTION (Bronze)")
    print("=" * 60)
    bronze_key = ingest_soil_csv(csv_path, task_id)

    print("\n" + "=" * 60)
    print("STEP 2: ETL (Bronze → Silver)")
    print("=" * 60)
    silver_key = process_bronze_to_silver(bronze_key, task_id)

    print("\n" + "=" * 60)
    print("STEP 3: VALIDATION")
    print("=" * 60)
    validate_silver(silver_key, bronze_key)

    return {
        "task_id": task_id,
        "bronze_key": bronze_key,
        "silver_key": silver_key,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.integration <csv_path> [task_id]")
        print("\nExample with real task_id from API:")
        print("  python -m data_pipeline.integration tests/data/soil_probes_batch1.csv 123e4567-e89b-12d3-a456-426614174000")
        sys.exit(1)

    csv_path = sys.argv[1]
    task_id = sys.argv[2] if len(sys.argv) > 2 else None

    result = run_full_pipeline(csv_path, task_id)

    print("\n" + "=" * 60)
    print("🏁 PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Task ID:    {result['task_id']}")
    print(f"  Bronze:     {result['bronze_key']}")
    print(f"  Silver:     {result['silver_key']}")
    print("=" * 60)