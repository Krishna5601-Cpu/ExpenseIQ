# ExpenseIQ - Development Notes

This file contains things I learned while building ExpenseIQ.

---

## Project Goal

Build an expense tracker that is clean, modular, and actually useful instead of just another CRUD project.

---

## Things I Learned

### Flask Application Factory

Initially I was writing everything directly in one place.

Later I switched to the Application Factory pattern using `create_app()`. It makes the project much cleaner and easier to scale.

---

### Blueprints

Instead of putting all routes in one file, I separated them into:

- main
- expense
- budget

This made navigation much easier.

---

### Service Layer

One of the biggest improvements in this project.

Instead of writing database queries inside routes, all business logic now lives inside services.

Routes only receive requests and return responses.

---

### SQLAlchemy

Things I learned:

- Creating models
- CRUD operations
- Database sessions
- Updating records
- Deleting records
- Using `db.session.get()` instead of the older `query.get()`

---

### Validation

Validation should not happen inside routes.

Creating a dedicated validation service keeps the code cleaner and avoids repeating the same checks.

---

### Jinja Templates

Using template inheritance reduced a lot of duplicated HTML.

Instead of repeating the navbar on every page, I created a shared `base.html`.

---

### Components

Breaking large templates into components made the project much easier to maintain.

Current components:

- Navbar
- Expense Table
- Insights

---

### Google Gemini API

Learned how to:

- Configure API keys using `.env`
- Send prompts
- Parse AI responses
- Handle missing API keys gracefully

---

### Matplotlib

Used Matplotlib to generate charts dynamically.

Charts are regenerated whenever the dashboard loads.

---

### Error Handling

Instead of assuming everything works, I started handling possible failures like:

- Invalid user input
- Missing API keys
- Corrupted JSON
- Database errors

---

### Project Structure

One of the biggest lessons from this project.

Keeping files small is much better than having one huge file.

Separating routes, services, models, templates, and static files makes the project easier to understand.

---

## If I Continue This Project

Some ideas for future versions:

- User authentication
- Monthly reports
- Export expenses to CSV/PDF
- Recurring expenses
- Dashboard filters
- REST API
- Docker support
- PostgreSQL
- Unit tests

---

## Final Thoughts

This project taught me much more than just Flask.

It helped me understand how to organize a real application, separate responsibilities, and write cleaner code. There are still many improvements I can make, but compared to my earlier projects, this is a big step forward.
