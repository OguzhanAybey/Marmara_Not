# Tech Context

## Technology Stack
-   **Backend Framework**: Django (Python)
-   **Database**: SQLite (Development/Default)
-   **Frontend**: HTML, CSS, JavaScript (likely Bootstrap for styling based on icon usage)
-   **Template Engine**: Django Templates

## Development Setup
-   **Python Environment**: `venv` or `venv_broken` (detected in root).
-   **Dependencies**: Standard Django dependencies.
-   **Static Files**: Served from `static/` directory.
-   **Media Files**: User uploads stored in `media/notes/`.

## Project Structure
-   `Marmara_Not/` (Root)
    -   `uni_notes/`: Project configuration (`settings.py`, `urls.py`).
    -   `notes/`: Main application (Models, Views, Templates).
    -   `templates/`: Global templates (if any).
    -   `static/`: Static assets (CSS, JS, Images).
    -   `media/`: User uploaded content.
    -   `manage.py`: Django management script.

## Constraints
-   **File Uploads**: Relies on local file system storage (`media/`).
