
<a id="readme-top"></a>

<br />
<div>
  <img src="https://lh3.googleusercontent.com/d/1Ln6zyl_vqXihF3i8ZdYVMtNX4xG4-AL8=s220?authuser=0" alt="Logo" width="100" height="100">
  <h3>Fireflies - API Mocking Service</h3>

  <p>
    A flexible service for simulating custom API responses with ease, helping streamline testing and development workflows.
    <br />
  </p>
</div>

---

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="justify">
Fireflies is an API mocking service designed to simplify testing by simulating real-world API responses. 
With Fireflies, you can define custom status codes and response bodies based on the incoming request body, 
allowing you to test various scenarios without relying on external APIs. Whether you're handling edge cases, 
validating error handling, or optimizing response workflows, Fireflies ensures comprehensive test coverage 
and accelerates your development process.
</p>

---

<!-- GETTING STARTED -->
## Getting Started

To get started with Fireflies, follow the steps below to set up your environment and run the application.

### Prerequisites

Ensure you have the following installed:

* **pip**  
  Install required dependencies:
  ```sh
  pip install -r requirements.txt
  ```

* **PostgreSQL Database**  
  Set up a PostgreSQL database instance.

### Environment Setup

Create a `.env` file at the root of the project with the following content:

```plaintext
ENVIRONMENT=local
DATABASE_URL=postgresql://username:password@host:port/database_name
```

Replace `username`, `password`, `host`, `port`, and `database_name` with your database credentials.

### Running the Application

Run the application using the following command:

```sh
python -m uvicorn main:app --reload
```

This will start the application in development mode with hot-reloading enabled.

---