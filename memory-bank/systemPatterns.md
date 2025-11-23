# System Patterns

## Architecture
The project follows the standard **Django MVT (Model-View-Template)** architecture.

- **Models**: Define the data structure (Faculty, Department, Course, Note).
- **Views**: Handle the business logic and data retrieval (Function-Based Views are used).
- **Templates**: Render the UI using Django Template Language (DTL) and Bootstrap (implied by class names in views like `fa-` icons and structure).

## Data Models (`notes/models.py`)
1.  **Faculty**: Represents a university faculty.
    -   `name`, `slug`
2.  **Department**: Represents a department within a faculty.
    -   `faculty` (FK), `name`, `slug`
3.  **Course**: Represents a course within a department.
    -   `department` (FK), `name`, `code`, `slug`
4.  **Note**: Represents a lecture note file.
    -   `course` (FK), `uploader` (FK to User), `title`, `description`, `file`, `status` (pending/approved/rejected), `created_at`, `approved_at`.

## Key Technical Decisions
-   **Slug-based URLs**: SEO-friendly and readable URLs are used for navigation (e.g., `/fakulte/<slug>/`).
-   **Function-Based Views (FBVs)**: Used for all views, keeping logic explicit.
-   **SQLite**: Used as the database (default Django setup).
-   **Django Auth**: Built-in authentication used for user management.

## Component Relationships
-   **Faculty** 1 -- * **Department**
-   **Department** 1 -- * **Course**
-   **Course** 1 -- * **Note**
-   **User** 1 -- * **Note** (Uploader)
