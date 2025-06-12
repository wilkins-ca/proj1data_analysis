# Data Analytics Project: Sales Insights from a Normalized Database

---

## 🧾 Summary
This project explores purchasing behavior using a sales dataset sourced from Kaggle, with a focus on location, shipping method, and customer type. The primary goal was to demonstrate best practices in data normalization and SQL querying using PostgreSQL and SQLAlchemy, while also modeling data wrangling in Python with pandas.

---

## ❓ Why This Project?
I chose this dataset because it was just large enough to present a meaningful challenge: structuring a normalized database schema from a flat `.csv` source, preparing foreign key relationships, and loading the data using SQLAlchemy. I also wanted hands-on experience extracting business insights from real-world-style sales data.

---

## 🏗️ What I Built
Starting with a `.csv` file, I loaded the data into a pandas DataFrame, checked for null values, and removed non-essential columns. I then engineered two new fields:

- **Retail Price**: calculated from sales total, quantity sold, and discount  
- **High Price Flag**: a boolean marking when a retail price is in the top 20% of all retail prices in the dataset

I created new ID columns to represent future foreign keys, built a normalized schema using SQLAlchemy ORM classes, and loaded the data into PostgreSQL. I then wrote multi-table SQL queries to analyze and extract insights.

---

## 🧠 What I Learned and Solved
One of the trickier parts of the process was setting up the foreign key fields in the pandas DataFrame before loading them into PostgreSQL. I used Python’s `map()` function to replace string labels with numerical foreign keys during normalization—splitting attributes like category, subcategory, segment, and shipping mode into dimension tables.

I also gained practical troubleshooting experience with PostgreSQL, especially around `GROUP BY` and aggregation behavior, as well as typecasting for numeric rounding.

---

## 📊 Insights Derived

<details>
<summary><strong>Top 10 cities with the highest total sales</strong></summary>

```sql
SELECT 
  sales.city, 
  sales.state, 
  ROUND(SUM(sales_total)::numeric, 2) AS sales_sum
FROM sales
GROUP BY sales.city, sales.state
ORDER BY sales_sum DESC
LIMIT 10;
```
</details> <details> <summary><strong>Average profit for each customer segment</strong></summary>

```sql
SELECT 
  ROUND(AVG(sales.profit)::numeric, 2) AS avg_profit, 
  segments.seg
FROM sales
JOIN segments ON sales.segment = segments.id
GROUP BY segments.seg;
```


</details> <details> <summary><strong>Subcategories with the least overall profit</strong></summary>

```sql
SELECT 
  subcats.subcat, 
  ROUND(AVG(sales.profit)::numeric, 2) AS avg_profit
FROM sales
JOIN subcats ON sales.subcat = subcats.id
GROUP BY subcats.subcat
ORDER BY avg_profit
LIMIT 5;
```

</details> <details> <summary><strong>Sales totals by shipping mode and customer segment</strong></summary>

```sql
SELECT 
  ROUND(SUM(sales.sales_total)::numeric, 2) AS total_sales, 
  segments.seg, 
  shippingmode.mode
FROM sales
JOIN shippingmode ON sales.ship_mode = shippingmode.id
JOIN segments ON sales.segment = segments.id
GROUP BY shippingmode.mode, segments.seg
ORDER BY total_sales;
```


</details> <details> <summary><strong>Average discount and profit per subcategory</strong></summary>

```sql

SELECT 
  subcats.subcat, 
  ROUND(AVG(sales.discount)::numeric, 2) AS avg_discount, 
  ROUND(AVG(sales.profit)::numeric, 2) AS avg_profit
FROM subcats
JOIN sales ON subcats.id = sales.subcat
GROUP BY subcats.subcat;
```

</details>


## ✅ Applied Knowledge

This project demonstrates my ability to:

    - Normalize raw data into a relational database schema

    - Use SQLAlchemy ORM for data modeling and loading

    - Transform and enrich data with pandas

    - Write multi-table SQL queries to generate actionable insights

## 📈 Tableau Visualizations (Coming Soon)
I’ll be adding both embedded Tableau dashboards and links to interactive visualizations hosted online.