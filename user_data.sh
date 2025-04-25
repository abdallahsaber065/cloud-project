#!/bin/bash
# Use shebang for execution context
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "Starting User Data Script"

# Update the system
yum update -y
yum install python3 python3-pip git -y
pip3 install --upgrade pip

# Get Application Code
cd /home/ec2-user
git clone https://github.com/abdallahsaber065/cloud-project.git app
cd app

# Set Environment Variables
export S3_BUCKET_NAME="file-share-app-project-bucket-000" 
export AWS_REGION="eu-north-1" 

# Persist environment variables for the ec2-user session
echo "export S3_BUCKET_NAME=${S3_BUCKET_NAME}" >> /home/ec2-user/.bashrc
echo "export AWS_REGION=${AWS_REGION}" >> /home/ec2-user/.bashrc

# Install Application Dependencies
pip3 install -r requirements.txt

# Run Application
echo "Starting Flask app via Waitress on port 80"
sudo -u ec2-user sh -c "export S3_BUCKET_NAME='${S3_BUCKET_NAME}'; export AWS_REGION='${AWS_REGION}'; waitress-serve --host 0.0.0.0 --port 80 app:app > /var/log/webapp.log 2>&1 &"

echo "User Data Script Finished"