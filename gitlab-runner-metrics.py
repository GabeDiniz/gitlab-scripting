import json
import os

import requests

# GitLab API configuration
GITLAB_GRAPHQL_URL = "https://gitlab.instance.net/api/graphql"
ACCESS_TOKEN = os.getenv("GITLAB_TOKEN")


#  GraphQL query to retrieve runners with required fields
GRAPHQL_QUERY = """
query ($afterCursor: String) {
  runners(first: 100, after: $afterCursor) {
    nodes {
      id
      tagList
      status
      description
      managers {
        nodes {
          ipAddress
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_all_runners():
    """
    Fetches all GitLab runners with their details and unique IP addresses.
    """
    runners_data = []
    after_cursor = None

    while True:
        # Define variables for pagination
        variables = {"afterCursor": after_cursor}

        # Make a request to GitLab GraphQL API
        response = requests.post(
            GITLAB_GRAPHQL_URL,
            json={"query": GRAPHQL_QUERY, "variables": variables},
            headers=HEADERS
        )
        data = response.json()

        # Check for errors
        if "errors" in data:
            print("Error in API response:", data["errors"])
            break

        # Extract runners
        runners = data.get("data", {}).get("runners", {}).get("nodes", [])
        for runner in runners:
            ip_addresses = {manager["ipAddress"] for manager in runner.get("managers", {}).get("nodes", []) if manager.get("ipAddress")}

            runners_data.append({
                "id": (runner.get("id")).split('Runner/')[1],
                "tagList": runner.get("tagList", []),
                "status": runner.get("status"),
                "description": runner.get("description"),
                "ip_addresses": list(ip_addresses)  # Remove duplicates
            })

        # Pagination handling
        page_info = data.get("data", {}).get("runners", {}).get("pageInfo", {})
        after_cursor = page_info.get("endCursor")
        if not page_info.get("hasNextPage"):
            break

    return runners_data

def save_to_json(data, filename="gitlab_runners.json"):
    """
    Saves the retrieved runner data to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    runners = fetch_all_runners()
    save_to_json(runners)
