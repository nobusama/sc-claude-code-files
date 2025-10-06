# Usage Examples

This document provides quick examples for using the refactored e-commerce analysis modules.

## Quick Start

### 1. Running the Complete Analysis

Simply open and run the refactored notebook:

```bash
jupyter notebook EDA_Refactored.ipynb
```

The notebook will:
- Load all datasets
- Calculate key business metrics
- Generate 7 interactive Plotly visualizations
- Display comprehensive summary insights

### 2. Changing the Analysis Period

Edit the configuration constants at the top of the notebook:

```python
# Analyze 2024 vs 2023 instead of 2023 vs 2022
ANALYSIS_YEAR = 2024
COMPARISON_YEAR = 2023
DATA_PATH = 'ecommerce_data/'
```

Run all cells and the entire analysis updates automatically!

## Using Modules Independently

### Example 1: Basic Data Loading

```python
from data_loader import EcommerceDataLoader

# Initialize loader
loader = EcommerceDataLoader(data_path='ecommerce_data/')

# Load all datasets
datasets = loader.load_all_data()

# Access individual datasets
orders = datasets['orders']
products = datasets['products']
customers = datasets['customers']

print(f"Loaded {len(orders)} orders")
print(f"Loaded {len(products)} products")
```

### Example 2: Processing Sales Data

```python
from data_loader import EcommerceDataLoader

loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()

# Process delivered orders with temporal features
sales = loader.process_sales_data(
    orders=datasets['orders'],
    order_items=datasets['order_items'],
    status_filter='delivered'
)

# Data now includes: month, year columns
print(sales[['order_id', 'price', 'month', 'year']].head())

# Filter by year
sales_2023 = sales[sales['year'] == 2023]
print(f"Total 2023 sales: ${sales_2023['price'].sum():,.2f}")
```

### Example 3: Calculating Business Metrics

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

# Load and process data
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Calculate metrics for 2023 vs 2022
metrics = BusinessMetrics(analysis_year=2023, comparison_year=2022)

# Get complete summary
summary = metrics.get_summary_metrics(sales)

print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
print(f"Revenue Growth: {summary['revenue_growth']:.2%}")
print(f"Avg Order Value: ${summary['avg_order_value']:,.2f}")
print(f"Total Orders: {summary['total_orders']:,}")
```

### Example 4: Individual Metric Calculations

```python
from business_metrics import BusinessMetrics

metrics = BusinessMetrics(analysis_year=2023, comparison_year=2022)

# Calculate specific metrics
total_revenue = metrics.calculate_revenue(sales, year=2023)
revenue_growth = metrics.calculate_revenue_growth(sales)
aov = metrics.calculate_average_order_value(sales, year=2023)
total_orders = metrics.calculate_total_orders(sales, year=2023)
monthly_growth = metrics.calculate_monthly_growth(sales, year=2023)

print(f"Revenue: ${total_revenue:,.2f}")
print(f"YoY Growth: {revenue_growth:.2%}")
print(f"AOV: ${aov:,.2f}")
print(f"Orders: {total_orders:,}")
print(f"\nMonthly Growth Rates:")
print(monthly_growth)
```

### Example 5: Creating Visualizations

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

# Setup
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])
metrics = BusinessMetrics(2023, 2022)

# Create monthly revenue trend
fig1 = metrics.create_monthly_revenue_chart(sales, year=2023)
fig1.show()

# Create category analysis
sales_categories = loader.merge_sales_with_categories(
    sales[sales['year'] == 2023],
    datasets['products']
)
fig2 = metrics.create_category_revenue_chart(sales_categories, top_n=10)
fig2.show()

# Create geographic analysis
sales_states = loader.merge_sales_with_customers(
    sales[sales['year'] == 2023],
    datasets['orders'],
    datasets['customers']
)
fig3 = metrics.create_state_revenue_map(sales_states)
fig3.show()
```

### Example 6: Delivery and Review Analysis

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

# Load data
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Add delivery metrics
sales_2023 = sales[sales['year'] == 2023]
sales_with_delivery = loader.add_delivery_metrics(sales_2023)

# Merge with reviews
sales_with_reviews = sales_with_delivery.merge(
    datasets['reviews'][['order_id', 'review_score']],
    on='order_id'
)

# Create unique order-level data
review_data = sales_with_reviews[[
    'order_id', 'delivery_speed', 'review_score'
]].drop_duplicates()

# Categorize delivery speed
review_data['delivery_time'] = review_data['delivery_speed'].apply(
    loader.categorize_delivery_speed
)

# Analyze impact
delivery_impact = review_data.groupby('delivery_time')['review_score'].mean()
print("Delivery Speed Impact on Reviews:")
print(delivery_impact)

# Visualize
metrics = BusinessMetrics(2023, 2022)
fig = metrics.create_delivery_time_chart(review_data)
fig.show()
```

### Example 7: Custom Analysis for Different Years

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

# Compare 2021 vs 2020 instead
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Create metrics calculator for different years
metrics_2021 = BusinessMetrics(analysis_year=2021, comparison_year=2020)

# Get metrics
summary = metrics_2021.get_summary_metrics(sales)
print(f"2021 vs 2020 Analysis:")
print(f"Revenue Growth: {summary['revenue_growth']:.2%}")
print(f"Order Growth: {summary['order_growth']:.2%}")

# Create visualization
fig = metrics_2021.create_monthly_revenue_chart(sales, year=2021)
fig.show()
```

