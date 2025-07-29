# express-flask-azure-bridge
Connecting an Express.js backend with a Flask service in Python that communicates with Azure Computer Vision.

This project demonstrates how I built a system where a Node.js backend (Express) communicates with a Python application (Flask), which in turn connects to the Azure Computer Vision service.
🔧 Technologies:

   - Express.js (Node.js)

   - Flask (Python)

   - Azure AI / OCR

📡 Architecture:

   - The client sends a technical CAD drawing with tags (e.g., pipe or valve tags) to the Express server

   - Express forwards the data to the Flask server

   - Flask sends a request to Azure Computer Vision

   - The response from Azure goes back through Flask to Express, and then to the user

💡 Use Case:

This project was used in my company’s internal application for analyzing documents and images. The code has been simplified and made public for demonstration purposes.
