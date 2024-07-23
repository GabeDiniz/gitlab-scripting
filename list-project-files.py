import gitlab # pip install python-gitlab
import sys

'''
Description: Recursively list the files under a project directory
Usage:
  Search files: py list-project-files.py <project-id> <branch> <repo-directory>
    Example: py list-project-files.py 12345 master src/unit-tests
    >>> Result: lists all the files within unit-tests and nested folders

Problem: 
Solution: 
'''

# Constants
gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here

# Initialize GitLab connection
gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

# Recurse through files and folders
def list_files_recursive(project_id, branch, directory, base_path=""):
  try:
    project = gl.projects.get(project_id)
    items = project.repository_tree(path=directory, ref=branch, all=True)

    for item in items:
      item_path = f"{base_path}/{item['path']}" if base_path else item['path']
      # If the item is a FILE: print it
      if item['type'] == 'blob':
        print(item_path)
      # If the item is a FOLDER: recurse through it
      elif item['type'] == 'tree':
        list_files_recursive(project_id, branch, item['path'], base_path)
  # Catch error
  except gitlab.exceptions.GitlabGetError as e:
    print(f"Failed to get files from project ID '{project_id}': {e}")

def main():
  if len(sys.argv) != 4:
    print("Usage: python list_project_files.py <project_id> <branch> <directory>")
    sys.exit(1)

  project_id = sys.argv[1]
  branch = sys.argv[2]
  directory = sys.argv[3]

  list_files_recursive(project_id, branch, directory)

if __name__ == "__main__":
  main()