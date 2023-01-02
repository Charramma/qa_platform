# 问答平台相关视图

from flask import Blueprint, request, render_template, redirect, url_for, flash, g
from models.extension import db
from models.qa import QuestionModel, AnswerModel
from .qa_form import QuestionForm, AnswerForm
from .extension import log_required
from sqlalchemy import or_

qa_bp = Blueprint('qa_blueprint', __name__, url_prefix='/')


@qa_bp.route('/')
def index():
    """
    首页视图
    :return:
    """
    questions = QuestionModel.query.order_by(db.text('-create_time'))
    return render_template("qa/index.html", questions=questions)


@qa_bp.route('/question/public/', methods=['GET', 'POST'])
@log_required
def public_question():
    """
    发布问答视图
    :return:
    """
    if request.method == 'GET':
        return render_template("qa/public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            # 将问题存入数据库
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            flash("标题内容或格式错误")
            return redirect(url_for("qa_blueprint.public_question"))


@qa_bp.route('/detail/<int:question_id>/')
def detail(question_id):
    """
    问答详情视图
    :param question_id:
    :return:
    """
    question = QuestionModel.query.get(question_id)
    return render_template("qa/detail.html", question=question)


@qa_bp.route('/answer/<int:question_id>', methods=['POST'])
def answer(question_id):
    """
    回答视图
    :param question_id:
    :return:
    """
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data

        answer_model = AnswerModel(content=content, question_id=question_id, user=g.user)
        db.session.add(answer_model)
        db.session.commit()

        return redirect(url_for("qa_blueprint.detail", question_id=question_id))
    else:
        flash("表单验证失败")
        return redirect(url_for("qa_blueprint.detail", question_id=question_id))


@qa_bp.route('/search/')
def search():
    """
    搜索视图
    :return:
    """
    q = request.args.get("q")
    questions = QuestionModel.query.filter(
        or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))).order_by(db.text('create_time'))
    return render_template("qa/index.html", questions=questions)
