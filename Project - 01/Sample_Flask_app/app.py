from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

# A metric counter — counts how many times "/" is visited
# Prometheus will read this number
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of homepage requests'
)


@app.route('/')  # The homepage.
def hello():
    REQUEST_COUNT.inc()

    hostname = os.getenv("HOSTNAME", "Local Machine")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Monitoring App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 800px;
                margin: 60px auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
            }}

            .status {{
                color: green;
                font-weight: bold;
            }}

            .card {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}

            ul {{
                line-height: 1.8;
            }}

            a {{
                color: #007bff;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 DevOps Monitoring Application</h1>

            <div class="card">
                <p><strong>Status:</strong>
                <span class="status">Running Successfully</span></p>

                <p><strong>Hostname:</strong> {hostname}</p>
            </div>

            <div class="card">
                <h3>Available Endpoints</h3>
                <ul>
                    <li><a href="/health">/health</a> - Health Check</li>
                    <li><a href="/metrics">/metrics</a> - Prometheus Metrics</li>
                </ul>
            </div>

            <div class="card">
                <h3>Monitoring Stack</h3>
                <ul>
                    <li>Flask Application</li>
                    <li>Prometheus Metrics</li>
                    <li>Docker Ready</li>
                    <li>Kubernetes Ready</li>
                </ul>
            </div>
            <div class="card">
                <h3>Deployment Information</h3>
                <p><strong>Replicas:</strong> 1</p>
                <p><strong>Image:</strong> abdullah4261/sample-flask-app:latest</p>
            </div>

            <div class="card">
                <h3>VERSION - 2 CI/CD PIPELINE</h3>
                <p><strong>Replicas:</strong> 2</p>
                <p><strong>Kubernetes pulling the image from the Dockerhub:</strong> abdullah4261/devops-project-01:latest</p>
            </div>
        </div>
    </body>
    </html>
    """, 200


@app.route('/health')  # A health check URL. Kubernetes pings this every few seconds. If it gets a 200 back, the app is alive. If not, K8s restarts it.
def health():
    """Kubernetes pings this endpoint to check if our app is alive"""
    return {'status': 'healthy'}, 200


@app.route('/metrics')  # Prometheus scrapes this to collect all your metrics (request count, process stats, etc.).
def metrics():
    """Prometheus scrapes this URL every 15 seconds to collect stats"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    # host='0.0.0.0' = accept connections from ANY IP (required in containers!)
    # Without this, Docker/K8s can't reach the app
    app.run(host='0.0.0.0', port=5000, debug=False)  # Critical! Without this, Flask only listens on localhost inside the container and nothing outside can reach it
