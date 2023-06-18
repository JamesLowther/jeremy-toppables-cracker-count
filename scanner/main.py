import posts
import ai
import webhook

NEW_POST_LIMIT = None

def main():
    try:
        all_posts = posts.get_posts()
        new_posts = posts.filter_posts(all_posts, limit=NEW_POST_LIMIT)
        new_posts_count = len(new_posts)

        new_image_count = 0

        for post in new_posts:
            new_image_count += posts.download_post_images(post)

        new_scan_count = ai.scan_unscanned_posts()
        ai.write_scan_manifest()

        webhook.send_webhook(new_posts_count, new_image_count, new_scan_count)

    except Exception as e:
        print(f"Error: {e}")
        webhook.send_error(e)

        exit(1)

if __name__ == "__main__":
    main()
