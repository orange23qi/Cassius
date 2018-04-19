# -*-coding: utf-8-*-
# yamlfile example:
# http://gitlab.1dmy.com/ezbuy/garencieres/blob/master/service/internal/redis-orm/tag.yaml

import yaml


class AnalyzeYaml(object):
    def YamlToCreate(self, YamlText):
        '''
        把yaml文本转换成建表语句
        '''
        status = 1
        msg = ''
        data = []

        YamlDict = yaml.load(YamlText)
##      需要增加解析失败报错

        for TableNameCamel in YamlDict:
            TmpSql = 'CREATE TABLE '
            TableName = YamlDict[TableNameCamel]['dbtable']
##      需要增加yaml缺失key的报错
            IndexCol = ''

#           拼接建表语句
            TmpSql += TableName + ' ( '
            PrimaryCol = '\n\tPRIMARY KEY ('
            TableInfo = '\n) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;\n\n'
            IsNoInc = 0

            for ColumnInfo in YamlDict[TableNameCamel]['fields']:
                ColumnName = ''
                ColumType = ''
                ColCommnet = ''
                ColumFlag = ''
                ColSql = ''
                IsPri = 0
                IsIdx = 0
                IsUniq = 0
                IsNullAble = 0
                IsComment = 0

                for ColumnTag in ColumnInfo:
                    if ColumnTag.lower() not in ['flags', 'comment', 'sqltype']:
                        ColumnName = self.CamelToUnderline(ColumnTag)
                        ColumTypeOrg = ColumnInfo[ColumnTag]
                        ColumType = self.TypeMapping(ColumTypeOrg)

                    elif ColumnTag == 'flags':
                        for KeyWord in ColumnInfo[ColumnTag]:
                            if KeyWord.lower() == 'primary':
                                IsPri = 1
                            elif KeyWord.lower() == 'index':
                                IsIdx = 1
                            elif KeyWord.lower() == 'unique':
                                IsUniq = 1
                            elif KeyWord.lower() == 'noinc':
                                IsNoInc = 1
                            elif KeyWord.lower() == 'nullable':
                                IsNullAble = 1

                    elif ColumnTag == 'comment':
                        IsComment = 1
                        ColCommnet = ColumnInfo[ColumnTag]
                        ColCommnet = " COMMENT '" + ColCommnet + "',"

                    elif ColumnTag == 'sqltype':
                        ColumTypeOrg = ColumnInfo[ColumnTag]
                        ColumType = self.TypeMapping(ColumTypeOrg)

#               处理字段定义
                ColSql = ColumnName + ' ' + ColumType

                if ColumTypeOrg == 'string':
                    ColumFlag = " NOT NULL DEFAULT ''"
                else:
                    ColumFlag = " NOT NULL DEFAULT 0"

                if IsComment == 0:
                    ColCommnet = ","

#               处理特殊属性
                if IsPri == 1:
                    PrimaryCol += ColumnName + ')'
                    if ColumTypeOrg != 'string':
                        ColumFlag += ' AUTO_INCREMENT'
                    else:
                        TableInfo = TableInfo.replace(' AUTO_INCREMENT=1', '')
                if IsIdx == 1:
                    IndexCol += ',\n\tKEY idx_' + ColumnName + ' (' + ColumnName + ')'
                if IsUniq == 1:
                    IndexCol += ',\n\tUNIQUE KEY uniq_' + ColumnName + ' (' + ColumnName + ')'
                if IsNoInc == 1:
                    ColumFlag = ColumFlag.replace(' AUTO_INCREMENT', '')
                    TableInfo = TableInfo.replace(' AUTO_INCREMENT=1', '')
                if IsNullAble == 1:
                    ColumFlag = ColumFlag.replace(' NOT NULL', '')

                TmpSql += '\n\t' + ColSql + ColumFlag + ColCommnet

#           处理组合主键
            if YamlDict[TableNameCamel].get('primary') is not None:

                PrimaryCol = '\n\tPRIMARY KEY ('
                for ColNameCaml in YamlDict[TableNameCamel]['primary']:
                    PrimaryCol += self.CamelToUnderline(ColNameCaml) + ', '
                PrimaryCol += ')'
                PrimaryCol = PrimaryCol.replace(', )', ')')

#           处理组合唯一索引
            if YamlDict[TableNameCamel].get('uniques') is not None:
                for ColNameCamlList in YamlDict[TableNameCamel]['uniques']:
                    UniqCol = ''
                    UniqName = 'uniq_'

                    for ColNameCaml in ColNameCamlList:
                        UniqName += self.CamelToUnderline(ColNameCaml).split('_')[0] + '_'
                        UniqCol += self.CamelToUnderline(ColNameCaml) + ', '

                    UniqCol = ',\n\tUNIQUE KEY ' + UniqName + ' (' + UniqCol + ')'
                    IndexCol += UniqCol
                IndexCol = IndexCol.replace(', )', ')').replace('_ ', ' ')

#           处理组合索引
            if YamlDict[TableNameCamel].get('indexes') is not None:
                for v_columnInfo in YamlDict[TableNameCamel]['indexes']:
                    MulIndexCol = ''
                    MulIndexName = 'idx_'

                    for ColNameCaml in ColNameCamlList:
                        MulIndexName += self.CamelToUnderline(ColNameCaml).split('_')[0] + '_'
                        MulIndexCol += self.CamelToUnderline(ColNameCaml) + ', '

                    MulIndexCol = '\n\tKEY' + MulIndexName + ' (' + MulIndexCol + ')'
                    IndexCol += MulIndexCol
                IndexCol = IndexCol.replace(', )', ')').replace('_ ', ' ')

#           最后整理语句
            TmpSql += PrimaryCol + IndexCol + TableInfo
            data.append({'name': TableName, 'sql': TmpSql})

        return {'status': status, 'msg': msg, 'data': data}

    def CamelToUnderline(self, CamelFormat):
        '''
        驼峰命名格式转下划线命名格式
        '''
        UnderLineFormat = ''
        CamelFormat = CamelFormat.encode("utf-8")

        if isinstance(CamelFormat, str):
            for Alphabet in CamelFormat:
                UnderLineFormat += Alphabet \
                        if Alphabet.islower() else '_'+Alphabet.lower()
        return UnderLineFormat[1:]

    def UnderLineToCamel(self, UnderLineFormat):
        '''
        下划线命名格式驼峰命名格式
        '''
        CamelFormat = ''
        CamelFormat = CamelFormat.encode("utf-8")

        if isinstance(UnderLineFormat, str):
            for Alphabet in UnderLineFormat.split('_'):
                CamelFormat += Alphabet.capitalize()
        return CamelFormat

    def TypeMapping(self, ColumType):
        '''
        yaml文件中的类型与MySQL中的类型互相转换( 后续这段放到数据库配置表中 )
        '''
        ColumTypeInput = ColumType.lower()

        if ColumTypeInput == 'int64':
            return 'BIGINT(20)'
        elif ColumTypeInput == 'timeint':
            return 'BIGINT(20)'
        elif ColumTypeInput == 'int32':
            return 'INT(11)'
        elif ColumTypeInput == 'bool':
            return 'TINYINT(4)'
        elif ColumTypeInput == 'string':
            return 'VARCHAR(100)'
        elif ColumTypeInput == 'float64':
            return 'FLOAT(10,3)'
        else:
            return ColumType
