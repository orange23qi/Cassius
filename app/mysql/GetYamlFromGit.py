# -*- coding: UTF-8 -*-
from flask import current_app
import gitlab
import base64


class GitlabAPI(object):

    def __init__(self):
        self.CompanyName = current_app.config['COMPANY_NAME']
        self.GitHubUrl = current_app.config['GITHUB_URL']
        self.PrivateToken = current_app.config['PRIVATE_TOKEN']

    def GetFile(self, InputUrl):
        StrartPoint = InputUrl.find('/', InputUrl.find(self.CompanyName, 0))
        EndPoint = InputUrl.find('/', StrartPoint + 1)
        ProjectName = InputUrl[StrartPoint + 1: EndPoint]
#       获取ProjectId
        i = 1
        flag = 0
        ProjectId = 0
        gl = gitlab.Gitlab(self.GitHubUrl, self.PrivateToken)
        while i < 50:
            projects = gl.projects.list(page=i, per_page=10)
            for rows in projects:
                if rows.name == ProjectName:
                    ProjectId = rows.id
                    flag = 1
                    break
            if flag == 1:
                break
            i += 1
#       获取branch名称
        branches = gl.project_branches.list(project_id=ProjectId)
        for rows in branches:
            if InputUrl.find(rows.name, 0) != -1:
                BranchName = rows.name
                break
#       获取文件路径
        FilePath = InputUrl[InputUrl.find(BranchName, 0) + len(BranchName)+1:]
#       处理文件路径,如果最后一个是/的话,去除
        if FilePath[-1:] == "/":
            FilePath = FilePath[:-1]
#       判断FilePath是文件还是路径
        FileContent = ""
        project = gl.projects.get(ProjectId)
        items = project.repository_tree(path=FilePath, ref=BranchName)
#       如果list长度为0,则表示FilePath是文件,用files.get方法获取文件内容
        if len(items) == 0:
            f = project.files.get(file_path=FilePath, ref=BranchName)
            FileContent = base64.b64decode(f.content).decode("utf-8")
        else:
            for rows in items:
                FileFullPath = ""
                if rows["type"] == "blob":
                    FileFullPath = FilePath + "/" + rows["name"]
                    f = project.files.get(file_path=FileFullPath, ref=BranchName)
#                    FileContent += "#FileName: " + rows["name"] + '\n'
                    FileContent += base64.b64decode(f.content).decode("utf-8")
                    FileContent += '\n'

        return {"status": 1, "msg": "", "data": FileContent}
