from models.user_model import User
import argparse


parser = argparse.ArgumentParser(description='create new user account')
parser.add_argument('-u', '--username', metavar='username',
                    required=True, help='username')
parser.add_argument('-e', '--email', metavar='email',
                    required=True, help='user email')
parser.add_argument('-p', '--password', metavar='password',
                    required=True, help='user password')
parser.add_argument('-su', '--superuser', metavar='superuser',
                    required=True, help='is user admin')

user = parser.parse_args()


def main():
    new_user = User.create(user.username, user.email,
                           user.password, bool(user.superuser))
    print('user {} created'.format(new_user))


if __name__ == "__main__":
    main()
