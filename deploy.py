import subprocess
import os
import sys
import argparse

def run_command(command, error_message):
    """Execute a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}\n{e.stderr}")
        sys.exit(1)

def create_dockerfile(app_name):
    """Create a Dockerfile for a simple Flask app."""
    dockerfile_content = f"""
FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
"""
    with open(f"{app_name}/Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print(f"Dockerfile created for {app_name}")

def create_flask_app(app_name):
    """Create a simple Flask app."""
    os.makedirs(app_name, exist_ok=True)
    app_content = """
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World from Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
    with open(f"{app_name}/app.py", "w") as f:
        f.write(app_content)
    print(f"Flask app created in {app_name}/app.py")

def build_docker_image(app_name, image_name):
    """Build a Docker image."""
    run_command(f"docker build -t {image_name} {app_name}", f"Failed to build Docker image {image_name}")

def run_docker_container(image_name, container_name, port):
    """Run a Docker container."""
    run_command(f"docker run -d --name {container_name} -p {port}:5000 {image_name}",
                f"Failed to run container {container_name}")

def main():
    parser = argparse.ArgumentParser(description="Automate Dockerized Flask app deployment")
    parser.add_argument("--app-name", default="myapp", help="Name of the app directory")
    parser.add_argument("--image-name", default="myapp-image", help="Name of the Docker image")
    parser.add_argument("--container-name", default="myapp-container", help="Name of the Docker container")
    parser.add_argument("--port", default="5000", help="Port to expose")
    args = parser.parse_args()

    print("Starting deployment automation...")
    create_flask_app(args.app_name)
    create_dockerfile(args.app_name)
    build_docker_image(args.app_name, args.image_name)
    run_docker_container(args.image_name, args.container_name, args.port)
    print(f"Deployment complete! Access at http://localhost:{args.port}")

if __name__ == "__main__":
    main()
