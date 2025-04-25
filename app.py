import os
import boto3
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flash messages

S3_BUCKET = os.environ.get(
    "S3_BUCKET_NAME", "file-share-app-project-bucket-000"
)  

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1") 

# File type validation
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

s3_client = boto3.client("s3", region_name=AWS_REGION)


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
            flash("AWS credentials not found.")
            return redirect(url_for("index"))
        except ClientError as e:
            flash(f"Failed to upload file: {e}")
            app.logger.error(f"S3 Upload Error: {e}")  # Log the error for debugging
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}")
            app.logger.error(f"Unexpected Error: {e}")
            return redirect(url_for("index"))

    else:
        flash("File type not allowed.")
        return redirect(url_for("index"))


if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible externally, port 80 requires sudo or other setup
    # For EC2 deployment, a production server like Gunicorn/Waitress is better.
    # Running on port 5000 for local testing. UserData will handle running on port 80.
    app.run(debug=True, host="0.0.0.0", port=5000)
