import os
import csv
import requests
from googleapiclient.discovery import build
import config  # Import the config file


def fetch_crunchbase_data(query):
    """Fetches data from Crunchbase API."""
    base_url = "https://api.crunchbase.com/v3.1/organizations"
    params = {
        "user_key": config.CRUNCHBASE_API_KEY,
        "name": query,
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if "data" in data:
            return data
        else:
            print("Crunchbase response missing 'data' key.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"Crunchbase API HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Crunchbase API request error: {req_err}")
    except ValueError as parse_err:
        print(f"Error parsing Crunchbase response: {parse_err}")
    return None


def fetch_google_data(query, num_results=10):
    """Fetches data using Google Custom Search JSON API."""
    try:
        service = build("customsearch", "v1", developerKey=config.GOOGLE_API_KEY)
        response = (
            service.cse()
            .list(q=query, cx=config.GOOGLE_CSE_ID, num=num_results)
            .execute()
        )
        if "items" in response:
            return [
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
                for item in response["items"]
            ]
        else:
            print("Google API response missing 'items' key.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Google API network error: {e}")
    except Exception as e:
        print(f"Google API error: {e}")
    return []


def extract_emails_from_results(results):
    """Extracts email addresses from a list of URLs."""
    import re

    emails = set()
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    for result in results:
        if "link" in result:
            try:
                response = requests.get(result["link"], timeout=5)
                response.raise_for_status()
                page_content = response.text
                emails.update(re.findall(email_pattern, page_content))
            except requests.exceptions.RequestException as e:
                print(f"Error accessing {result['link']}: {e}")
    return emails


def save_results_to_csv(filename, headers, data):
    """Saves results to a CSV file in the ./data folder."""
    # Ensure the data folder exists
    os.makedirs("./../data", exist_ok=True)
    filepath = os.path.join("./../data", filename)

    # Write data to the CSV file
    try:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write headers
            writer.writerows(data)    # Write data rows
        print(f"Results saved to {filepath}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")


def main():
    # Example search terms
    crunchbase_query = "tech startups"
    google_query = "Tech startups in Banglore"

    # Fetch data from Crunchbase
    # print("Fetching Crunchbase data...")
    # crunchbase_data = fetch_crunchbase_data(crunchbase_query)
    # if crunchbase_data:
    #     crunchbase_results = []
    #     print("Crunchbase Data:")
    #     for item in crunchbase_data.get("data", {}).get("items", []):
    #         name = item.get("properties", {}).get("name")
    #         website = item.get("properties", {}).get("homepage_url")
    #         email = item.get("properties", {}).get("email")
    #         print(f"Name: {name}")
    #         print(f"Website: {website}")
    #         print(f"Contact Email: {email}")
    #         print("-" * 40)
    #         crunchbase_results.append([name, website, email])

    #     # Save Crunchbase results to CSV
    #     save_results_to_csv(
    #         "crunchbase_results.csv",
    #         ["Name", "Website", "Contact Email"],
    #         crunchbase_results
    #     )
    # else:
    #     print("Failed to retrieve data from Crunchbase.")

    # Fetch data from Google
    print("\nFetching Google search results...")
    google_data = fetch_google_data(google_query)
    if google_data:
        google_results = []
        print("\nGoogle Search Results:")
        for result in google_data:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print("-" * 40)
            google_results.append([result['title'], result['link'], result['snippet']])

        # Save Google search results to CSV
        save_results_to_csv(
            "google_results.csv",
            ["Title", "Link", "Snippet"],
            google_results
        )

        # Extract emails from Google search results
        print("\nExtracting emails from Google search results...")
        emails = extract_emails_from_results(google_data)
        if emails:
            print("Extracted Emails:")
            email_results = [[email] for email in emails]
            for email in emails:
                print(email)

            # Save extracted emails to CSV
            save_results_to_csv(
                "extracted_emails.csv",
                ["Email"],
                email_results
            )
        else:
            print("No emails found.")
    else:
        print("Failed to retrieve data from Google.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
