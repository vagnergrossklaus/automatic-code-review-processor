import argparse
import os

from app.processor import workspace, review, publish
from infra.git.gitenum import GitEnum

exit_code_error = -1
exit_code_success = 0


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument("--GIT_TYPE", help="Informe ase é GIT_HUB ou GIT_LAB")
    parser.add_argument("--GIT_URL", help="Informe a URL do GIT")
    parser.add_argument("--GIT_USER", help="Informe o usuário")
    parser.add_argument("--GIT_TOKEN", help="Informe o token")
    parser.add_argument("--GIT_PROJECT_ID", help="Informe o id do projeto")
    parser.add_argument("--GIT_MERGE_REQUEST_ID", help="Informe o id do merge request")
    parser.add_argument("--STAGE", help="Informe o stage da execucao", default="default")

    args = parser.parse_args()
    git_enum = GitEnum[args.GIT_TYPE]

    path_resources = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../resources")

    path_target, path_source, merge = workspace.setup(
        git_url=args.GIT_URL,
        git_user=args.GIT_USER,
        git_token=args.GIT_TOKEN,
        id_project_target=args.GIT_PROJECT_ID,
        id_merge_request=args.GIT_MERGE_REQUEST_ID,
        git_enum=git_enum,
        path_resources=path_resources,
    )

    comments = review.review(
        path_target=path_target,
        path_source=path_source,
        path_resources=path_resources,
        merge=merge,
        stage=args.STAGE,
    )

    qt_pending_comment = publish.publish(
        comments=comments,
        id_project=args.GIT_PROJECT_ID,
        id_merge_request=args.GIT_MERGE_REQUEST_ID,
        git_enum=git_enum,
        git_url=args.GIT_URL,
        git_token=args.GIT_TOKEN,
        git_user=args.GIT_USER,
    )

    if qt_pending_comment > 0:
        exit_code = exit_code_error
    else:
        exit_code = exit_code_success

    return exit_code
