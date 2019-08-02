
# FlaskForm class definitions for GenotypeDescription
# This file is automatically generated from the schema by schema/build_from_schema.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from custom_validators import *
from wtforms import StringField, SelectField, DateField, BooleanField, IntegerField, DecimalField, TextAreaField, HiddenField, validators, MultipleFileField
class GenotypeDescriptionForm(FlaskForm):
    genotype_name = StringField('Genotype Name', [validators.Length(max=255), NonEmpty()], description="Descriptive name for this genotype")
    genotype_subject_id = StringField('Subject ID', [validators.Length(max=255), NonEmpty()], description="Identifier of the subject from which this genotype was inferred")
    genotype_biosample_ids = StringField('Sample IDs', [validators.Length(max=255), NonEmpty()], description="Comma-separated list of accession number(s) of the sample(s) from which the genotype was derived, e.g. SAMN05924304 (NCBI), SAMEA5178755 (ENA)")
    genotype_run_ids = StringField('Sequence Sets', [validators.Length(max=255), NonEmpty()], description="Comma-separated list of accession number(s) of the sequence sets from which this genotype was derived, e.g. SRR7154792 (NCBI), ERX3006608 (NCBI)")
    gen_ncbi_hash = HiddenField('gen_ncbi_hash', [validators.Length(max=255)], description="md5 sum of details passed to ncbi")
    inference_tool_id = SelectField('Inference Tool', [validators.Optional()], choices=[])
    locus = SelectField('Locus', choices=[('IGH', 'IGH'), ('IGK', 'IGK'), ('IGL', 'IGL'), ('TRA', 'TRA'), ('TRB', 'TRB'), ('TRD', 'TRD'), ('TRG', 'TRG')], description="Gene locus")
    sequence_type = SelectField('Sequence Type', choices=[('V', 'V'), ('D', 'D'), ('J', 'J'), ('CH1', 'CH1'), ('CH2', 'CH2'), ('CH3', 'CH3'), ('CH4', 'CH4'), ('Leader', 'Leader')], description="Sequence type (V, D, J, CH1 ... CH4, Leader)")
    genotype_filename = StringField('Genotype Filename', [validators.Length(max=255)], description="Name of the uploaded file from which the genotype was read")
    genotype_file = FileField('Genotype File', description="CSV file containing genotype information")


