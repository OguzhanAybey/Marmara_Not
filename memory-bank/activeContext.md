# Active Context

## Current Focus
**Version: v1.2.0** - The project has completed major URL restructuring and model improvements. Current focus is on implementing user-facing features from the roadmap.

## Recent Changes (v1.2.0)
-   **URL System Refactor**: Implemented short, meaningful URLs (`/ders/faculty-slug/department-slug/COURSE_CODE/`)
-   **Model Improvements**: 
    -   Removed unique constraint from Course slug to allow same code across departments
    -   Added department context to course display (e.g., "MATH101 - Calculus 1 (Malzeme Mühendisliği)")
-   **Admin Panel**: Added faculty column, advanced filtering, and bulk operations
-   **Performance**: Fixed N+1 query problems and optimized database indexes

## Active Decisions
-   **Faculty-Scoped Course Codes**: Same course code can exist in different departments
-   **URL Structure**: Using hierarchical slugs for better SEO and UX

## Next Steps (Roadmap)
1.  **Mobil Responsive Menu**: Improve mobile navigation
2.  **Kullanıcı Kayıt/Giriş**: Custom authentication pages
3.  **İstatistikler**: Dashboard with statistics
4.  **Değerlendirme Sistemi**: Rating system for notes
