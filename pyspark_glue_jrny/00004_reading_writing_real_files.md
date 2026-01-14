
### What's Next? Reading & Writing Real Files (Very Important for Glue)
In AWS Glue, most of your data comes from files in **S3** (CSV, JSON, Parquet, etc.), and you write cleaned results back to S3.

Let's simulate that locally first — it's almost identical code when you move to Glue.

**Step 1: Create a sample CSV in your local notebooks folder**
- In JupyterLab (file browser on left) → right-click → New → Text File
- Name it `sales_data.csv`
- Paste this content and save:
  ```
  Name,Age,Job,Salary,City
  Alice,28,Engineer,85000,Austin
  Bob,35,Manager,120000,Dallas
  Charlie,22,Intern,45000,Houston
  Dana,40,Director,180000,Plano
  Eve,,Analyst,95000,Frisco
  Frank,32,Sales,75000,Plano
  ```

**Step 2: Read CSV in PySpark (new cell)**

```python
# Read from local folder (mounted volume)
df_from_csv = spark.read.option("header", "true") \
                        .option("inferSchema", "true") \
                        .csv("/home/jovyan/work/sales_data.csv")

df_from_csv.show()
df_from_csv.printSchema()   # See data types Spark guessed
```

**Step 3: Clean & Write as Parquet (Glue loves Parquet!)**

```python
# Same cleaning as before
df_clean_csv = df_from_csv \
    .withColumn("Senior", when(col("Age") >= 30, "Yes").otherwise("No")) \
    .withColumn("Bonus", col("Salary") * lit(0.10)) \
    .na.fill({"Age": 25})

# Write to Parquet (partitioned by City - common in Glue)
df_clean_csv.write.mode("overwrite") \
             .partitionBy("City") \
             .parquet("/home/jovyan/work/clean_sales_parquet")

print("Done! Check your local 'notebooks/clean_sales_parquet' folder")
```

After running:
- Stop your container if you want (Containers tab → Stop)
- In File Explorer, go to `C:\pyproj\learning_lib\pyspark_glue_jrny\notebooks\clean_sales_parquet`
- You'll see Parquet files + folders by City (e.g. `City=Austin/`, `City=Plano/`) — this is exactly how Glue stores partitioned data in S3!

### Why This Matters for AWS Glue
When you write real Glue PySpark jobs, the code looks **almost the same**, except:
```python
# In Glue instead of local path
df = glueContext.create_dynamic_frame.from_catalog(database="my_db", table_name="sales_raw")
# ... transformations ...
glueContext.write_dynamic_frame.from_options(
    frame=df_clean,
    connection_type="s3",
    connection_options={"path": "s3://my-bucket/clean/sales/"},
    format="parquet"
)
```

So you're already practicing the exact transformations Glue uses!

Want to:
- Try JSON instead of CSV?
- Add more complex cleaning (e.g. split full name, handle dates)?
- Simulate a small Glue job locally with `aws-glue-libs` container?
- Move to real AWS next (create S3 bucket + crawler)?

Just say the word! You're doing fantastic — keep going! 🚀