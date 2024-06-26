import requests # pip install requests
import sys

'''
Description: Track files with git lfs for all project branches.
Usage:
  Track files: py enable-lfs.py
  Specify project and file extension to be tracked below.

Problem: Manually tracking files with Git Large File Storage (LFS) across all 
  branches in a GitLab project that already exists can be tedious and error-prone. 
  An automated solution helps to ensure consistency and efficiency in tracking 
  specific file types with Git LFS across all project branches.
Solution: The provided Python script automates the process of tracking specific 
  file types with Git LFS across all branches of a GitLab project. It updates or 
  creates the .gitattributes file in each branch to include the specified LFS tracking rule. 
  This script ensures that the specified file types are consistently tracked with Git LFS, 
  reducing manual effort and potential errors.
'''

# Constants
author_email = "gabriel.sundiniz@gmail.com" # your GitLab author email
author_name = "Gabriel Diniz" # your GitLab author name
gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here
projectID = "12642" # your projectID
track = "zip" # file extension you want to tag as LFS

headers = {'Private-Token': private_token}
lfs_tracking_rule = f'\n*.{track} filter=lfs diff=lfs merge=lfs -text'

def get_branches():
  url = f'{gitlab_url}/api/v4/projects/{projectID}/repository/branches'
  response = requests.get(url, headers=headers)
  return response.json()

def update_gitattributes(branch):
  # Assuming .gitattributes is at the root. 
  file_path = '.gitattributes'
  url = f'{gitlab_url}api/v4/projects/{projectID}/repository/files/{file_path}'
  print(f"URL: {url}")
  data = {
    'branch': branch['name'],
    'author_email': author_email,
    'author_name': author_name,
    'content': lfs_tracking_rule,
    'commit_message': f'Track .{track} files with Git LFS',
    'encoding': 'text',
  }
  # Check if .gitattributes exists and update it, otherwise create a new one
  get_response = requests.get(f"{url}?ref={branch['name']}", headers=headers)
  if get_response.status_code == 200:
    # Append the rule if file exists
    existing_content = requests.utils.unquote(get_response.json()['content'])
    print("\nGET RESPONSE CONTENT: " + str(get_response.json()['content']))
    
    if lfs_tracking_rule not in existing_content:
      data['content'] = existing_content + lfs_tracking_rule
      response = requests.put(url, headers=headers, json=data)
    else:
      print(f"[CHECK] .gitattributes in {branch['name']} already updated.")
      return
  else:
    # Create file if it does not exist
    response = requests.post(url, headers=headers, json=data)
  
  if response.status_code in [200, 201]:
    print(f"[SUCCESS] Updated .gitattributes in {branch['name']}.")
  else:
    print(f"[ERROR] Failed to update .gitattributes in {branch['name']}: {response.content}")

def main():
  branches = get_branches()
  print(f"Branches: {branches}")
  for branch in branches:
    update_gitattributes(branch)

if __name__ == '__main__':
  if private_token == '':
    print("[ERROR] Please set your GitLab private token in the # Constants section of this python file.")
    sys.exit()
  main()
