
# FlaskForm class definitions for InferredSequence
# This file is automatically generated from the schema by schema/build_from_schema.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from custom_validators import *
from wtforms import StringField, SelectField, DateField, BooleanField, IntegerField, DecimalField, TextAreaField, validators
class InferredSequenceForm(FlaskForm):
    sequence_id = SelectField('sequence_id', [validators.Optional()], choices=[], description="Identifier of the sequence within the genotype")
    genotype_id = SelectField('genotype_id', [validators.Optional()], choices=[], description="Identifier of the genotype from which these sequences were inferred")
    inferred_extension = BooleanField('Extension?', [], description="Checked if the inference reports an extension to a known sequence")
    ext_3prime = TextAreaField('3\'  Extension', [ValidNucleotideSequence(ambiguous=False, gapped=True), validators.Optional()], description="Extending sequence at 3\' end (IMGT gapped)")
    start_3prime_ext = IntegerField('3\' start', [validators.Optional()], description="Start co-ordinate of 3\' extension (if any) in IMGT numbering")
    end_3prime_ext = IntegerField('3\' end', [validators.Optional()], description="End co-ordinate of 3\' extension (if any) in IMGT numbering")
    ext_5prime = TextAreaField('5\' Extension', [ValidNucleotideSequence(ambiguous=False, gapped=True), validators.Optional()], description="Extending sequence at 5\' end (IMGT gapped)")
    start_5prime_ext = IntegerField('5\' start', [validators.Optional()], description="Start co-ordinate of 5\' extension (if any) in IMGT numbering")
    end_5prime_ext = IntegerField('5\' end', [validators.Optional()], description="End co-ordinate of 5\' extension (if any) in IMGT numbering")
    seq_accession_no = StringField('Accession Number', [validators.Length(max=255), NonEmpty()], description="Accession number of the inferred allele within the repository")
    deposited_version = StringField('Version', [validators.Length(max=255)], description="Version number of the sequence within the repository")
    run_ids = StringField('Run Accession Numbers', [validators.Length(max=255), NonEmpty()], description="Comma-separated list of accession number(s) of the run(s) listing the raw sequences from which this inference was made")


