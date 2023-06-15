import posts
import ai

NEW_POST_LIMIT = 3

def main():
    all_posts = posts.get_posts()
    new_posts = posts.filter_posts(all_posts, limit=NEW_POST_LIMIT)

    for post in new_posts:
        posts.download_post_images(post)

    ai.scan_unscanned_posts()
    ai.write_scan_manifest()

if __name__ == "__main__":
    main()
