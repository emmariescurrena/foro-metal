"""Forms for main"""

from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import Length, InputRequired
from flask_wtf import FlaskForm


class CreateTopicForm(FlaskForm):
    """Form for create topic"""

    title = StringField(
        "Título del tópico",
        validators=[InputRequired(), Length(max=256)]
    )
    text = StringField(
        "Texto",
        validators=[InputRequired(), Length(max=10000)],
        widget=TextArea()
    )
    tags = StringField(
        "Etiquetas para ayudar a otros a encontrar tu tópico. Dejar espacio entre las etiquetas",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ej.: thrash-metal guitar black-sabbath"}
    )


class CreateReplyForm(FlaskForm):
    """Form for create reply"""

    text = StringField(
        "Respuesta",
        validators=[InputRequired(), Length(max=10000)],
        widget=TextArea()
    )
