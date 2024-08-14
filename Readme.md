# Django Chat Application

## Overview

This is a scalable Django-based chat application, designed to handle both HTTP/HTTPS and WebSocket connections efficiently using Docker. The project is structured to run separate containers for different services like `Django Web`, `Django Channels`, `Redis`, `MySQL`, and `Nginx`.

## Features

- **Dockerized Environment**: The application runs within a Docker environment, facilitating easy setup and scalability.
- **Separate Django Services**: 
  - `django_web`: Handles HTTP/HTTPS requests.
  - `django_channels`: Manages WebSocket connections, making it easier to scale according to traffic.
- **Redis as Channel Layer**: Redis is used as the channel layer for Django Channels, ensuring efficient message brokering between the services.
- **Channel Multiplexer**: Utilizes `ChannelMultiplexer` to reduce client connections to a single connection, handling multiple consumers effectively.
- **Automated Setup**: 
  - Automatically creates admin credentials based on environment variables.
  - Adds dummy users to the application on startup for testing purposes.

## Project Structure

- **Docker Containers**:
  - `django_web`: Handles the main application logic and HTTP/HTTPS requests.
  - `django_channels`: Dedicated to managing WebSocket connections.
  - `redis`: Acts as the channel layer for Django Channels.
  - `mysql`: The relational database for storing application data.
  - `nginx`: Reverse proxy server for load balancing and serving static files.

## Prerequisites

- Docker & Docker Compose

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Environment Variables**:
   - The project uses separate environment files for `django_web` and `django_channels`:
     - **`.env` for `django_web`**:
       - Contains settings specific to the main web server, such as:
         - `DEBUG`: Controls whether the application is in debug mode.
         - `SECRET_KEY`: The secret key for Django.
         - `ALLOWED_HOSTS`: A list of strings representing the host/domain names that this Django site can serve.
         - `PROJECT_ADMIN_DETAIL`: Phone number for the default admin user.
         - `PROJECT_ADMIN_DEFAULT_SECRET`: Default password for the admin user.
         - `CSRF_TRUSTED_ORIGINS`: Trusted origins for CSRF protection.
         - `CORS_ALLOWED_ORIGINS`: Allowed origins for CORS.
         - `DJANGO_SETTINGS_MODULE`: Specifies the settings module for Django.
     - **`channels.env` for `django_channels`**:
       - Contains settings tailored for the Channels service, including:
         - `DEBUG`: Controls whether the application is in debug mode.
         - `SECRET_KEY`: The secret key for Django.
         - `ALLOWED_HOSTS`: A list of strings representing the host/domain names that this Django site can serve.
         - `PROJECT_ADMIN_DETAIL`: Phone number for the default admin user.
         - `PROJECT_ADMIN_DEFAULT_SECRET`: Default password for the admin user.
         - `CSRF_TRUSTED_ORIGINS`: Trusted origins for CSRF protection.
         - `CORS_ALLOWED_ORIGINS`: Allowed origins for CORS.
         - `DJANGO_SETTINGS_MODULE`: Specifies the settings module for Django Channels.
   - Customize these files according to your specific environment needs.

3. **Docker Compose**:
   - The Docker Compose file (`local-docker-compose.yml`) orchestrates the containers, including `django_web`, `django_channels`, `redis`, `mysql`, and `nginx`.
   - To build and run the containers, execute the following command:
     ```bash
     docker compose -f "local-docker-compose.yml" up -d --build
     ```
   - This command will build the Docker images, start the containers in detached mode (`-d`), and rebuild them if necessary (`--build`).

4. **Access the Application**:
   - Once the containers are up and running, you can access the various services as follows:
     - **Django Web Application**: 
       - Accessible at `http://localhost:5000`.
       - Handles all HTTP/HTTPS requests.
     - **Django Channels (WebSocket Service)**:
       - Accessible at `http://localhost:5001`.
       - Manages WebSocket connections for real-time communication.
     - **Redis**:
       - Accessible at `http://localhost:6379`.
       - Acts as the channel layer for Django Channels, enabling efficient message brokering.
     - **Redis Insight**:
       - If using the Redis stack with Redis Insight, access it at `http://localhost:8001` for a graphical interface to manage and monitor Redis.

