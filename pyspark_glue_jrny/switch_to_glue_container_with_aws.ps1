# Stop and remove the existing Glue container to re-launch with credentials
Write-Host "Stopping existing container 'glue_jupyter_lab'..."
docker stop glue_jupyter_lab
docker rm glue_jupyter_lab

# Define image and paths
$glueImage = "amazon/aws-glue-libs:glue_libs_4.0.0_image_01"
$awsDir = "$env:USERPROFILE\.aws"

Write-Host "Starting new container with AWS Credentials mounted..."

# Run the new container
# - Mounts existing 'pyspark_data' volume (Code/Data)
# - Mounts local .aws directory to /home/glue_user/.aws (Credentials)
# - Sets AWS_PROFILE environment variable to 'study'
docker run -itd `
    -p 8888:8888 `
    -p 4040:4040 `
    --name glue_jupyter_lab `
    -v pyspark_data:/home/glue_user/workspace/jupyter_workspace `
    -v ${awsDir}:/home/glue_user/.aws `
    -e AWS_PROFILE=study `
    -e DISABLE_SSL=true `
    $glueImage `
    /home/glue_user/jupyter/jupyter_start.sh

Write-Host "Container started! Access Jupyter Lab at: http://localhost:8888"
Write-Host "AWS Profile 'study' is now active inside the container."
