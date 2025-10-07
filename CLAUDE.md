# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a course materials repository for "Claude Code: A Highly Agentic Coding Assistant" from DeepLearning.AI. It contains learning materials, reading notes, and hands-on project examples demonstrating Claude Code best practices.

The repository includes three types of content:
- **Course notes** (`reading_notes/`) - Detailed notes for lessons 0-8 including prompts and summaries
- **Lesson 7 project** (`lesson7_files/`) - Complete e-commerce data analysis implementation
- **Reference materials** - Links to course repositories and additional resources

## Primary Working Directory: lesson7_files/

The main executable code is in `lesson7_files/`, which contains a refactored e-commerce analytics project with:
- Jupyter notebooks for exploratory data analysis
- Python modules for data processing and metrics
- Streamlit dashboard application
- E-commerce datasets in `ecommerce_data/` subdirectory

## Common Commands

### Running the Lesson 7 Project

```bash
cd lesson7_files

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit dashboard
streamlit run dashboard.py

# Run the Jupyter notebook
jupyter notebook EDA_Refactored.ipynb

# Run validation tests
python test_comparison.py
```

### Working with the Python Modules

The project uses two reusable modules:

**data_loader.py** - Data loading and preprocessing:
```python
from data_loader import EcommerceDataLoader

loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales_data = loader.process_sales_data(datasets['orders'], datasets['order_items'])
```

**business_metrics.py** - Metrics calculation and visualization:
```python
from business_metrics import BusinessMetrics

metrics = BusinessMetrics(analysis_year=2023, comparison_year=2022)
revenue = metrics.calculate_revenue(sales_data, 2023)
fig = metrics.create_monthly_revenue_chart(sales_data)
```

## Code Architecture

### Lesson 7 Project Structure

The e-commerce analytics project follows a modular architecture:

1. **Data Layer** (`data_loader.py`):
   - `EcommerceDataLoader` class handles all CSV file loading
   - Processes sales data with proper datetime handling
   - Merges datasets (orders, items, products, customers, reviews)
   - Uses `.copy()` throughout to avoid SettingWithCopyWarning

2. **Business Logic Layer** (`business_metrics.py`):
   - `BusinessMetrics` class calculates KPIs (revenue, growth, AOV)
   - Creates interactive Plotly visualizations
   - Generates comprehensive business reports

3. **Presentation Layer**:
   - `dashboard.py`: Streamlit app with year filtering and interactive charts
   - `EDA_Refactored.ipynb`: Clean notebook with configuration constants

### Configuration Pattern

Both the notebook and modules use configuration constants for easy year changes:

```python
ANALYSIS_YEAR = 2023
COMPARISON_YEAR = 2022
DATA_PATH = 'ecommerce_data/'
```

This design allows analyzing different time periods without modifying business logic.

### Key Design Decisions

- **No warnings**: All pandas SettingWithCopyWarning issues eliminated using proper `.copy()` usage
- **Plotly over Matplotlib**: All 7 visualizations use Plotly for interactivity
- **Type hints**: Functions include type annotations for better IDE support
- **Comprehensive docstrings**: All classes and methods fully documented

## Dataset Structure

The `ecommerce_data/` directory contains 6 CSV files:
- `orders_dataset.csv` - Order information and status
- `order_items_dataset.csv` - Line items with product and price
- `products_dataset.csv` - Product categories
- `customers_dataset.csv` - Customer state information
- `order_reviews_dataset.csv` - Review scores
- `order_payments_dataset.csv` - Payment details

## Development Notes

### When Working with the Lesson 7 Code

- Always use `.copy()` when creating filtered DataFrames to avoid warnings
- The project expects data in `lesson7_files/ecommerce_data/` subdirectory
- Year filters should be configured at the top of notebooks, not hard-coded in functions
- All visualization functions return Plotly figure objects

### Testing

Run `test_comparison.py` to validate that refactored code produces identical results to original analysis. All 10 tests should pass.

### Documentation Files

The project includes extensive documentation:
- `README.md` - Complete project documentation with examples
- `README_REFACTORED.md` - Quick reference for refactored implementation
- Inline docstrings in all modules

## Course Repository References

The course uses external repositories for lessons 2-6 and lesson 8 (links in `links_to_course_repos.md`):
- RAG chatbot starting/final repos (lessons 3-5)
- FRED dashboard repo (lesson 8)

These are reference materials only and not included in this repository.