### Example 8: Exporting Data for Further Analysis

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics
import pandas as pd

# Load and process
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Calculate metrics
metrics = BusinessMetrics(2023, 2022)
summary = metrics.get_summary_metrics(sales)

# Export summary to CSV
summary_df = pd.DataFrame([summary])
summary_df.to_csv('metrics_summary_2023.csv', index=False)

# Export monthly data
monthly_revenue = sales[sales['year'] == 2023].groupby('month')['price'].sum()
monthly_revenue.to_csv('monthly_revenue_2023.csv', header=['revenue'])

print("✓ Data exported successfully")
```

### Example 9: Creating a Custom Report

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

def generate_annual_report(year: int, comparison_year: int):
    """Generate a comprehensive annual report."""

    # Load data
    loader = EcommerceDataLoader('ecommerce_data/')
    datasets = loader.load_all_data()
    sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

    # Calculate metrics
    metrics = BusinessMetrics(year, comparison_year)
    summary = metrics.get_summary_metrics(sales)

    # Print report
    print(f"{'=' * 80}")
    print(f"ANNUAL REPORT - {year}")
    print(f"{'=' * 80}\n")

    print(f"Financial Performance:")
    print(f"  Total Revenue:    ${summary['total_revenue']:>15,.2f}")
    print(f"  YoY Growth:       {summary['revenue_growth']:>15.2%}")
    print(f"\nOrder Metrics:")
    print(f"  Total Orders:     {summary['total_orders']:>15,}")
    print(f"  Avg Order Value:  ${summary['avg_order_value']:>15,.2f}")
    print(f"  YoY Order Growth: {summary['order_growth']:>15.2%}")

    print(f"\n{'=' * 80}")

# Use it
generate_annual_report(year=2023, comparison_year=2022)
```

### Example 10: Batch Processing Multiple Years

```python
from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics
import pandas as pd

# Load data once
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Get all years in data
years = sorted(sales['year'].unique())

# Calculate metrics for each year
results = []
for i in range(1, len(years)):
    current_year = years[i]
    previous_year = years[i-1]

    metrics = BusinessMetrics(current_year, previous_year)
    summary = metrics.get_summary_metrics(sales)

    results.append({
        'year': current_year,
        'revenue': summary['total_revenue'],
        'revenue_growth': summary['revenue_growth'],
        'orders': summary['total_orders'],
        'aov': summary['avg_order_value']
    })

# Create DataFrame
results_df = pd.DataFrame(results)
print(results_df)

# Save to CSV
results_df.to_csv('multi_year_analysis.csv', index=False)
```

## Testing for Warnings

To verify no SettingWithCopyWarnings are generated:

```python
import warnings
warnings.filterwarnings('error')  # Convert warnings to errors

from data_loader import EcommerceDataLoader
from business_metrics import BusinessMetrics

try:
    loader = EcommerceDataLoader('ecommerce_data/')
    datasets = loader.load_all_data()
    sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

    metrics = BusinessMetrics(2023, 2022)
    summary = metrics.get_summary_metrics(sales)

    print("✅ Success - No warnings generated!")

except Warning as e:
    print(f"❌ Warning detected: {e}")
```

## Tips

1. **Always use .copy()** when creating filtered DataFrames that you'll modify
2. **Use configuration constants** at the top of notebooks for easy year changes
3. **Reuse the loader instance** for multiple operations instead of recreating it
4. **Cache processed data** if running the same analysis multiple times
5. **Export visualizations** using `fig.write_html('chart.html')` or `fig.write_image('chart.png')`

## Common Patterns

### Pattern 1: Load → Process → Analyze → Visualize

```python
# Load
loader = EcommerceDataLoader('ecommerce_data/')
datasets = loader.load_all_data()

# Process
sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

# Analyze
metrics = BusinessMetrics(2023, 2022)
summary = metrics.get_summary_metrics(sales)

# Visualize
fig = metrics.create_monthly_revenue_chart(sales)
fig.show()
```

### Pattern 2: Filter → Merge → Aggregate

```python
# Filter by year
sales_2023 = sales[sales['year'] == 2023]

# Merge with categories
sales_categories = loader.merge_sales_with_categories(sales_2023, datasets['products'])

# Aggregate
top_categories = sales_categories.groupby('product_category_name')['price'].sum().sort_values(ascending=False)
print(top_categories.head(10))
```

### Pattern 3: Calculate → Compare → Visualize

```python
# Calculate for current year
revenue_2023 = metrics.calculate_revenue(sales, 2023)

# Calculate for previous year
revenue_2022 = metrics.calculate_revenue(sales, 2022)

# Compare
growth = (revenue_2023 - revenue_2022) / revenue_2022
print(f"Growth: {growth:.2%}")

# Visualize
fig = metrics.create_monthly_growth_chart(sales, 2023)
fig.show()
```

## Need Help?

- Check `REFACTORING_SUMMARY.md` for complete documentation
- Review `EDA_Refactored.ipynb` for working examples
- Run `test_comparison.py` to verify no warnings
- All functions have comprehensive docstrings with examples
