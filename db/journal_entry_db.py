
# ORM definitions for JournalEntry
# This file is automatically generated from the schema by schema/build_from_schema.py

from app import db
from db.userdb import User
from db.styled_table import *
from flask_table import Table, Col, LinkCol, create_table
from db.view_table import ViewCol
from sqlalchemy.orm import backref

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    author = db.Column(db.String(255))
    type = db.Column(db.String(255))
    title = db.Column(db.String(1000))
    body = db.Column(db.Text())
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    submission = db.relationship('Submission', backref = 'journal_entries')
    gene_description_id = db.Column(db.Integer, db.ForeignKey('gene_description.id'))
    gene_description = db.relationship('GeneDescription', backref = 'journal_entries')
    parent_id = db.Column(db.Integer, db.ForeignKey('journal_entry.id'))
    children = db.relationship('JournalEntry', backref = backref('parent', remote_side = [id]))


def save_JournalEntry(db, object, form, new=False):   
    object.title = form.title.data
    object.body = form.body.data

    if new:
        db.session.add(object)
        
    db.session.commit()   



def populate_JournalEntry(db, object, form):   
    form.title.data = object.title
    form.body.data = object.body




def copy_JournalEntry(c_from, c_to):   
    c_to.date = c_from.date
    c_to.author = c_from.author
    c_to.type = c_from.type
    c_to.title = c_from.title
    c_to.body = c_from.body



class JournalEntry_table(StyledTable):
    id = Col("id", show=False)
    date = StyledCol("date", tooltip="Date submission received")
    author = StyledCol("author", tooltip="email address of author")
    title = StyledCol("Note title", tooltip="title of entry")


def make_JournalEntry_table(results, private = False, classes=()):
    t = create_table(base=JournalEntry_table)
    ret = t(results, classes=classes)
    return ret

class JournalEntry_view(Table):
    item = ViewCol("", column_html_attrs={"class": "col-sm-3 text-right font-weight-bold view-table-row"})
    value = Col("")


def make_JournalEntry_view(sub, private = False):
    ret = JournalEntry_view([])
    ret.items.append({"item": "Note title", "value": sub.title, "tooltip": "title of entry", "field": "title"})
    ret.items.append({"item": "Note", "value": sub.body, "tooltip": "body text of entry", "field": "body"})
    return ret

