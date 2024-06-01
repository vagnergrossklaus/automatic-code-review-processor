import os
import shutil
import subprocess
from datetime import timezone

from github import Github
from github import Auth

from infra.git.dto.git_request_dto import GitRequestDTO
from infra.git.git_wrapper import GitWrapper


# TODO IMPLEMENTAR CLASSE
class GitHubWrapper(GitWrapper):

    def __init__(self, git_url, git_token):
        self.git_url = git_url
        self.git_token = git_token

        auth = Auth.Token(git_token)
        self.github_api = Github(auth=auth)

    def get_http_url_by_project_id(self, id_project):
        return self.github_api.get_repo(id_project).clone_url

    def get_id_project_source_by_id_project_target(self, id_project_target, id_merge_request):
        return self.github_api.get_repo(id_project_target).get_pull(int(id_merge_request)).base.repo.full_name

    def get_changes_by_merge(self, id_merge_request, id_project):
        changes = []
        for file in self.github_api.get_repo(id_project).get_pull(int(id_merge_request)).get_files().get_page(0):
            change = {'old_path': file.filename, 'new_path': file.filename}
            changes.append(change)
        return changes

    def get_merge_request(self, id_merge_request, id_project):
        pull_request = self.github_api.get_repo(id_project).get_pull(int(id_merge_request))
        dto = GitRequestDTO
        dto.title = pull_request.title
        dto.assignee = pull_request.assignee
        dto.source_branch = pull_request.head.ref
        dto.target_branch = pull_request.base.ref
        dto.author = {'username': pull_request.user.login}
        dto.web_url = pull_request.url
        dto.created_at = pull_request.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        return dto

    def clone_repo(self, url, branch, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)
        command = ["git", "clone", "-b", branch, url, path]
        subprocess.run(command)

    def get_threads_by_merge_request(self, id_project, id_merge_request):
        pass

    def resolve_merge_request_thread(self, id_thread, id_project, merge_request_id):
        pass

    def create_merge_request_thread(self, comment, id_project, id_merge_request, position):
        pass

    def get_versions_by_merge_request(self, id_project, id_merge_request):
        pass
