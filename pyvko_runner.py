from api import Api


def main():
    api = Api()

    current_user = api.current_user()

    groups = current_user.groups()

    for group in groups[:10]:
        print(group)

    for posts in groups[0].posts():
        print(posts)


if __name__ == '__main__':
    main()
