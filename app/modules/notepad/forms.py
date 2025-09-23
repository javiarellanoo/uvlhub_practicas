from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField


class NotepadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=256)])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save notepad')
