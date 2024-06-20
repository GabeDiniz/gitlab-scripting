import requests # pip install requests

'''
Description: 
Usage:

Problem: 
Solution: 
'''

gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here
projectID = "12642" # your projectID
track = "zip"

HEADERS = {'Private-Token': PRIVATE_TOKEN}
LFS_TRACKING_RULE = f'\n*.{TRACK} filter=lfs diff=lfs merge=lfs -text'

def get_branches():
    url = f'{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches'
    response = requests.get(url, headers=HEADERS)
    return response.json()

def update_gitattributes(branch):
    # Assuming .gitattributes is at the root. 
    file_path = '.gitattributes'
    url = f'{GITLAB_URL}api/v4/projects/{PROJECT_ID}/repository/files/{file_path}'
    print(f"URL: {url}")
    data = {
        'branch': branch['name'],
        'author_email': 'gdiniz@opentext.com',
        'author_name': 'Gabriel Diniz',
        'content': LFS_TRACKING_RULE,
        'commit_message': f'Track .{TRACK} files with Git LFS',
        'encoding': 'text',
    }
    # Check if .gitattributes exists and update it, otherwise create a new one
    get_response = requests.get(f"{url}?ref={branch['name']}", headers=HEADERS)
    if get_response.status_code == 200:
        # Append the rule if file exists
        # OLD AND NOT WORKING:
        # existing_content = requests.utils.unquote(get_response.json()['content'])
        # NEW:
        existing_content = DEFAULT
        print("\nGET RESPONSE CONTENT: " + str(get_response.json()['content']))
        if LFS_TRACKING_RULE not in existing_content:
            data['content'] = existing_content + LFS_TRACKING_RULE
            response = requests.put(url, headers=HEADERS, json=data)
        else:
            print(f".gitattributes in {branch['name']} already updated.")
            return
    else:
        # Create file if it does not exist
        response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Updated .gitattributes in {branch['name']}.")
    else:
        print(f"Failed to update .gitattributes in {branch['name']}: {response.content}")

def main():
    branches = get_branches()
    print(f"Branches: {branches}")
    for branch in branches:
        update_gitattributes(branch)

if __name__ == '__main__':
    main()