## API Documentation

- **Swagger API Docs**:
  - The application provides comprehensive API documentation using Swagger.
  - You can access the Swagger UI at `http://localhost:5000/swagger/`.
  - This interface allows you to explore and test the various API endpoints provided by the application.
  - The documentation is automatically generated based on the Django REST framework views and serializers, ensuring it is always up-to-date with the latest API changes.
  - Developers can use the Swagger UI to understand the available endpoints, required parameters, request/response formats, and authentication methods.


## Automated Admin and Dummy User Setup

- **Admin User Creation**:
  - On application startup, an admin user is automatically created based on the environment variables `PROJECT_ADMIN_DETAIL` and `PROJECT_ADMIN_DEFAULT_SECRET`.
  - The phone number for the admin account is defined by `PROJECT_ADMIN_DETAIL`, and the password is set by `PROJECT_ADMIN_DEFAULT_SECRET`.
  - This process ensures that an admin account is always available upon initial deployment without manual intervention.

- **Dummy Users**:
  - Along with the admin user, the application automatically generates a set of dummy users for testing and development purposes.
  - These users are useful for quickly testing the application's functionality without needing to manually create accounts.
  - The dummy users are created with predefined credentials, allowing for consistent and repeatable testing scenarios.


## Authentication and Authorization

- **OTP-Based Authentication**:
  - The application employs a passwordless authentication system using One-Time Passwords (OTP) for login and signup.
  - Users receive an OTP via their registered phone number, which they can use to authenticate and access their account.
  - This method enhances security by eliminating the need for passwords, reducing the risk of password-related vulnerabilities.

- **JWT for Authorization**:
  - For authorization, the application uses JSON Web Tokens (JWT).
  - Upon successful authentication via OTP, a JWT is issued to the user, which they can use to access protected resources within the application.
  - JWTs ensure that only authenticated users can perform certain actions or access specific areas of the application.
  - The tokens are securely stored on the client side and included in the headers of HTTP requests to authorize access.

## Django Apps and Models

The project is organized into several Django apps, each with specific responsibilities:

- **`core`**:
  - **Responsibilities**: Manages user authentication and CRUD (Create, Read, Update, Delete) operations.
  - **Models**:
    - `User`: Custom user model with additional fields as needed for the application.

- **`otp`**:
  - **Responsibilities**: Handles the OTP-based authentication flow for user login.
  - **Models**:
    - `VerifyPhoneNumber`: Model for storing OTP codes, their expiration times, and related metadata.

- **`my_app`**:
  - **Responsibilities**: Manages interactions between users, such as sending and accepting friend requests, and storing chat messages.
  - **Models**:
    - `Interest`: Represents a request sent from one user to another.
    - `ChatMessage`: Stores chat messages exchanged between users.

- **`chat`**:
  - **Responsibilities**: Exclusively runs in the `django_channels` container to handle WebSocket connections. It does not contain any models.
  - **Purpose**: 
    - Handles real-time communication through WebSocket connections.
    - Integrates with the Django Channels framework to manage chat sessions, broadcasts, and other real-time features.

## Incomplete Aspects and Potential Next Steps

### Incomplete Aspects
- **Test Scripts**: 
  - The application currently has pending test scripts that need to be implemented.

### Potential Next Steps

1. **User List Filters**:
   - Implement filters to search the user list by name, email, or phone number.
   - This feature would enhance user management and improve the overall user experience by making it easier to find specific users.

2. **Geolocation-Based User Discovery**:
   - Introduce geolocation functionality to identify and display nearby users.
   - This could be particularly useful for features like local networking or location-based services within the application.

3. **In-App and External Notifications**:
   - Add support for in-app notifications or integrate external notification services (e.g., push notifications, SMS) to alert users of new messages.
   - This feature would ensure that users are promptly informed of new activity, even when they are not actively using the app.

4. **Media and Document Sharing**:
   - Extend the application to support sending videos, images, and documents.
   - Use AWS S3 or another cloud storage service provider for storing media and documents securely and efficiently.

5. **Group Messaging and Channel Support**:
   - Develop group messaging and channel support to allow users to communicate in larger groups or within specific channels.
   - This feature would broaden the application's use cases, making it suitable for both personal and professional communication scenarios.
