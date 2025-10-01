# Credly

This repository contains both the frontend and backend for the Credential Verification System.
The app allows users to verify educational credentials, such as WAEC and NECO certificates,
through the backend API. The backend integrates with external services to validate the authenticity
of these certificates, while the frontend provides a user-friendly interface for entering document
details and viewing verification results. The system streamlines the verification process,
ensuring accurate and efficient validation of documents.

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
  - [Backend Installation](#backend-installation)
  - [Frontend Installation](#frontend-installation)
- [Running the Project](#running-the-project)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)


## Project Overview

This project consists of two parts:
1. **Backend**: A Flask-based API to handle document verification and process requests.
2. **Frontend**: A React-based UI for interacting with the verification system.

## Directory Structure

/credly |
├── backend/ |
    ├── app.py │
    ├── requirements.txt │
    └── README.md
└── frontend/ |
    ├── src/
    ├── package.json
    └── README.md
└── README.md


## Installation

### Backend Installation

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the main file:

    ```bash
    python app.py
    ```

### Frontend Installation

1. Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2. Install the required dependencies:

    ```bash
    npm install
    ```

## Running the Project

Ensure both the frontend and backend are set up as described above.

### Running the Backend

1. Start the backend server:

    ```bash
    cd backend
    python app.py
    ```

The backend will be available at `http://127.0.0.1:5000`.

### Running the Frontend

2. Start the frontend server in another terminal:

    ```bash
    cd frontend
    npm start
    ```

The frontend will be available at `http://localhost:3000`.

3. Once both servers are running, you can interact with the frontend, which will make API calls to the backend.
