# Desktop Application with Golang and Python Microservice

This project consists of two components:

1. **Golang Desktop Application**:
    - A desktop application that supports Windows and Linux platforms (testing on Windows is sufficient).
    - Features a GUI interface for configuring server URLs, API keys, device registration, and scanning.
    - Demonstrates the use of Go concepts like structs, interfaces, error handling, best practices, and Go routines.

2. **Python Microservice**:
    - A backend service that exposes APIs for device registration, saving scan results, and viewing scan results.
    - Protected by JWT tokens and uses an SQL database to store device and scan data.
    - Demonstrates Object-Oriented Programming (OOP), error handling, and best practices in Python.

## Golang Desktop Application

### Features:
- **Cross-Platform Support**: 
  - Supports both Windows and Linux platforms (Windows testing is sufficient).
- **GUI**: 
  - Displays a welcome message and an image.
  - Allows users to configure the server URL and API key.
  - Server URL and API Key are persistent across sessions.
- **Device Registration**:
  - The user can click a button to register a device.
  - On successful registration, a message is shown.
- **Scan Now**:
  - The "Scan Now" button is enabled only if the device registration is successful.
  - On clicking "Scan Now", the app fetches system information (OS Name, OS Version, Last Updated Date, Available Disks, Free Disk Space, Total Disk Space) and sends it to the server via the POST API to save scan results.
  - Displays success or failure messages.
- **View Previous Scans**:
  - Users can view previous scan results from the server.

### Key Concepts Demonstrated:
- **Structs and Interfaces** in Go.
- **Logic and Error Handling**.
- **Best Practices**.
- **Go Routines** for concurrency.

### Running the Django Project:

1. Clone this repository:
   ```bash
   git clone https://github.com/roni30895/Desktop_application.git

2. Create virtual environment
   ```bash
   python -m venv venv

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process (for windows)

   .\venv\Scripts\activate

3. Install all the dependencies using requirements.txt
   
   ```bash
    pip install -r .\requirements.txt

4. Go to desktop_app directory

   ```bash
    cd desktop_app

5. Migrate the database:
   ```bash
   python manage.py migrate

6. Run the server:
    ``` bash
    python manage.py runserver

7. Create api token using following command.

   ```bash
   
    curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "admin", "password": "your_admin_password"}'

  You will get following response:
  {
    "access_token":"",
    "refresh_token":""
  }

  Using this token you can use following. You can access the APIs via:

  POST /api/register_device/
  POST /api/save_scan_results/
  GET /api/view_all_devices/