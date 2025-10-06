"""
Data loader module for e-commerce data processing.

This module provides the EcommerceDataLoader class for loading and preprocessing
e-commerce datasets including orders, order items, products, customers, and reviews.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Tuple


class EcommerceDataLoader:
    """
    Handles loading and preprocessing of e-commerce data from CSV files.

    This class provides methods to load all e-commerce datasets and process
    sales data with proper handling of datetime conversions and data filtering.

    Attributes:
        data_path (str): Path to the directory containing CSV files.
    """

    def __init__(self, data_path: str = 'ecommerce_data/'):
        """
        Initialize the data loader with the path to data files.

        Args:
            data_path (str): Path to directory containing CSV files. Defaults to 'ecommerce_data/'.
        """
        self.data_path = Path(data_path)
        self._validate_data_path()

    def _validate_data_path(self) -> None:
        """Validate that the data path exists."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data path not found: {self.data_path}")

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all e-commerce datasets from CSV files.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets:
                - 'orders': Orders dataset
                - 'order_items': Order items dataset
                - 'products': Products dataset
                - 'customers': Customers dataset
                - 'reviews': Reviews dataset

        Raises:
            FileNotFoundError: If any required CSV file is missing.
        """
        datasets = {}

        # Define file mappings
        files = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv',
            'products': 'products_dataset.csv',
            'customers': 'customers_dataset.csv',
            'reviews': 'order_reviews_dataset.csv'
        }

        # Load each dataset
        for name, filename in files.items():
            file_path = self.data_path / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Required file not found: {file_path}")
            datasets[name] = pd.read_csv(file_path)

        return datasets

    def process_sales_data(
        self,
        orders: pd.DataFrame,
        order_items: pd.DataFrame,
        status_filter: str = 'delivered'
    ) -> pd.DataFrame:
        """
        Process and merge sales data with proper datetime handling.

        This method merges orders and order items, filters by order status,
        and extracts temporal features (month, year) from order timestamps.
        All operations use proper .copy() to avoid SettingWithCopyWarning.

        Args:
            orders (pd.DataFrame): Orders dataset with order information.
            order_items (pd.DataFrame): Order items dataset with product and price info.
            status_filter (str): Order status to filter by. Defaults to 'delivered'.

        Returns:
            pd.DataFrame: Processed sales data with columns:
                - order_id, order_item_id, product_id, price
                - order_status, order_purchase_timestamp, order_delivered_customer_date
                - month, year
        """
        # Merge order items with orders
        sales_data = pd.merge(
            left=order_items[['order_id', 'order_item_id', 'product_id', 'price']],
            right=orders[[
                'order_id',
                'order_status',
                'order_purchase_timestamp',
                'order_delivered_customer_date'
            ]],
            on='order_id'
        )

        # Filter by status and create a proper copy
        sales_filtered = sales_data[sales_data['order_status'] == status_filter].copy()

        # Convert timestamp to datetime
        sales_filtered['order_purchase_timestamp'] = pd.to_datetime(
            sales_filtered['order_purchase_timestamp']
        )

        # Extract temporal features
        sales_filtered['month'] = sales_filtered['order_purchase_timestamp'].dt.month
        sales_filtered['year'] = sales_filtered['order_purchase_timestamp'].dt.year

        return sales_filtered

    def add_delivery_metrics(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """
        Add delivery speed metrics to sales data.

        Calculates the number of days between order purchase and delivery.

        Args:
            sales_data (pd.DataFrame): Sales data with order timestamps.

        Returns:
            pd.DataFrame: Sales data with added 'delivery_speed' column (days).
        """
        # Create a copy to avoid SettingWithCopyWarning
        sales_with_delivery = sales_data.copy()

        # Convert delivery date to datetime if not already
        if sales_with_delivery['order_delivered_customer_date'].dtype == 'object':
            sales_with_delivery['order_delivered_customer_date'] = pd.to_datetime(
                sales_with_delivery['order_delivered_customer_date']
            )

        # Calculate delivery speed in days
        sales_with_delivery['delivery_speed'] = (
            sales_with_delivery['order_delivered_customer_date'] -
            sales_with_delivery['order_purchase_timestamp']
        ).dt.days

        return sales_with_delivery

    def categorize_delivery_speed(self, days: int) -> str:
        """
        Categorize delivery speed into time buckets.

        Args:
            days (int): Number of days for delivery.

        Returns:
            str: Delivery time category ('1-3 days', '4-7 days', or '8+ days').
        """
        if days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'

    def merge_sales_with_customers(
        self,
        sales_data: pd.DataFrame,
        orders: pd.DataFrame,
        customers: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge sales data with customer information.

        Args:
            sales_data (pd.DataFrame): Processed sales data.
            orders (pd.DataFrame): Orders dataset.
            customers (pd.DataFrame): Customers dataset.

        Returns:
            pd.DataFrame: Sales data merged with customer state information.
        """
        # First merge with orders to get customer_id
        sales_with_customers = pd.merge(
            left=sales_data[['order_id', 'price']],
            right=orders[['order_id', 'customer_id']],
            on='order_id'
        )

        # Then merge with customers to get customer_state
        sales_with_state = pd.merge(
            left=sales_with_customers,
            right=customers[['customer_id', 'customer_state']],
            on='customer_id'
        )

        return sales_with_state

    def merge_sales_with_categories(
        self,
        sales_data: pd.DataFrame,
        products: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge sales data with product categories.

        Args:
            sales_data (pd.DataFrame): Processed sales data.
            products (pd.DataFrame): Products dataset.

        Returns:
            pd.DataFrame: Sales data merged with product category information.
        """
        return pd.merge(
            left=products[['product_id', 'product_category_name']],
            right=sales_data[['product_id', 'price']],
            on='product_id'
        )
