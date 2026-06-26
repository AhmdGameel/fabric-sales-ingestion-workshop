from notebookutils import mssparkutils

# Get all CSV files from the landing folder
files = [
    f for f in mssparkutils.fs.ls("Files/landing")
    if f.name.lower().endswith(".csv")
]

if len(files) == 0:
    print("No new CSV files found in landing.")

else:
    # Read all CSV files
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("Files/landing/*.csv")
    )

    # Create the table if it doesn't exist, otherwise append
    if spark.catalog.tableExists("sales"):
        df.write.mode("append").format("delta").saveAsTable("sales")
    else:
        df.write.mode("overwrite").format("delta").saveAsTable("sales")

    print(f"Processed {len(files)} file(s).")

    # Archive processed files
    for file in files:
        source = file.path
        destination = f"Files/archive/{file.name}"

        mssparkutils.fs.cp(source, destination)
        mssparkutils.fs.rm(source, False)

        print(f"Archived: {file.name}")

    print("Pipeline completed successfully.")
