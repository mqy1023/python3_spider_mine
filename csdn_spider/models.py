from peewee import *

db = MySQLDatabase("csdn_spider", host="127.0.0.1", port=3333, user="root", password="root")

class BaseModel(Model):
    class Meta:
        database = db

#设计数据表的时候有几个重要点一定要注意
"""
char类型， 要设置最大长度
对于无法确定最大长度的字段，可以设置为Text
设计表的时候 采集到的数据要尽量先做格式化处理
default和null=True
"""


class Topic(BaseModel):
    title = CharField()
    content = TextField(default="")
    id = IntegerField(primary_key=True)
    author = CharField()
    create_time = DateTimeField()
    answer_nums = IntegerField(default=0)
    click_nums = IntegerField(default=0)
    praised_nums = IntegerField(default=0)
    jtl = FloatField(default=0.0)  # 结帖率
    score = IntegerField(default=0)  # 赏分
    status = CharField()  # 状态
    last_answer_time = DateTimeField()


class Answer(BaseModel):
    topic_id = IntegerField()
    author = CharField()
    content = TextField(default="")
    create_time = DateTimeField()
    parised_nums = IntegerField(default=0) #点赞数

if __name__ == "__main__":
    db.create_tables([Topic, Answer])
