"""
Business metrics calculation and visualization module.

This module provides the BusinessMetrics class for calculating key business metrics
and creating interactive Plotly visualizations for e-commerce data analysis.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple, Optional


class BusinessMetrics:
    """
    Handles calculation of business metrics and creation of visualizations.

    This class provides methods to calculate revenue, growth rates, and other
    key performance indicators, as well as generate interactive Plotly charts.

    Attributes:
        analysis_year (int): Primary year for analysis.
        comparison_year (int): Previous year for comparison.
    """

    def __init__(self, analysis_year: int = 2023, comparison_year: int = 2022):
        """
        Initialize the BusinessMetrics calculator.

        Args:
            analysis_year (int): Primary year for analysis. Defaults to 2023.
            comparison_year (int): Previous year for comparison. Defaults to 2022.
        """
        self.analysis_year = analysis_year
        self.comparison_year = comparison_year

    def calculate_revenue(self, sales_data: pd.DataFrame, year: int) -> float:
        """
        Calculate total revenue for a specific year.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year' and 'price' columns.
            year (int): Year to calculate revenue for.

        Returns:
            float: Total revenue for the specified year.
        """
        year_data = sales_data[sales_data['year'] == year]
        return year_data['price'].sum()

    def calculate_revenue_growth(
        self,
        sales_data: pd.DataFrame,
        current_year: Optional[int] = None,
        previous_year: Optional[int] = None
    ) -> float:
        """
        Calculate year-over-year revenue growth rate.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year' and 'price' columns.
            current_year (int, optional): Current year. Defaults to analysis_year.
            previous_year (int, optional): Previous year. Defaults to comparison_year.

        Returns:
            float: Revenue growth rate as a decimal (e.g., 0.05 for 5% growth).
        """
        current_year = current_year or self.analysis_year
        previous_year = previous_year or self.comparison_year

        current_revenue = self.calculate_revenue(sales_data, current_year)
        previous_revenue = self.calculate_revenue(sales_data, previous_year)

        if previous_revenue == 0:
            return 0.0

        return (current_revenue - previous_revenue) / previous_revenue

    def calculate_monthly_growth(
        self,
        sales_data: pd.DataFrame,
        year: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate month-over-month growth rate for a specific year.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year', 'month', and 'price' columns.
            year (int, optional): Year to calculate growth for. Defaults to analysis_year.

        Returns:
            pd.Series: Month-over-month growth rates indexed by month.
        """
        year = year or self.analysis_year
        year_data = sales_data[sales_data['year'] == year]

        monthly_revenue = year_data.groupby('month')['price'].sum()
        monthly_growth = monthly_revenue.pct_change()

        return monthly_growth

    def calculate_average_order_value(
        self,
        sales_data: pd.DataFrame,
        year: Optional[int] = None
    ) -> float:
        """
        Calculate average order value for a specific year.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year', 'order_id', and 'price' columns.
            year (int, optional): Year to calculate AOV for. Defaults to analysis_year.

        Returns:
            float: Average order value.
        """
        year = year or self.analysis_year
        year_data = sales_data[sales_data['year'] == year]

        return year_data.groupby('order_id')['price'].sum().mean()

    def calculate_total_orders(
        self,
        sales_data: pd.DataFrame,
        year: Optional[int] = None
    ) -> int:
        """
        Calculate total number of unique orders for a specific year.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year' and 'order_id' columns.
            year (int, optional): Year to calculate orders for. Defaults to analysis_year.

        Returns:
            int: Total number of unique orders.
        """
        year = year or self.analysis_year
        year_data = sales_data[sales_data['year'] == year]

        return year_data['order_id'].nunique()

    def calculate_order_growth(
        self,
        sales_data: pd.DataFrame,
        current_year: Optional[int] = None,
        previous_year: Optional[int] = None
    ) -> float:
        """
        Calculate year-over-year order count growth rate.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year' and 'order_id' columns.
            current_year (int, optional): Current year. Defaults to analysis_year.
            previous_year (int, optional): Previous year. Defaults to comparison_year.

        Returns:
            float: Order count growth rate as a decimal.
        """
        current_year = current_year or self.analysis_year
        previous_year = previous_year or self.comparison_year

        current_orders = self.calculate_total_orders(sales_data, current_year)
        previous_orders = self.calculate_total_orders(sales_data, previous_year)

        if previous_orders == 0:
            return 0.0

        return (current_orders - previous_orders) / previous_orders

    def get_summary_metrics(self, sales_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate all key summary metrics for the analysis year.

        Args:
            sales_data (pd.DataFrame): Complete sales data.

        Returns:
            Dict[str, float]: Dictionary containing:
                - total_revenue: Total revenue for analysis year
                - revenue_growth: YoY revenue growth rate
                - avg_order_value: Average order value
                - aov_growth: YoY AOV growth rate
                - total_orders: Total number of orders
                - order_growth: YoY order count growth rate
                - avg_monthly_growth: Average month-over-month growth rate
        """
        metrics = {
            'total_revenue': self.calculate_revenue(sales_data, self.analysis_year),
            'revenue_growth': self.calculate_revenue_growth(sales_data),
            'avg_order_value': self.calculate_average_order_value(sales_data),
            'total_orders': self.calculate_total_orders(sales_data),
            'order_growth': self.calculate_order_growth(sales_data)
        }

        # Calculate AOV growth
        current_aov = self.calculate_average_order_value(sales_data, self.analysis_year)
        previous_aov = self.calculate_average_order_value(sales_data, self.comparison_year)
        metrics['aov_growth'] = (current_aov - previous_aov) / previous_aov if previous_aov != 0 else 0.0

        # Calculate average monthly growth
        monthly_growth = self.calculate_monthly_growth(sales_data)
        metrics['avg_monthly_growth'] = monthly_growth.mean()

        return metrics

    # Visualization methods

    def create_monthly_revenue_chart(
        self,
        sales_data: pd.DataFrame,
        year: Optional[int] = None
    ) -> go.Figure:
        """
        Create an interactive line chart showing monthly revenue trend.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year', 'month', and 'price' columns.
            year (int, optional): Year to visualize. Defaults to analysis_year.

        Returns:
            go.Figure: Plotly figure object.
        """
        year = year or self.analysis_year
        year_data = sales_data[sales_data['year'] == year]

        monthly_revenue = year_data.groupby('month')['price'].sum().reset_index()
        monthly_revenue.columns = ['Month', 'Revenue']

        fig = px.line(
            monthly_revenue,
            x='Month',
            y='Revenue',
            title=f'Monthly Revenue Trend - {year}',
            markers=True
        )

        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )

        fig.update_traces(
            line_color='#1f77b4',
            line_width=3,
            marker_size=8
        )

        return fig

    def create_category_revenue_chart(
        self,
        sales_categories: pd.DataFrame,
        top_n: int = 10
    ) -> go.Figure:
        """
        Create an interactive bar chart showing revenue by product category.

        Args:
            sales_categories (pd.DataFrame): Sales data with 'product_category_name' and 'price'.
            top_n (int): Number of top categories to display. Defaults to 10.

        Returns:
            go.Figure: Plotly figure object.
        """
        category_revenue = (
            sales_categories
            .groupby('product_category_name')['price']
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        category_revenue.columns = ['Category', 'Revenue']

        fig = px.bar(
            category_revenue,
            x='Revenue',
            y='Category',
            orientation='h',
            title=f'Top {top_n} Product Categories by Revenue',
            color='Revenue',
            color_continuous_scale='Blues'
        )

        fig.update_layout(
            xaxis_title='Revenue ($)',
            yaxis_title='Category',
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white',
            height=500
        )

        return fig

    def create_state_revenue_map(self, sales_by_state: pd.DataFrame) -> go.Figure:
        """
        Create an interactive choropleth map showing revenue by US state.

        Args:
            sales_by_state (pd.DataFrame): Sales data with 'customer_state' and 'price' columns.

        Returns:
            go.Figure: Plotly figure object.
        """
        state_revenue = (
            sales_by_state
            .groupby('customer_state')['price']
            .sum()
            .reset_index()
        )
        state_revenue.columns = ['State', 'Revenue']

        fig = px.choropleth(
            state_revenue,
            locations='State',
            color='Revenue',
            locationmode='USA-states',
            scope='usa',
            title=f'Revenue by State - {self.analysis_year}',
            color_continuous_scale='Reds',
            hover_data={'Revenue': ':,.2f'}
        )

        fig.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            template='plotly_white',
            height=600
        )

        return fig

    def create_review_score_chart(self, review_data: pd.DataFrame) -> go.Figure:
        """
        Create an interactive bar chart showing review score distribution.

        Args:
            review_data (pd.DataFrame): Data with 'review_score' column.

        Returns:
            go.Figure: Plotly figure object.
        """
        review_dist = (
            review_data['review_score']
            .value_counts(normalize=True)
            .sort_index()
            .reset_index()
        )
        review_dist.columns = ['Review Score', 'Percentage']
        review_dist['Percentage'] = review_dist['Percentage'] * 100

        fig = px.bar(
            review_dist,
            x='Review Score',
            y='Percentage',
            title='Customer Review Score Distribution',
            color='Percentage',
            color_continuous_scale='Greens'
        )

        fig.update_layout(
            xaxis_title='Review Score',
            yaxis_title='Percentage (%)',
            template='plotly_white',
            height=500,
            xaxis={'type': 'category'}
        )

        return fig

    def create_delivery_time_chart(
        self,
        review_speed_data: pd.DataFrame
    ) -> go.Figure:
        """
        Create a bar chart showing average review scores by delivery time.

        Args:
            review_speed_data (pd.DataFrame): Data with 'delivery_time' and 'review_score'.

        Returns:
            go.Figure: Plotly figure object.
        """
        delivery_reviews = (
            review_speed_data
            .groupby('delivery_time')['review_score']
            .mean()
            .reset_index()
        )
        delivery_reviews.columns = ['Delivery Time', 'Avg Review Score']

        # Order categories properly
        category_order = ['1-3 days', '4-7 days', '8+ days']
        delivery_reviews['Delivery Time'] = pd.Categorical(
            delivery_reviews['Delivery Time'],
            categories=category_order,
            ordered=True
        )
        delivery_reviews = delivery_reviews.sort_values('Delivery Time')

        fig = px.bar(
            delivery_reviews,
            x='Delivery Time',
            y='Avg Review Score',
            title='Average Review Score by Delivery Speed',
            color='Avg Review Score',
            color_continuous_scale='RdYlGn',
            range_color=[3.5, 5.0]
        )

        fig.update_layout(
            xaxis_title='Delivery Time',
            yaxis_title='Average Review Score',
            template='plotly_white',
            height=500
        )

        return fig

    def create_order_status_chart(
        self,
        orders: pd.DataFrame,
        year: Optional[int] = None
    ) -> go.Figure:
        """
        Create a pie chart showing order status distribution.

        Args:
            orders (pd.DataFrame): Orders data with 'order_status' column.
            year (int, optional): Year to filter by. Defaults to analysis_year.

        Returns:
            go.Figure: Plotly figure object.
        """
        year = year or self.analysis_year

        # Filter by year and get status distribution
        status_dist = (
            orders[orders['year'] == year]['order_status']
            .value_counts()
            .reset_index()
        )
        status_dist.columns = ['Status', 'Count']

        fig = px.pie(
            status_dist,
            values='Count',
            names='Status',
            title=f'Order Status Distribution - {year}',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )

        fig.update_layout(
            template='plotly_white',
            height=500
        )

        return fig

    def create_monthly_growth_chart(
        self,
        sales_data: pd.DataFrame,
        year: Optional[int] = None
    ) -> go.Figure:
        """
        Create a bar chart showing month-over-month growth rates.

        Args:
            sales_data (pd.DataFrame): Sales data with 'year', 'month', and 'price'.
            year (int, optional): Year to visualize. Defaults to analysis_year.

        Returns:
            go.Figure: Plotly figure object.
        """
        year = year or self.analysis_year
        monthly_growth = self.calculate_monthly_growth(sales_data, year)

        growth_df = monthly_growth.reset_index()
        growth_df.columns = ['Month', 'Growth Rate']
        growth_df['Growth Rate'] = growth_df['Growth Rate'] * 100
        growth_df = growth_df.dropna()  # Remove first month with NaN

        # Color bars based on positive/negative growth
        colors = ['green' if x >= 0 else 'red' for x in growth_df['Growth Rate']]

        fig = go.Figure(data=[
            go.Bar(
                x=growth_df['Month'],
                y=growth_df['Growth Rate'],
                marker_color=colors,
                text=growth_df['Growth Rate'].round(2),
                texttemplate='%{text}%',
                textposition='outside'
            )
        ])

        fig.update_layout(
            title=f'Month-over-Month Growth Rate - {year}',
            xaxis_title='Month',
            yaxis_title='Growth Rate (%)',
            template='plotly_white',
            height=500,
            showlegend=False
        )

        return fig
