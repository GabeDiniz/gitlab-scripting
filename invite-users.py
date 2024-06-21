import requests # pip install requests
import sys
import json

'''
Description: Invite multiple users to multiple projects with this script.
Usage:
  Invite user(s): py invite-users.py <username-1>,<username-2>,<username-n>
  Projects are specified in the constants below.

Problem: 
Solution: 
'''

# Constants
gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here
projects = ["12642", "12641"] # your projectID(s)

def add_users(users):
  for username in users:
    # Get the user ID from the username
    user_response = requests.get(
      f'{gitlab_url}/api/v4/users?username={username}',
      headers={'PRIVATE-TOKEN': private_token}
    )
    user_id = user_response.json()[0]['id'] if user_response.ok else None

    if user_id:
      for project in projects:
        # Invite the user to the project
        invite_response = requests.post(
          f'{gitlab_url}/api/v4/projects/{project}/members',
          headers={'PRIVATE-TOKEN': private_token},
          json={'user_id': user_id, 'access_level': 30}  # level 20 = Reporter | level 30 = Developer | level 40 = Maintainer | level 50 = Owner
        )

        response = json.loads(invite_response.text)

        if invite_response.ok:
          print(f'[SUCCESS] Invited {username} to the project')
        elif response.get("message") == "Member already exists":
          print(f"[SUCCESS KIND OF?] The user {username} already has access to the projects...")
        else:
          print(f'[FAILED] Unable to invite {username}, please try to invite the user manually.\nIt is possible the user does not have a GitLab account\n[ERROR]: {invite_response.text}')

    else:
      print(f'User {username} not found.')


if __name__ == "__main__":
  # Check if a project name and/or languages is provided as an argument
  if private_token == "":
    print("[ERROR] Please set your GitLab private token in the # Constants section of this python file.")
    sys.exit()
  if not (len(sys.argv) == 2):
    print("Description: Adds listed users to listed projects")
    print("Usage: python add-gitlab-users.py <user-id>,<user-id-2>,<user-id-n>")
    sys.exit(1)

  # Split input users by comma
  users = (sys.argv[1]).split(",")
  print(f"Granting access to: {users}")

  add_users(users)
