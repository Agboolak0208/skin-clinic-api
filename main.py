
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()

# Load the campaign dataset
df = pd.read_csv("skin clinic campaign.csv")


@app.get("/")
def home():
    return {
        "message": "Skin Clinic Campaign Analysis API",
        "customers": len(df)
    }


@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():
    # Task 1: Gender vs Campaign Response
    gender = (
        df.groupby("Gender")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=(
                "Response_to_Campaign",
                lambda x: (x == "Yes").sum()
            )
        )
        .reset_index()
    )

    gender["Response Rate (%)"] = (
        gender["Responded"] / gender["Total_Customers"] * 100
    ).round(2)

    # Task 2: Age Group vs Campaign Response
    age = (
        df.groupby("AgeGroup")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=(
                "Response_to_Campaign",
                lambda x: (x == "Yes").sum()
            )
        )
        .reset_index()
    )

    age["Response Rate (%)"] = (
        age["Responded"] / age["Total_Customers"] * 100
    ).round(2)

    # Task 3: Last-quarter Purchase vs Campaign Response
    purchase = (
        df.groupby("Purchase_Last_Quarter")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=(
                "Response_to_Campaign",
                lambda x: (x == "Yes").sum()
            )
        )
        .reset_index()
    )

    purchase["Response Rate (%)"] = (
        purchase["Responded"] / purchase["Total_Customers"] * 100
    ).round(2)

    # Task 4: Product Usage vs Campaign Response
    product_df = df.copy()

    product_df["Product_Usage_Group"] = pd.cut(
        product_df["Unique_Products_Purchased"],
        bins=[0, 4, 8, float("inf")],
        labels=["1-4", "5-8", ">8"],
        include_lowest=True
    )

    products = (
        product_df.groupby("Product_Usage_Group", observed=False)
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=(
                "Response_to_Campaign",
                lambda x: (x == "Yes").sum()
            )
        )
        .reset_index()
    )

    products["Response Rate (%)"] = (
        products["Responded"] / products["Total_Customers"] * 100
    ).round(2)

    # Display the four analyses as HTML tables
    sections = {
        "1. Gender vs Campaign Response": gender,
        "2. Age Group vs Campaign Response": age,
        "3. Last-quarter Purchase vs Campaign Response": purchase,
        "4. Product Usage vs Campaign Response": products,
    }

    html = """
    <html>
    <head>
        <title>Skin Clinic Campaign Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; }
            table { border-collapse: collapse; margin-bottom: 30px; }
            th, td { border: 1px solid #ccc; padding: 10px; }
            th { background-color: #e8eef7; }
            h1 { color: #243b53; }
        </style>
    </head>
    <body>
        <h1>Skin Clinic Campaign Analysis</h1>
        <p>Total customers analysed: """ + str(len(df)) + "</p>"

    for title, table in sections.items():
        html += f"<h2>{title}</h2>"
        html += table.to_html(index=False, border=0)

    html += "</body></html>"

    return html