# IT Asset Management Dashboard

This is a Streamlit-based dashboard for managing IT assets, connected to a Neon PostgreSQL database.

## Setup Instructions

1. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Set Up Database**:
   - The database schema is defined in `schema.sql`.
   - Run `python init_db.py` to create the tables automatically.

3. **Run the Application**:
   ```
   streamlit run app.py
   ```

## Features

- Add new assets via the sidebar.
- View asset inventory in a table.
- Visualize asset status and types with charts.
- Get alerts for expired warranties.

## Database

The application uses Neon PostgreSQL. Update the `DATABASE_URL` in `database.py` with your Neon connection string if needed.
