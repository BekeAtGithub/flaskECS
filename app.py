from flask import Flask
import os

app = Flask(__name__)

# Environment variable for version numbr .
VERSION = "1.0"

# Get the hostname (this will be dynamic depending on your system) 
HOSTNAME = os.getenv("HOSTNAME", "Node")

# Counter to store the number suffix (could be managed by an external service for multiple instances)
counter = 1

@app.route("/")
def index():
    global counter
    # Generate the hostname with number suffix
    node_name = f"{HOSTNAME}-{str(counter).zfill(2)}"
    # Increment the counter for the next instance
    counter += 1
    # Display node name and version
    return f"<h1>{node_name}</h1><p>Version: {VERSION}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
