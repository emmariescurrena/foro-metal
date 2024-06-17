"""Forms for main"""

from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import Length, InputRequired
from flask_wtf import FlaskForm
from .topic_custom_validators import UniqueTopicTitle, TagsQuantity, TagsValidCharacters


class CreateTopicForm(FlaskForm):
    """Form for create topic"""

    title = StringField(
        "Título del tópico",
        validators=[InputRequired(), Length(
            min=1, max=256), UniqueTopicTitle()],
        render_kw={"class": "form-control"}
    )
    text = StringField(
        "Texto",
        validators=[InputRequired(), Length(min=10, max=10000)],
        widget=TextArea(),
        render_kw={"class": "form-control"}
    )
    tags = StringField(
        "Etiquetas para ayudar a otros a encontrar tu tópico. Dejar espacio entre las etiquetas",
        validators=[InputRequired(), TagsQuantity(), TagsValidCharacters()],
        render_kw={
            "placeholder": "Ej.: thrash-metal guitar sabbath-black-sabbath", "class": "form-control"}
    )
    submit = SubmitField("Crear tópico", render_kw={"class": "btn btn-primary mt-3" })


class CreateReplyForm(FlaskForm):
    """Form for create reply"""

    text = StringField(
        "Respuesta",
        validators=[InputRequired(), Length(min=10, max=10000)],
        widget=TextArea(),
        render_kw={"class": "form-control"} 
    )
    submit = SubmitField("Responder", render_kw={"class": "btn btn-primary mt-3" } )
