import datetime
import json
import os
import fire
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

here_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.join(here_path, '..')
md_path = os.path.join(here_path, '..', 'docs', 'eng')

# SQLAlchemy class:
#
# table document:
#    id: text pk
#    title: text
#    type: text
#    file_md: text
#    file_html: text
#    lang_code: text
#    enabled: boolean default True
#    family: text
#    description: text
#    created_at: datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = 'document'
    id = Column(String, primary_key=True)
    title = Column(String)
    type = Column(String)
    file_md = Column(String)
    file_html = Column(String)
    lang_code = Column(String)
    enabled = Column(Boolean, default=True)
    family = Column(String)
    description = Column(String)
    created_at = Column(DateTime)


def _import_json(path):  # one-time use
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    engine = create_engine('sqlite:///data.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for title in data:
        o = data[title]
        id = title.lower()
        title = title.replace('_', ' ')
        family = o['family']
        description = o['description']
        file_md = o['file_md']
        file_html = o['file_html']

        file_path = os.path.join(root_path, file_md)
        created_at_epoch = os.path.getctime(file_path)
        created_at = datetime.datetime.fromtimestamp(created_at_epoch)

        document = Document(
            id=id,
            title=title,
            type='L',
            file_md=file_md,
            file_html=file_html,
            family=family,
            description=description,
            created_at=created_at
        )
        session.add(document)

    session.commit()
    session.close()


def get_all_languages():
    engine = create_engine('sqlite:///data.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    languages = session.query(Document).order_by(Document.family, Document.title).all()
    session.close()
    return languages


def dump_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///data.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    current_family = None
    for document in get_all_languages():
        if current_family != str(document.family):
            print(document.family)
            current_family = document.family
        print(f"    {document.title}")

    session.close()


if __name__ == '__main__':
    fire.Fire()
