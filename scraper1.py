import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

base_url = "https://books.toscrape.com/"

books_data = []

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]

    book_link = book.h3.a["href"]
    book_url = urljoin(base_url, book_link)

    detail_response = requests.get(book_url)
    detail_soup = BeautifulSoup(detail_response.text, "html.parser")

    price = detail_soup.find("p", class_="price_color").text.strip()

    availability = detail_soup.find(
        "p",
        class_="instock availability"
    ).text.strip()

    rating = detail_soup.find("p", class_="star-rating")["class"][1]

    table = detail_soup.find("table", class_="table table-striped")

    rows = table.find_all("tr")

    product_info = {}
    for row in rows:
        key = row.th.text.strip()
        value = row.td.text.strip()
        product_info[key] = value

    books_data.append({
        "Title": title,
        "UPC": product_info.get("UPC", ""),
        "Product Type": product_info.get("Product Type", ""),
        "Price (Excl Tax)": product_info.get("Price (excl. tax)", ""),
        "Price (Incl Tax)": product_info.get("Price (incl. tax)", ""),
        "Tax": product_info.get("Tax", ""),
        "Availability": availability,
        "Rating": rating
    })

df = pd.DataFrame(books_data)

df.to_csv("books_dataset.csv", index=False)

print(f"Success! {len(df)} records saved to books_dataset.csv")