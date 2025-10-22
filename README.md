# Little HTTP Server

This project is a **personal learning project** aimed at understanding the basics of HTTP servers. It is a simple implementation of an HTTP server in Python and is **not production-ready** or secure. Use it only for educational purposes.

---

## Features
- Basic HTTP server functionality.
- Support for adding custom handlers for different routes.
- Example handlers for serving files and JSON responses.

---

## How to Use

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Install Dependencies**  
   Ensure you have Python installed. Install any required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**  
   Start the server by running the `main.py` file:
   ```bash
   python main.py
   ```

4. **Access the Server**  
   By default, the server will run on `http://localhost:8080`. You can access the available routes in your browser or using tools like `curl`.

---

## Adding a Handler

To add a custom handler:

1. **Create a New Handler Class**  
   Create a new class that inherits from the `Handler` base class. Implement the `handle_connection` method to define how the server should respond to requests.

   Example:
   ```python
   from handler import Handler

   class CustomHandler(Handler):
       def handle_connection(self, verb, path, header_dict, body):
           status = '200 OK'
           response_body = 'Hello, this is a custom handler!'
           return f'HTTP/1.0 {status}\r\n\r\n{response_body}'.encode(), status
   ```

2. **Register the Handler**  
   In `main.py`, add the handler to the server for a specific route:
   ```python
   from custom_handler import CustomHandler

   custom_handler = CustomHandler()
   server.add_handler('GET', '/custom', custom_handler)
   ```

3. **Restart the Server**  
   Restart the server to apply the changes.

---

## Disclaimer
This project is for **educational purposes only**. It is not secure or optimized for production use. Use it at your own risk.