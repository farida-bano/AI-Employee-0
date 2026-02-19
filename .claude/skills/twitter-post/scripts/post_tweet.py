import os
import argparse
import datetime
from requests_oauthlib import OAuth1Session

def log_to_vault(content):
    vault_path = os.path.join("AI_Employee_Vault", "reports", "twitter_history.log")
    os.makedirs(os.path.dirname(vault_path), exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    with open(vault_path, "a") as f:
        f.write(f"[{timestamp}] Content: {content}
")

def post_tweet(content):
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET environment variables must be set.")
        return

    payload = {"text": content}
    twitter = OAuth1Session(api_key, client_secret=api_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)

    try:
        response = twitter.post("https://api.twitter.com/2/tweets", json=payload)
        if response.status_code == 201:
            log_to_vault(content)
            print("Success: Tweet posted.")
        else:
            print(f"Error: Failed to post tweet. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error: Failed to post tweet. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tweet on Twitter (X).")
    parser.add_argument("--content", required=True, help="The text content of the tweet.")
    args = parser.parse_args()

    post_tweet(args.content)
