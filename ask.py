from app import create_app
from app.models import db, User, Question

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db , 'User':User , 'Question':Question}
