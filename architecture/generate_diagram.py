# generate_diagram.py
from diagrams import Diagram, Edge, Cluster
from diagrams.programming.language import Python
from diagrams.programming.framework import Flask
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Internet
from diagrams.onprem.client import User

def generate_architecture_diagram():
    with Diagram("QR Code Generator Architecture", show=False, direction="TB"):
        user = User("User")
        
        with Cluster("Vercel"):
            html = Internet("HTML Form")
            flask = Flask("Flask App")
            qr_gen = Python("QR Generator")
            font_api = Internet("Google Fonts API")

        user >> Edge(label="1. Access") >> html
        html >> Edge(label="2. Submit Form") >> flask
        flask >> Edge(label="3. Generate QR") >> qr_gen
        flask >> Edge(label="4. Fetch Font") >> font_api
        qr_gen >> Edge(label="5. Return QR") >> flask
        flask >> Edge(label="6. Send QR") >> user

if __name__ == "__main__":
    generate_architecture_diagram()