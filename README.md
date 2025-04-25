# Simple File Share - Cloud Project

A lightweight file sharing web application built on AWS cloud services. This project provides an easy-to-use interface for uploading, storing, and sharing files securely in the cloud.

## 📸 Screenshot *(hosted on our System)* 🖼️ 🎉

We are proud to showcase our application in action! Here's a glimpse of the user interface:

![Simple File Share Screenshot](https://s3.eu-north-1.amazonaws.com/file-share-app-project-bucket-000/Screenshot_2025-04-25_144233.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIARB6YQRXX2Y6DWZ2D%2F20250425%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20250425T114306Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmV1LW5vcnRoLTEiRzBFAiEAihGP8bdpY8SdDcxW1VybeP8zGwwIR27%2FNpLHoVUEpPECIEVXU8vwNChdJ9uZOZdtvnY%2FLM%2BfXc2QTgLnzH2C6CQDKr0FCCwQABoMMDcyOTMxNjQyODYzIgzHvXIajzVIgabDKZYqmgUHem2kxmGmPnQSICOixTlH%2BtXRliN69LNEo01ph7QW7sNXJM2oB1P8rRMN%2F6YnynVvxMyCt%2FfKx2QuGnDMdhAHqWW8eoLcf%2BkyzLrQATOZLr%2Fhj%2B3Xkbqin%2FhjmgyCHHhzf9WD1gkvEZ5u2MWUKQg1e8MFM%2FHJ%2F16nFryXS65FXOHUsfvPzS%2FLRvf4ZAODB0Voqu6WbNzZRHUL%2BWM%2FFFB9jMsEvPli4hJEjtZdosGSNA3Z7ab1f8YJ%2BDWeYugjGAbboTpRgXttv9Q9RvYw4sG6Oa7X0HTC41CXh73y%2B0buptpK5hO2KDmFjz7zLPemLJZNcQEPiKAyf%2BQJVSp2dri8HxdwO%2FrJBylwnLVQ7qCRneUri7DijWN7992L3E9OiSthQWdhSzN1VvKLtE%2FGONCKbqEmZN0ogbUuQmkuMCrJ7%2FnlDjnibFvWEJXOF6Te7pTAMYl3Qn6thH3SOGfoFEDeibTzCDSmUa9RmswL0Is6Ry0EWZ83RPH5Zepz1g6kvJrC2K%2FMnWrm0dWr4P9A%2B3iUWZzWetHVslRH1yM1TmgM50NQB%2FoQx2zuJJkuNx2469fV6nayavcDrVDq3WLPLdPbm2DgAlC6JJH0e5Iba2x9wx%2F6yzHGqSWNRW2OFoJJr%2FLWYWl5xtHAxznSNGFjDdeqr7Pt4nWQFmboOPa548SlbrLBk0Im6552IKhZLqDPP264L1vxefEtXGkVNo%2BUH%2FGEfNUr2Aj%2BibwLWWCBb6Bv%2ByawXR%2BFXO0lBVtEMS%2FDmDa7V9xlLfZ3MIPP4ls07hN1k1GySOh6S%2BbtnHBj3WZY6X4Lmg9ZHfVj6u69%2BqN2ONm7rb%2BkDTlZ6h7dbVu4Z8BAh8WlrSLh2DJy7cZCRdL9lH91l%2BJ0iBGJGHowqsytwAY6sQEHV%2BwZAmvRupWw%2FH44k0VQDA9c%2BO4gncVL9YuM6a71m1krBJBomjaiJOejYXIH3KSsQb2aslpZONkekQcOHw1uNpmyFBZksMhTf9lmdMUvPk8f9Wm%2Bgf62GwLptPzl5uavxyVCnvkPBw7c3jw8Ck%2FAPk52HEPD5eN3SwkRXhd6vwaC7Eob1n1cL3rIntxHISbwUgajk2JLgMd3qHNijnNhLoGjq1w8uLinCQTzt5xkBFw%3D&X-Amz-Signature=0086fb071c69549ae66c3039c46f3beb7c57db3fb3c91b2420fce59a10d9f150)

## 🌟 Features

- **Simple Web Interface**: Clean, responsive design for uploading files through a web browser
- **Secure File Storage**: All files stored securely in Amazon S3 buckets
- **Temporary Download Links**: Time-limited secure links for file sharing
- **File Management**: View, search, and delete your uploaded files
- **File Type Filtering**: Support for common file types (images, documents, PDFs, etc.)
- **User Feedback System**: Built-in feedback mechanism for user suggestions and issue reporting

## ⚙️ Architecture

This application uses a multi-tier AWS architecture:

- **Frontend**: HTML, CSS, JavaScript with Flask templates
- **Backend**: Python Flask web server running on EC2
- **Storage**: Amazon S3 bucket for secure file storage
- **Networking**: Custom VPC with appropriate security groups
- **Security**: IAM roles for secure S3 access from EC2

![Architecture Diagram](https://via.placeholder.com/800x400?text=Architecture+Diagram)

## 🚀 Deployment

The application is designed to be deployed on AWS infrastructure:

1. **EC2 Instance**: Hosts the Flask web application
2. **S3 Bucket**: Provides scalable object storage for files
3. **IAM Role**: Grants EC2 instance secure access to S3 resources
4. **Security Groups**: Control network traffic to the application

### Installation Steps

1. Clone the repository to your EC2 instance:

   ```bash
   git clone https://github.com/abdallahsaber065/cloud-project.git app
   cd app
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set the required environment variables:

   ```bash
   export S3_BUCKET_NAME="your-s3-bucket-name"
   export AWS_REGION="your-aws-region"
   ```

4. Run the application:

   ```bash
   # For development
   python app.py
   
   # For production (using Waitress)
   waitress-serve --host 0.0.0.0 --port 80 app:app
   ```

5. Access the application through your EC2 instance's public IP or domain.

## 🔒 Security Considerations

- Files are stored privately in S3 and accessed via time-limited presigned URLs
- EC2 uses IAM role for S3 access (no hardcoded credentials)
- Security groups restrict network access to the application

## 👥 Team Members & Roles

| Name               | Role                   | Responsibilities                                                       |
| ------------------ | ---------------------- | ---------------------------------------------------------------------- |
| Nour Kamal         | AWS Account Setup      | Created and configured AWS account                                     |
| Loay Mohamed       | EC2 & IAM Setup        | Launched EC2, configured IAM roles                                     |
| Abdelrahman Hamada | S3 & File Handling     | Created S3 bucket, implemented file operations                         |
| Abdullah Saber     | Web App Development    | Built web interface and backend logic                                  |
| Ahmed Ihaab        | VPC & Testing          | Network setup, testing, documentation                                  |
| Yousef Bakr        | Test and Documentation | Tested the app, ensured functionality, and compiled the project report |

## 🖥️ Pages & Features

1. **Home Page**: File upload interface
2. **Files Page**: View and manage uploaded files
3. **Search Page**: Find files with advanced filtering
4. **Feedback Page**: Submit suggestions or report issues

## 📋 Project Requirements

This project was created as part of a cloud computing course assignment with the following requirements:

- Create a simple file sharing web application on AWS
- Use EC2 for hosting and S3 for file storage
- Implement IAM roles for secure access management
- Configure VPC for network security
- Implement basic file upload and download functionality

## 💡 Bonus Features Implemented

- **File Listing**: View all uploaded files with metadata
- **Enhanced UI**: Applied modern HTML/CSS styling
- **Search Functionality**: Find files by name, type, or date
- **Feedback System**: Built-in communication channel with EmailJS

## 📝 License

This project is created for educational purposes as part of a cloud computing course.
