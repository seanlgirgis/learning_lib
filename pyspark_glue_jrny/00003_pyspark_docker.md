Great choice going the **Docker route** — it's clean, reproducible, and avoids polluting your local machine with Java/Spark versions. Since you're new to PySpark and want ease + quick feedback, the **best beginner-friendly option in 2026** is to use a **Jupyter Notebook** environment with PySpark pre-installed. This way you can write, run, and see results immediately in a nice browser interface (no terminal hassle for the first days).

### Recommended Setup: jupyter/pyspark-notebook (Still Excellent & Maintained via quay.io)

This is the classic, most straightforward image for learning PySpark locally.

**Why this one?**
- Comes with JupyterLab + PySpark + Spark pre-configured
- You get a beautiful notebook where you can play interactively
- No need to install Java, Spark, or anything else on your host machine
- Very popular and stable for beginners

**Step-by-step (takes ~5-10 minutes)**

1. **Make sure Docker Desktop is running**  
   Open Docker Desktop — it should show the whale icon in your system tray/menu bar.

2. **Pull the image** (use the updated quay.io location — official recommendation now)  
   Open your terminal (PowerShell on Windows, Terminal on Mac/Linux) and run:

   ```bash
   docker pull quay.io/jupyter/pyspark-notebook:latest
   ```

   (This pulls the latest version — usually Spark 3.5.x or newer in 2026)

3. **Run the container** (this is the magic one-liner):

   ```bash
   docker run -it --rm \
       -p 8888:8888 \
       -p 4040:4040 \
       -v "${PWD}/notebooks":/home/jovyan/work/notebooks \
       quay.io/jupyter/pyspark-notebook:latest
   ```

   What each part means (super simple):
   - `-it --rm` → interactive + auto-delete when you stop (clean)
   - `-p 8888:8888` → Jupyter notebook in browser
   - `-p 4040:4040` → Spark UI (very useful to see jobs running)
   - `-v "${PWD}/notebooks":/home/jovyan/work/notebooks` → your current folder's "notebooks" subfolder will be shared inside the container (create the "notebooks" folder first if you want)

   **Windows tip**: If you're on Windows and `${PWD}` doesn't work, replace it with full path like `-v "C:/Users/YourName/projects/notebooks":/home/jovyan/work/notebooks`

4. **Open Jupyter in your browser**  
   After running the command, Docker will print something like:

   ```
   http://127.0.0.1:8888/lab?token=super-long-token-here
   ```

   Copy-paste that URL into your browser (Chrome/Firefox/Edge).  
   → You'll land in JupyterLab!

5. **Create your first notebook and test PySpark**  
   - Click **Python 3 (ipykernel)** to create a new notebook
   - In the first cell, paste and run (Shift+Enter):

     ```python
     from pyspark.sql import SparkSession

     spark = SparkSession.builder \
         .appName("MyFirstDockerPySpark") \
         .getOrCreate()

     print("Spark version:", spark.version)

     # Quick test DataFrame
     data = [("Alice", 25), ("Bob", 30), ("Charlie", 22)]
     df = spark.createDataFrame(data, ["Name", "Age"])
     df.show()
     ```

   You should see the Spark version and a nice little table!

   Also open http://localhost:4040 in another tab — you'll see the Spark Web UI showing your jobs.

### Bonus Tips for Smooth Sailing

- **Stop the container**: Press Ctrl+C in the terminal
- **Restart later**: Just run the same `docker run` command again
- **Want to keep the container alive longer?** Remove `--rm` and give it a name:
  ```bash
  docker run -d --name my-spark-jupyter \
      -p 8888:8888 -p 4040:4040 \
      -v "${PWD}/notebooks":/home/jovyan/work/notebooks \
      quay.io/jupyter/pyspark-notebook:latest
  ```
  Then stop/start with `docker stop my-spark-jupyter` and `docker start my-spark-jupyter`

- **Install extra Python packages** (pandas, etc.):
  Inside the notebook → run cell:
  ```python
  !pip install pandas matplotlib
  ```

- **Next level (optional later)**: Use docker-compose for a mini Spark cluster (1 master + workers), but **don't do it yet** — single container Jupyter is perfect for learning basics.

Once you can create DataFrames, filter, groupBy, join, and read/write CSV/Parquet in the notebook → you're ready to move to AWS Glue (the code will be almost identical!).

Let me know when you get the notebook open — we can then do your first real mini-project (like cleaning a sample CSV) right there! 🚀