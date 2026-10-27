import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def scrape_books_data():
  # Scraping a publicly accessible sandbox e-commerce site for demonstration
  base_url = "http://books.toscrape.com/catalogue/page-1.html"
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

  response = requests.get(base_url, headers=headers)
  if response.status_code != 200:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")
    return

  soup = BeautifulSoup(response.text, "html.parser")
  products = soup.find_all("article", class_="product_pod")

  scraped_data = []
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  for item in products:
    title = item.h3.a["title"]
    price_text = item.find("p", class_="price_color").text.strip()
    price = float(price_text.replace("Â£", "").replace("£", ""))
    availability = item.find("p", class_="instock availability").text.strip()

    scraped_data.append({
        "Product_Title": title,
        "Price_GBP": price,
        "Availability": availability,
        "Scraped_At": timestamp,
    })

  # Save to CSV
  output_file = "scraped_products.csv"
  fieldnames = ["Product_Title", "Price_GBP", "Availability", "Scraped_At"]

  with open(
      output_file, mode="w", newline="", encoding="utf-8"
  ) as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scraped_data)

  print(
      f"Successfully scraped {len(scraped_data)} records and exported to"
      f" '{output_file}'."
  )


if __name__ == "__main__":
  scrape_books_data()
