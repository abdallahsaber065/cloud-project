import os
import boto3
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
import datetime

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flash messages

S3_BUCKET = os.environ.get(
    "S3_BUCKET_NAME", "file-share-app-project-bucket-000"
)  

# Update region to match your CLI region
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1") 

# File type validation
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

# Remove the print statements that expose credential information
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Create S3 client with explicit credential handling and correct endpoint configuration
if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    s3_client = boto3.client(
        "s3", 
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        # Explicitly set the endpoint URL to match the region
        endpoint_url=f"https://s3.{AWS_REGION}.amazonaws.com"
    )
    print("Using explicitly provided AWS credentials")
else:
    # Fall back to default credential resolution with correct endpoint
    s3_client = boto3.client(
        "s3", 
        region_name=AWS_REGION,
        # Explicitly set the endpoint URL to match the region
        endpoint_url=f"https://s3.{AWS_REGION}.amazonaws.com"
    )
    print(f"Using default AWS credential chain with region: {AWS_REGION}")

# Add a test to verify credentials are working
try:
    s3_client.list_buckets()
    print("AWS credentials are valid - successfully connected to AWS")
except Exception as e:
    print(f"AWS credential validation failed: {e}")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Renders the main upload page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles the file upload process."""
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Sanitize filename
        try:
            # Option 1: Upload with public read ACL (Simpler for direct links, less secure)
            # s3_client.upload_fileobj(
            #     file,
            #     S3_BUCKET,
            #     filename,
            #     ExtraArgs={'ACL': 'public-read'}
            # )
            # download_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"

            # Option 2: Upload private and generate Presigned URL (More secure)
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                filename,
                # No ACL needed if bucket is private and accessed via presigned URL
            )

            # Generate a presigned URL for temporary access (expires in 3600 seconds = 1 hour)
            download_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": S3_BUCKET, "Key": filename},
                ExpiresIn=3600,  # URL expiry time in seconds
            )

            flash(f'File "{filename}" uploaded successfully!')
            return render_template(
                "result.html", download_url=download_url, filename=filename
            )

        except NoCredentialsError:
            error_msg = "AWS credentials not found. Please check your environment variables or AWS config files."
            app.logger.error(error_msg)
            flash(error_msg)
            return redirect(url_for("index"))
        except ClientError as e:
            error_msg = f"Failed to upload file: {e}"
            app.logger.error(f"S3 Upload Error: {e}")
            flash(error_msg)
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}")
            app.logger.error(f"Unexpected Error: {e}")
            return redirect(url_for("index"))

    else:
        flash("File type not allowed.")
        return redirect(url_for("index"))


# Function to list files in the S3 bucket
def list_uploaded_files():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            files = [
                {
                    'filename': obj['Key'],
                    'last_modified': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                    'size': obj['Size']
                }
                for obj in response['Contents']
            ]
            return files
        else:
            return []
    except ClientError as e:
        app.logger.error(f"Failed to list files: {e}")
        return []


@app.route("/files")
def files():
    """Renders a page displaying uploaded files."""
    uploaded_files = list_uploaded_files()
    return render_template("files.html", files=uploaded_files)


@app.route("/search")
def search():
    """Renders the search page."""
    return render_template("search.html")


@app.route("/feedback")
def feedback():
    """Renders the feedback page."""
    return render_template("feedback.html")


@app.route("/download/<filename>")
def download_file(filename):
    """Generate a presigned URL for downloading a specific file."""
    try:
        # Generate a presigned URL for temporary access (expires in 3600 seconds = 1 hour)
        download_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": filename},
            ExpiresIn=3600,  # URL expiry time in seconds
        )
        return redirect(download_url)
    except Exception as e:
        app.logger.error(f"Error generating download URL: {e}")
        flash(f"Error generating download URL: {str(e)}")
        return redirect(url_for("files"))


@app.route("/delete/<filename>")
def delete_file(filename):
    """Delete a file from the S3 bucket."""
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
        flash(f"File '{filename}' was successfully deleted.")
    except Exception as e:
        app.logger.error(f"Error deleting file: {e}")
        flash(f"Error deleting file: {str(e)}")
    return redirect(url_for("files"))


@app.route("/api/search", methods=["GET"])
def search_files():
    """API endpoint for searching files with various filters."""
    # Get search parameters
    query = request.args.get("query", "").lower()
    file_type = request.args.get("type", "all")
    date_filter = request.args.get("date", "all")
    sort_by = request.args.get("sort", "name")
    
    try:
        # Get all files first
        all_files = list_uploaded_files()
        results = []
        
        # Apply search filtering
        for file in all_files:
            filename = file['filename'].lower()
            
            # Filter by search query
            if query and query not in filename:
                continue
                
            # Filter by file type
            if file_type != "all":
                if file_type == "image" and not filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    continue
                elif file_type == "document" and not filename.endswith(('.doc', '.docx', '.pdf', '.txt')):
                    continue
                elif file_type == "pdf" and not filename.endswith('.pdf'):
                    continue
                elif file_type == "text" and not filename.endswith('.txt'):
                    continue
            
            # Filter by date
            if date_filter != "all":
                file_date = file['last_modified']
                today = datetime.datetime.now()
                
                if date_filter == "today" and not file_date.startswith(today.strftime('%Y-%m-%d')):
                    continue
                    
                elif date_filter == "week":
                    # Check if file is within the last 7 days
                    file_datetime = datetime.datetime.strptime(file_date, '%Y-%m-%d %H:%M:%S')
                    week_ago = today - datetime.timedelta(days=7)
                    if file_datetime < week_ago:
                        continue
                        
                elif date_filter == "month":
                    # Check if file is within the current month
                    if not file_date.startswith(today.strftime('%Y-%m')):
                        continue
                        
                elif date_filter == "year":
                    # Check if file is within the current year
                    if not file_date.startswith(today.strftime('%Y')):
                        continue
            
            # Add to results if it passed all filters
            results.append(file)
        
        # Sort results
        if sort_by == "name":
            results.sort(key=lambda x: x['filename'])
        elif sort_by == "date":
            results.sort(key=lambda x: x['last_modified'], reverse=True)
        elif sort_by == "size":
            results.sort(key=lambda x: x['size'], reverse=True)
            
        return {"files": results}
        
    except Exception as e:
        app.logger.error(f"Search error: {e}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    # Print useful debug info at startup
    app.logger.info(f"Starting app with bucket: {S3_BUCKET}, region: {AWS_REGION}")
    app.logger.info(f"AWS_ACCESS_KEY_ID environment variable is {'set' if AWS_ACCESS_KEY else 'not set'}")
    
    # Run on 0.0.0.0 to be accessible externally, port 80 requires sudo or other setup
    # For EC2 deployment, a production server like Gunicorn/Waitress is better.
    # Running on port 5000 for local testing. UserData will handle running on port 80.
    app.run(debug=True, host="0.0.0.0", port=5000)
