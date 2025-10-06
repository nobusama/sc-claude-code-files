#!/usr/bin/env python3
"""
Comparison test showing old vs new approach for SettingWithCopyWarning.

This script demonstrates the problems in the original code and how the
refactored modules solve them.
"""

import warnings
import pandas as pd

print("=" * 80)
print("SETTINGWITHCOPYWARNING - BEFORE vs AFTER COMPARISON")
print("=" * 80)

# Sample data
sample_data = pd.DataFrame({
    'order_id': ['ord1', 'ord2', 'ord3'],
    'status': ['delivered', 'delivered', 'canceled'],
    'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'price': [100, 200, 150]
})

print("\n❌ OLD APPROACH (Original Notebook)")
print("-" * 80)
print("This code generates SettingWithCopyWarning:")
print()
print("  sales_delivered = sample_data[sample_data['status'] == 'delivered']")
print("  sales_delivered['date'] = pd.to_datetime(sales_delivered['date'])")
print()

# Capture warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")

    # Original problematic code
    sales_delivered = sample_data[sample_data['status'] == 'delivered']
    sales_delivered['date'] = pd.to_datetime(sales_delivered['date'])

    if w:
        print(f"⚠️  WARNING GENERATED: {len(w)} warning(s)")
        print(f"    Type: {w[0].category.__name__}")
        print(f"    Message: A value is trying to be set on a copy of a slice...")
    else:
        print("✓ No warnings")

print("\n✅ NEW APPROACH (Refactored Modules)")
print("-" * 80)
print("This code uses .copy() to avoid warnings:")
print()
print("  sales_delivered = sample_data[sample_data['status'] == 'delivered'].copy()")
print("  sales_delivered['date'] = pd.to_datetime(sales_delivered['date'])")
print()

# Capture warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")

    # New corrected code
    sales_delivered = sample_data[sample_data['status'] == 'delivered'].copy()
    sales_delivered['date'] = pd.to_datetime(sales_delivered['date'])

    if w:
        print(f"⚠️  WARNING GENERATED: {len(w)} warning(s)")
    else:
        print("✓ No warnings generated!")

print("\n🔍 LOCATIONS FIXED IN REFACTORED CODE")
print("-" * 80)
locations = [
    ("data_loader.py:74", "sales_filtered = sales_data[...].copy()"),
    ("data_loader.py:78", "sales_filtered['order_purchase_timestamp'] = ..."),
    ("data_loader.py:82", "sales_filtered['month'] = ..."),
    ("data_loader.py:83", "sales_filtered['year'] = ..."),
    ("data_loader.py:99", "sales_with_delivery = sales_data.copy()")
]

for i, (location, fix) in enumerate(locations, 1):
    print(f"  {i}. {location:25} → {fix}")

print("\n📊 ORIGINAL NOTEBOOK WARNINGS")
print("-" * 80)
original_warnings = [
    ("Cell [23]", "sales_delivered['order_purchase_timestamp'] = pd.to_datetime(...)"),
    ("Cell [24]", "sales_delivered['month'] = sales_delivered[...].apply(lambda ...)"),
    ("Cell [25]", "sales_delivered['year'] = sales_delivered[...].apply(lambda ...)"),
    ("Cell [59]", "sales_delivered_2023['order_delivered_customer_date'] = pd.to_datetime(...)"),
    ("Cell [60]", "sales_delivered_2023['delivery_speed'] = (...).apply(lambda t: t.days)")
]

for i, (cell, code) in enumerate(original_warnings, 1):
    print(f"  {i}. {cell:12} {code}")

print("\n✅ ALL FIXED IN REFACTORED VERSION")
print("=" * 80)

# Now test the actual modules
print("\n🧪 TESTING REFACTORED MODULES")
print("-" * 80)

try:
    # Enable strict warning mode
    warnings.filterwarnings('error', category=pd.errors.SettingWithCopyWarning)

    from data_loader import EcommerceDataLoader
    from business_metrics import BusinessMetrics

    loader = EcommerceDataLoader('ecommerce_data/')
    datasets = loader.load_all_data()
    sales = loader.process_sales_data(datasets['orders'], datasets['order_items'])

    metrics = BusinessMetrics(2023, 2022)
    summary = metrics.get_summary_metrics(sales)

    print("✓ All modules loaded successfully")
    print("✓ All data processed without warnings")
    print(f"✓ Calculated {len(summary)} metrics")
    print(f"✓ Total revenue: ${summary['total_revenue']:,.2f}")
    print("\n✅ SUCCESS - No SettingWithCopyWarnings detected!")

except pd.errors.SettingWithCopyWarning as e:
    print(f"❌ FAILED - SettingWithCopyWarning detected: {e}")
except Exception as e:
    print(f"❌ FAILED - Error: {e}")

print("=" * 80)
