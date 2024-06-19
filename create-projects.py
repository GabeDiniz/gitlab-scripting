import gitlab # pip install python-gitlab
import sys

'''
Description: create a single or multiple projects, and edit rules with this script.
Usage:
  Create Single Project: py create-project.py "Project Name"
  Create Multiple Projects: py create-project.py "project-prefix" suffix-1,suffix-2,suffix-n
    Example: py create-project.py rocket english,french,spanish 
    >>> Result: rocket.english | rocket.french | rocket.spanish

Problem: Creating and managing multiple projects in GitLab manually can be time-consuming and 
  prone to errors. There is a need for an automated solution to create single or multiple projects, 
  and to configure their push rules effectively.
  
Solution: The provided Python script automates the creation of single or multiple GitLab projects 
  and updates their push rules simultaneously. By using the GitLab API, it facilitates the creation of projects 
  under a specified namespace and handles the configuration of push rules to ensure consistency 
  and reduce manual effort. The script can be executed with specific parameters to create a single
  project or multiple projects with a common prefix and different suffixes.
'''

gitlab_url = "https://gitlab.instance.net"
private_token = "your-private-token" # insert private token here
namespace_id = 1111 # GitLab group ID - the group the projects are going under

def create_project(project_name, languages):
  # Create a GitLab API client
  gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

  if languages:
    ######################################
    ### Create Language Project ##########
    ######################################
    print(">>> Creating Language Projects")

    # Parse Variables
    lo_languages = languages.split(",")

    for language in lo_languages:
      current_project = project_name + "." + language
      print(f'-----------------------------------\nCreating project: "{current_project}"')
      try:
        # Create a new language project
        project = gl.projects.create({'name': current_project, 'namespace_id': namespace_id})
        print(f'Project "{current_project}" created successfully! URL: {project.web_url}')

        # Disable push rules
        try:
          push_rules = project.pushrules.get()
        except gitlab.exceptions.GitlabGetError:
          push_rules = None

        if push_rules:
          push_rules.commit_committer_check = False
          push_rules.member_check = False
          push_rules.save()
          print(f'Push rules for "{current_project}" has been updated!')
          
      except gitlab.exceptions.GitlabCreateError as e:
        print(f'Error creating project: {e.response_body}')
      except gitlab.exceptions.GitlabUpdateError as e:
        print(f'Error updating push rules: {e.response_body}')
  
  else:
    ######################################
    ### Create Single Project ############
    ######################################
    print(">>> Creating Single Project")

    try:
      # Create a new project
      project = gl.projects.create({'name': project_name, 'namespace_id': namespace_id})
      print(f'Project "{project_name}" created successfully! URL: {project.web_url}')

      # Update rules
      try:
        push_rules = project.pushrules.get()
      except gitlab.exceptions.GitlabGetError:
        push_rules = None

      if push_rules:
        push_rules.commit_committer_check = True
        push_rules.member_check = True
        push_rules.save()
        print(f'Push rules for "{project_name}" has been updated!')
          
    except gitlab.exceptions.GitlabCreateError as e:
      print(f'Error creating project: {e.response_body}')
      quit()
    except gitlab.exceptions.GitlabUpdateError as e:
      print(f'Error updating push rules: {e.response_body}')
      quit()
  
  print("****************************************\nAll projects created successfully\n****************************************")



if __name__ == "__main__":
  # Check if private token has been set
  if private_token == '':
    print("INVALID Token: please set your private token on line 5 of this python file.")
  # Check if a project name and/or languages is provided as an argument
  if not (1 < len(sys.argv) < 4):
    print("Usage: python GitLab-AddProjects.py <project_name> <language>,<language-2>,<language-n>")
    sys.exit(1)

  project_name = sys.argv[1]
  if len(sys.argv) > 2:
    languages = sys.argv[2]
  else:
    languages = False

  create_project(project_name, languages)
