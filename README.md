# Microsoft Fabric Sales Ingestion Workshop

Resources for my **Global Fabric Day** workshop.

## What you'll find

* Sample sales CSV files
* PySpark Notebook code
* Simple end-to-end ingestion demo using Microsoft Fabric

## Architecture

```text
CSV Files
    │
    ▼
OneLake (Landing)
    │
    ▼
Notebook (PySpark)
    │
    ▼
Lakehouse (sales)
    │
    ▼
Archive
```

## Files

* **data/** → Sample CSV files
* **notebook/** → Notebook code used in the workshop

## Steps

1. Create a Fabric Workspace.
2. Create a Lakehouse.
3. Create **landing** and **archive** folders.
4. Upload the CSV files to **Files/landing**.
5. Create a Notebook and copy the code from `notebook/Load_Sales_to_Lakehouse.py`.
6. Add the Notebook to a Data Pipeline.
7. Run the Pipeline.

The notebook will:

* Load all CSV files into the **sales** table.
* Create the table if it doesn't exist.
* Append new records.
* Move processed files to the **archive** folder.

---

**Author:** Ahmed Gamel
