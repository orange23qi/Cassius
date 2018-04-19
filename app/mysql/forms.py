# -*-coding: utf-8-*-
from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import TextAreaField, SubmitField


class TextForm(FlaskForm):
    body = TextAreaField(u'文本框', validators=[Required(u'请输入sql')],
                         render_kw={'class': 'text-body',
                                    'rows': 20,
                                    'placeholder': u'请输入sql'})
    #body = TextAreaField(u'文本框')
    submit = SubmitField(u'转化')
