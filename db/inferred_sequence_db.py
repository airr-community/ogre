
# ORM definitions for InferredSequence
from app import db
from db.userdb import User
from db.styled_table import *
from flask_table import Table, Col, LinkCol

class InferredSequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('genotype.id'))
    sequence_details = db.relationship('Genotype', backref = 'inferred_sequences')
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    submission = db.relationship('Submission', backref = 'inferred_sequences')
    genotype_id = db.Column(db.Integer, db.ForeignKey('genotype_description.id'))
    genotype_description = db.relationship('GenotypeDescription', backref = 'inferred_sequences')
    repository_id = db.Column(db.String(255))
    deposited_version = db.Column(db.String(255))
    run_ids = db.Column(db.String(255))


def save_InferredSequence(db, object, form, new=False):   
    object.sequence_id = form.sequence_id.data
    object.genotype_id = form.genotype_id.data
    object.repository_id = form.repository_id.data
    object.deposited_version = form.deposited_version.data
    object.run_ids = form.run_ids.data

    if new:
        db.session.add(object)
        
    db.session.commit()   



def populate_InferredSequence(db, object, form):   
    form.repository_id.data = object.repository_id
    form.deposited_version.data = object.deposited_version
    form.run_ids.data = object.run_ids



class InferredSequence_table(StyledTable):
    id = Col("id", show=False)


def make_InferredSequence_table(results, private = False, classes=()):
    ret = InferredSequence_table(results, classes=classes)
    return ret

class InferredSequence_view(Table):
    item = Col("", column_html_attrs={"class": "col-sm-3 text-right font-weight-bold view-table-row"})
    value = Col("")


def make_InferredSequence_view(sub, private = False):
    ret = InferredSequence_view([])
    ret.items.append({"item": "sequence_id", "value": sub.sequence_id})
    ret.items.append({"item": "genotype_id", "value": sub.genotype_id})
    ret.items.append({"item": "repository_id", "value": sub.repository_id})
    ret.items.append({"item": "deposited_version", "value": sub.deposited_version})
    ret.items.append({"item": "run_ids", "value": sub.run_ids})
    return ret

