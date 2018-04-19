# -*-coding: utf-8-*-

from flask import render_template, url_for, jsonify
import json
import yaml
from . import mysql
from .forms import TextForm
from .AnalyzeYaml import AnalyzeYaml
from .GetYamlFromGit import GitlabAPI
from .MysqlParse import MysqlParse
from .SqlRulesDIY import CheckDDLSql
from .Inception import Inception
from .YamlToSql import YamlToSql
from .SqlReview import SqlReview


@mysql.route('/yaml', methods=['GET', 'POST'])
def yamltosql():
    form = TextForm()
    yamltosql = AnalyzeYaml()

    if form.validate_on_submit():
        YamlText = form.body.data
        YamlDict = yaml.load(YamlText)
        #form.body.data = yamltosql.YamlToSql(YamlText)
        form.body.data = YamlDict

    return render_template('yaml.html', form=form)


@mysql.route('/test', methods=['GET', 'POST'])
def test():
    form = TextForm()
    gitlabapi = GitlabAPI()
    mysqlparse = MysqlParse()
    checkddlsql = CheckDDLSql()
    inception = Inception()
    yamltosql = YamlToSql()
    sqlreview = SqlReview()

    if form.validate_on_submit():
        #result = gitlabapi.GetFile(form.body.data)
        #result = mysqlparse.GetTableDict('test', 'oper_express_image', form.body.data)
        #result = checkddlsql.CheckSql('test', 'oper_express_image', form.body.data)
        #result = inception.InceptionReview('test', form.body.data)
        #result = mysqlparse.GetSqlInfo('test', form.body.data)
        #result = mysqlparse.SplitSql('test', form.body.data)
        #result = yamltosql.YamlToAlter('test', form.body.data)
        result = sqlreview.SqlReview('test', form.body.data, 'ddl')
        print result['data']
        print type(result['data'])

        if result['status'] == -1:
            form.body.data = result['msg']
        else:
            if result['data'][0] == '':
                form.body.data = "pass"
            else:
                #form.body.data = result['data'][0]['result']
                form.body.data = result['data']

    return render_template('yaml.html', form=form)
