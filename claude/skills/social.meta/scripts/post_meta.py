import os
import argparse
import datetime
import requests

def log_social(platform, content, status):
    log_path = os.path.join("logs", "social", "log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] Platform: {platform}, Status: {status}, Content: {content}
")

def post_facebook(content):
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    
    if not all([page_id, access_token]):
        print("Error: FACEBOOK_PAGE_ID and FACEBOOK_PAGE_ACCESS_TOKEN must be set.")
        return

    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    payload = {"message": content, "access_token": access_token}
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            log_social("Facebook", content, "Success")
            print("Success: Facebook post created.")
        else:
            log_social("Facebook", content, f"Error: {response.text}")
            print(f"Error: Failed to post to Facebook. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        log_social("Facebook", content, f"Exception: {str(e)}")
        print(f"Error: Failed to post to Facebook. {e}")

def post_instagram(content, image_url):
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    if not all([account_id, access_token, image_url]):
        print("Error: INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN, and image_url must be set.")
        return

    # 1. Create Media Container
    media_url = f"https://graph.facebook.com/v18.0/{account_id}/media"
    payload = {
        "image_url": image_url,
        "caption": content,
        "access_token": access_token
    }
    
    try:
        res = requests.post(media_url, data=payload)
        res.raise_for_status()
        container_id = res.json().get("id")
        
        # 2. Publish Media
        publish_url = f"https://graph.facebook.com/v18.0/{account_id}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": access_token
        }
        res_publish = requests.post(publish_url, data=publish_payload)
        if res_publish.status_code == 200:
            log_social("Instagram", content, "Success")
            print("Success: Instagram post created.")
        else:
            log_social("Instagram", content, f"Error Publish: {res_publish.text}")
            print(f"Error: Failed to publish to Instagram. Status code: {res_publish.status_code}, Response: {res_publish.text}")
    except Exception as e:
        log_social("Instagram", content, f"Exception: {str(e)}")
        print(f"Error: Failed to post to Instagram. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post to Meta platforms (Facebook/Instagram).")
    parser.add_argument("--platform", required=True, choices=["facebook", "instagram"], help="Target platform.")
    parser.add_argument("--content", required=True, help="Post content/caption.")
    parser.add_argument("--image_url", help="Image URL for Instagram.")
    args = parser.parse_args()

    if args.platform == "facebook":
        post_facebook(args.content)
    elif args.platform == "instagram":
        if not args.image_url:
            print("Error: --image_url is required for Instagram posts.")
        else:
            post_instagram(args.content, args.image_url)
