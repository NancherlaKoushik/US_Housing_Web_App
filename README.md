

---

```markdown
# USA Housing App

The **USA Housing App** is an interactive web application built using [Shiny for Python](https://shiny.posit.co/py/). It visualizes and analyzes housing market data across the United States, allowing users to explore metrics such as median listing prices, home inventory changes, and new listings by state and date range. The app provides both graphical (line plots) and tabular views of the data, with filtering options for states and time periods.

## Features

- **Interactive Dashboard**: Filter housing data by state and date range using a sidebar interface.
- **Key Metrics**:
  - Current median listing price for a selected state or the entire U.S.
  - Percentage change in home inventory over time.
- **Visualizations**:
  - Line plots for median listing prices, for-sale inventory, and new listings, powered by [Plotly Express](https://plotly.com/python/plotly-express/).
  - Tabular data views for detailed exploration.
- **Data Sources**:
  - `Metro_new_listings_uc_sfrcondo_month.csv`: New listings data.
  - `Metro_mlp_uc_sfrcondo_sm_month.csv`: Median listing price data.
  - `Metro_invt_fs_uc_sfrcondo_sm_month.csv`: For-sale inventory data.
- **State Selection**: Includes a dropdown with all U.S. states and an option for nationwide data (via `state_choices.py`).

## Dependencies

To run this app, you’ll need the following Python packages:

- `shiny` - Framework for building the app.
- `pandas` - Data manipulation and analysis.
- `numpy` - Numerical operations.
- `plotly` - Interactive plotting library.
- `shinywidgets` - Enhanced Shiny widgets for Plotly integration.
- `faicons` - Font Awesome icons for UI elements.
- `pathlib` - File path handling.

You can install all dependencies using the following command:

```bash
pip install shiny pandas numpy plotly shinywidgets faicons
```

## Prerequisites

- **Python 3.8+**: Ensure you have a compatible version of Python installed.
- **CSV Data Files**: The app relies on three CSV files listed above. These should be placed in the same directory as the main script (`app.py`).
- **`state_choices.py`**: A supporting file that defines `STATE_CHOICES` (a list or dictionary of U.S. states). Ensure this file is present in the project directory.

## Project Structure

```
usa-housing-app/
├── app.py                       # Main Shiny app script
├── state_choices.py             # State choices definition
├── Metro_new_listings_uc_sfrcondo_month.csv  # New listings data
├── Metro_mlp_uc_sfrcondo_sm_month.csv        # Median listing price data
├── Metro_invt_fs_uc_sfrcondo_sm_month.csv    # For-sale inventory data
├── README.md                    # This file
```

## How to Clone and Run Locally

Follow these steps to set up and run the app on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/usa-housing-app.git
   cd usa-housing-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t have a `requirements.txt` yet, create one with:
   ```bash
   pip freeze > requirements.txt
   ```
   after installing the dependencies manually.

3. **Ensure Data Files Are Present**:
   Place the three CSV files (`Metro_new_listings_uc_sfrcondo_month.csv`, `Metro_mlp_uc_sfrcondo_sm_month.csv`, `Metro_invt_fs_uc_sfrcondo_sm_month.csv`) in the project directory.

4. **Run the App**:
   ```bash
   shiny run --reload app.py
   ```
   - The `--reload` flag enables automatic reloading when the code changes.
   - Open your browser and navigate to `http://127.0.0.1:8000` (or the port displayed in the terminal).

## Deployment

To deploy the app to a public server, you can use platforms like [ShinyApps.io](https://www.shinyapps.io/) (for Python Shiny apps) or a custom server. Here’s how to deploy to ShinyApps.io:

1. **Install the `rsconnect-python` CLI**:
   ```bash
   pip install rsconnect-python
   ```

2. **Configure Your Account**:
   - Sign up at [ShinyApps.io](https://www.shinyapps.io/).
   - Get your token and secret from the dashboard.
   - Run:
     ```bash
     rsconnect add --account <your-account> --token <your-token> --secret <your-secret>
     ```

3. **Deploy the App**:
   From the project directory, run:
   ```bash
   rsconnect deploy shiny . --name usa-housing-app
   ```
   - Ensure all files (including CSVs and `state_choices.py`) are in the directory.
   - The app will be deployed and accessible via a public URL provided by ShinyApps.io.

Alternatively, for a custom server (e.g., Heroku or a VPS):
- Use a `Procfile` (e.g., `web: shiny run --host 0.0.0.0 --port $PORT app.py`).
- Include a `requirements.txt` file.
- Configure the server to serve the app.

## Usage

- Select a state (or "United States" for nationwide data) from the dropdown.
- Adjust the date range slider to filter data between March 31, 2018, and April 30, 2024.
- Explore the value boxes for quick insights and navigate between plot and table views under each tab.

## Contributing

Feel free to fork this repository, submit issues, or create pull requests. Contributions to improve functionality, add new metrics, or enhance the UI are welcome!
