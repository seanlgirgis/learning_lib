# Stop and remove the existing generic PySpark container
Write-Host "Stopping existing container 'my-pyspark-lab'..."
docker stop my-pyspark-lab
docker rm my-pyspark-lab

# Pull the AWS Glue image (Glue 4.0 / Spark 3.3)
# This image contains the AWS Glue libraries, PySpark, and Jupyter
$glueImage = "amazon/aws-glue-libs:glue_libs_4.0.0_image_01"
Write-Host "Pulling AWS Glue image: $glueImage (This may take a few minutes)..."
docker pull $glueImage

# Run the new container
# - Maps port 8888 for Jupyter and 4040 for Spark UI
# - Mounts the EXISTING 'pyspark_data' volume to the Glue workspace so you don't lose files
# - Sets DISABLE_SSL=true to allow HTTP access to Jupyter (easier for local dev)
# - runs the jupyter_start.sh script to boot up the lab
Write-Host "Starting new container 'glue_jupyter_lab'..."
docker run -itd `
    -p 8888:8888 `
    -p 4040:4040 `
    --name glue_jupyter_lab `
    -v pyspark_data:/home/glue_user/workspace/jupyter_workspace `
    -e DISABLE_SSL=true `
    $glueImage `
    /home/glue_user/jupyter/jupyter_start.sh

Write-Host "Container started! Access Jupyter Lab at: http://localhost:8888"
Write-Host "Note: Your existing notebooks should appear in the file browser."
