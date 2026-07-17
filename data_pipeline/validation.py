from data_pipeline.s3_client import S3Storage
import pandas as pd
def validate_silver(silver_key: str, bronze_key: str | None = None) -> bool:
    """
    Читает Parquet из Silver, выводит схему, статистику и сравнивает размер с Bronze.
    Возвращает True если валидация пройдена, False иначе.
    """
    storage = S3Storage()
    silver_buffer = storage.download_to_buffer(silver_key)

    df = pd.read_parquet(silver_buffer)

    print("=" * 60)
    print(f"Silver file: {silver_key}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("=" * 60)

    print("\nSchema (Data Types):")
    print(df.dtypes.to_string())

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    print("\nNull counts per column:")
    nulls = df.isnull().sum()
    print(nulls[nulls > 0].to_string() if nulls.any() else "  (no nulls)")

    # Сравнение размеров (пропускаем для маленьких файлов)
    silver_size = silver_buffer.getbuffer().nbytes

    if bronze_key:
        bronze_buffer = storage.download_to_buffer(bronze_key)
        bronze_size = bronze_buffer.getbuffer().nbytes
        
        if bronze_size > 10240:  # Только для файлов > 10KB
            ratio = (1 - silver_size / bronze_size) * 100
            print(f"\nBronze size: {bronze_size / 1024:.1f} KB")
            print(f"Silver size: {silver_size / 1024:.1f} KB")
            print(f"Compression: {ratio:.1f}% smaller")
        else:
            print(f"\nSilver size: {silver_size / 1024:.1f} KB")
            print("File too small for compression benchmark (<10KB)")
    else:
        print(f"\nSilver size: {silver_size / 1024:.1f} KB")

    # Проверка типов (совместимая с Pandas 2.x)
    expected_types = {
        "sample_date": "datetime64",      
        "ph_level": "float64",
        "carbon_content_(%)": "float64",
        "nitrogen_(mg/kg)": "float64",
    }
    
    print("\nType validation:")
    all_ok = True
    for col, expected_prefix in expected_types.items():
        if col not in df.columns:
            print(f" {col}: MISSING (expected {expected_prefix})")
            all_ok = False
            continue
            
        actual = str(df[col].dtype)
        ok = actual.startswith(expected_prefix)
        status = "OK" if ok else "NOT OK"
        print(f"  {status} {col}: {actual} (expected {expected_prefix}*)")
        if not ok:
            all_ok = False

    if all_ok:
        print("\nAll validations passed!")
    else:
        print("\nSome validations failed!")
    
    return all_ok