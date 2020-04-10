http://118.178.56.54:7474/browser/
usernm: neo4j
passwd: By5liml123

node4j图数据库
   id： uuid
   name: 字符串，标签
   attributes： {属性}
   AtlasRelation：联系标签


暂时约定的格式：
    节点：AtlasNode
        uuid
        name
        attributes
    联系：AtlasRelation
        uuid
        name
        attributes

节点实例：

uuid:"1"
name :”硝酸胺“
attributes：{"发展历史":"公元。。。","应急处置":"....","理化性质":"","用途":""}