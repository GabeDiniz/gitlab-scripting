import requests # pip install requests
import sys
import json

gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here

projects = ["12642", "12641"]

def add_users(users):
  for username in users:
    # Get the user ID from the username
    user_response = requests.get(
      f'{gitlab_url}/api/v4/users?username={username}',
      headers={'PRIVATE-TOKEN': private_token}
    )
    user_id = user_response.json()[0]['id'] if user_response.ok else None

    if user_id:
      # Invite the user to the project
      invite_certdev_response = requests.post(
        f'{gitlab_url}/api/v4/projects/{projects[0]}/members',
        headers={'PRIVATE-TOKEN': private_token},
        json={'user_id': user_id, 'access_level': 20}  # Access level 20 corresponds to Reporter role - level 50 = Owner
      )

      invite_production_response = requests.post(
        f'{gitlab_url}/api/v4/projects/{projects[1]}/members',
        headers={'PRIVATE-TOKEN': private_token},
        json={'user_id': user_id, 'access_level': 20}
      )

      response = json.loads(invite_certdev_response.text)
      response2 = json.loads(invite_production_response.text)

      if invite_certdev_response.ok and invite_production_response.ok:
        print(f'[Success] Invited {username} to Production and cert.dev as a Reporter')
      elif response.get("message") == "Member already exists" and response2.get("message") == "Member already exists":
        print(f"[Success] The user {username} already has access to the projects...")
      else:
        print(f'[FAILED] Unable to invite {username}, please try to invite the user manually. \nProduction Error: {invite_production_response.text}\nCert.dev Error: {invite_certdev_response.text}')
    else:
      print(f'User {username} not found.')


if __name__ == "__main__":
  # Check if a project name and/or languages is provided as an argument
  if private_token == "":
    print("[Error] Please add your GitLab private token to line 6 of this python file.")
    sys.exit()
  if not (len(sys.argv) == 2):
    print("Description: Adds listed users as Reporters to the cert.dev and Production repositories.")
    print("Usage: python add-gitlab-users.py <user-id>,<user-id-2>,<user-id-n>")
    sys.exit(1)

  # Split input users by comma
  users = (sys.argv[1]).split(",")
  print(f"Granting access to: {users}")

  add_users(users)
