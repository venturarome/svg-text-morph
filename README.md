# svg-text-morph

**svg-text-morph** is a dynamic API built with FastAPI that generates smooth, animated SVG text morphing transitions on the fly. It lets you create stunning text animations by morphing between words using customizable parameters like fade time, show time, and transformation time.

Enjoy creating amazing SVG animations, and thank you for using svg-text-morph!
Remember to ⭐ star the project if you find it useful!

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Live Demo](#live-demo)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Open Issues](#open-issues)

---

## Features

- **Dynamic SVG Animations:** Generate animated SVGs by morphing text transitions.
- **Customizable Parameters:** Easily configure timing (fade, show, translate) and font settings.
- **Clean API:** Built with FastAPI; automatically generated interactive docs available at `/docs`.
- **Modular Codebase:** Organized project structure with dedicated schemas, services, dependencies, and tests.
- **Free Deployment:** Hosted on Render for public access.

---

## Technologies Used

- **Python 3.9+**
- **FastAPI** – A modern, fast web framework for building APIs.
- **Uvicorn** – A lightning-fast ASGI server.
- **svgwrite** – A Python library for generating SVG files.
- **Jinja2** – For templating (rendering dynamic HTML pages).
- **Render** – Free hosting platform for deploying your FastAPI project.
- **Pytest** – For testing the application.

---

## Live Demo

You can test the API live at:  
**[https://svg-text-morph.onrender.com](https://svg-text-morph.onrender.com)**  
*(Check the `/docs` endpoint for interactive API documentation.)*

---

## Getting Started

### Prerequisites

- Python 3.9 or higher installed on your machine.
- [Git](https://git-scm.com/) for cloning the repository.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/venturarome/svg-text-morph.git
   cd svg-text-morph
   ```

2. **Create and activate a virtual environment:**

    On Unix/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application locally:**
    ```bash
    uvicorn main:app --reload
    ```

5. **Access the API:**
Visit http://localhost:8000 to see the welcome page and check out the API documentation at http://localhost:8000/docs.

6. Whenever you want to **finish working** on it:
    - Stop the server (CTRL+C).
    - Exit the virtual environment by running `deactivate`.


### Contributing

Contributions are welcome! If you’d like to contribute to **svg-text-morph**, please follow these steps:
1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/my-new-feature
    ```
3. **Commit your changes** with clear commit messages.
4. **Push your branch** to your fork:
    ```bash
    git push origin feature/my-new-feature
    ```
5. **Create a pull request** with a description of your changes and why they’re needed.


### Open Issues
Before contributing, or if you encounter any bugs or have feature requests, please check the [open issues](https://github.com/venturarome/svg-text-morph/issues).
