# -*- coding: utf-8 -*-
"""

"""
#from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField,  DateField, FieldList, FormField
from wtforms.validators import DataRequired, Length, ValidationError, Email


# 4.2.1 basic form example
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


# custom validator
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit1 = SubmitField('添加')
    submit2 = SubmitField('获取数据')
class FortyThreeForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField('提交')

'''
    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError('Must be 42.')
'''


# upload form
class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


class CmdForm(FlaskForm):
    title = StringField('Linux Command', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('参数')#, validators=[DataRequired()])
    publish = SubmitField('执行')

class WIFIForm(FlaskForm):
    ssid = StringField('WIFI SSID设置', validators=[DataRequired(), Length(1, 50)])
    pwd  = StringField('WIFI密码设置', validators=[DataRequired(), Length(8,128)])
    static_ip  = StringField('静态IP地址设置')
    publish = SubmitField('设置')

class LANForm(FlaskForm):
    static_ip = StringField('IP设置', validators=[DataRequired(), Length(1, 50)])
    mask  = StringField('掩码设置')
    gateway  = StringField('网关设置')
    publish = SubmitField('设置')


class ItemForm(FlaskForm):
    date_sel = DateField('日期', format='%Y-%m-%d')
    content = StringField("内容")
    delete = SubmitField("删除")
 
#自定义表单类
class AddForm(FlaskForm):
    item_list = FieldList(FormField(ItemForm),min_entries =0) #min_entries =3表示有三个同样的ItemForm
    submit = SubmitField("添加")

"""
# multiple files upload form
class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()
"""

# multiple submit button
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')


class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit1 = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField('Register')


class SigninForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField()


class RegisterForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField()

'''
# CKEditor Form
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')
'''
