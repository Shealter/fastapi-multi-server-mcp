# Contributing to DeepL MCP Server

Thank you for your interest in contributing to the DeepL MCP Server! We appreciate your efforts to improve this project.

## How to Contribute

There are several ways you can contribute:

*   **Reporting Bugs**: If you find a bug, please report it by opening an issue on GitHub.
*   **Suggesting Features**: Have an idea for a new feature? Open an issue to discuss it.
*   **Submitting Pull Requests**: If you'd like to contribute code, please follow the guidelines below.

## Setting up Your Development Environment

To set up your local development environment, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AlwaysSany/fastapi-multi-server-mcp.git
    cd fastapi-multi-server-mcp.git
    ```

2.  **Install `uv` (recommended) or use `pip`:**

    With **pip**,
    ```bash
    pip install uv
    ```

    With **pipx**,
    ```bash
    pipx install uv
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

4.  **Set your environment variables:**
    Create a `.env` file from `.env.example`. You can do this by running the following command and then update the `.env` file with your DeepL API key:
    ```bash
    cp .env.example .env
    ```
    
    ```env
    # Weather API (OpenWeatherMap)
    OPENWEATHER_API_KEY=your_openweather_api_key
    
    # News API
    NEWS_API_KEY=your_news_api_key
    
    
    # Exchange Rates API
    EXCHANGE_RATES_API_KEY=your_exchange_rates_api_key
    
    # Server Configuration
    PORT=10000
    HOST=0.0.0.0
    ```

5.  **Run the server in development mode:**

  ```bash
  # Using UV
  uv run uvicorn main:app --reload --host 0.0.0.0 --port 10000 --reload
  
  # Using `npx` to debug the running application,
  npx @modelcontextprotocol/inspector uv run uvicorn main:app
  ```

## Running Tests

To ensure your changes don't introduce regressions, please run the existing tests.

1.  **Ensure you have `pytest` installed.** It should be installed with `uv sync`.
2.  **Run tests from the project root:**
    ```bash
    uv run pytest tests/
    ```

## Code Style

*   Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
*   We recommend using a linter (e.g., `flake8` or `ruff`) and a formatter (e.g., `black`) to ensure consistency.

## Pull Request Process

1.  **Fork the repository** and create your branch from `main`.
2.  **Make your changes**.
3.  **Ensure your code passes tests** and adheres to the code style guidelines.
4.  **Write clear, concise commit messages**.
5.  **Push your changes** to your forked repository.
6.  **Open a pull request** to the `main` branch of the original repository.
    *   Provide a clear and detailed description of your changes.
    *   Reference any related issues.

## Reporting Bugs and Suggesting Features

If you find a bug or have a feature request, please open an issue on our [GitHub Issues page](https://github.com/AlwaysSany/fastapi-multi-server-mcp/issues).
*   For bug reports, please include steps to reproduce the bug and any relevant error messages.
*   For feature requests, describe the feature and why you think it would be valuable. 
