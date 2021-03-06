"""empty message

Revision ID: e04e5dfc8be2
Revises: 1a85fff4fb23
Create Date: 2018-08-13 15:20:38.252857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e04e5dfc8be2'
down_revision = '1a85fff4fb23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genotype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sequence_id', sa.String(length=255), nullable=True),
    sa.Column('sequences', sa.Integer(), nullable=True),
    sa.Column('closest_reference', sa.String(length=255), nullable=True),
    sa.Column('closest_host', sa.String(length=255), nullable=True),
    sa.Column('nt_diff', sa.Integer(), nullable=True),
    sa.Column('nt_substitutions', sa.String(length=255), nullable=True),
    sa.Column('aa_diff', sa.Integer(), nullable=True),
    sa.Column('aa_substitutions', sa.String(length=255), nullable=True),
    sa.Column('unmutated_frequency', sa.Numeric(), nullable=True),
    sa.Column('unmutated_sequences', sa.Integer(), nullable=True),
    sa.Column('unmutated_umis', sa.Integer(), nullable=True),
    sa.Column('allelic_percentage', sa.Numeric(), nullable=True),
    sa.Column('unique_ds', sa.Integer(), nullable=True),
    sa.Column('unique_js', sa.Integer(), nullable=True),
    sa.Column('unique_cdr3s', sa.Integer(), nullable=True),
    sa.Column('haplotyping_locus', sa.String(length=255), nullable=True),
    sa.Column('haplotyping_ratio', sa.String(length=255), nullable=True),
    sa.Column('nt_sequence', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genotype')
    # ### end Alembic commands ###
