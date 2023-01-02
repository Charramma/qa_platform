# 问答平台相关表单类
import wtforms
from wtforms.validators import length


# 问题表单类
class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=3)])


# 回答表单类
class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
