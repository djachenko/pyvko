from api import Api


def main():
    api = Api()

    test_group = api.get_group("pyvko_test")

    posts = test_group.posts()

    post_ids = [post.id for post in posts]

    for post_id in post_ids:
        test_group.delete_post(post_id)


if __name__ == '__main__':
    main()
