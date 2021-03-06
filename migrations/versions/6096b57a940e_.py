"""empty message

Revision ID: 6096b57a940e
Revises: 4cfbadc065e7
Create Date: 2018-08-31 15:52:26.172643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6096b57a940e'
down_revision = '4cfbadc065e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inferred_sequence', sa.Column('seq_accession_no', sa.String(length=255), nullable=True))
    op.drop_column('inferred_sequence', 'repository_id')
    op.add_column('repertoire', sa.Column('rep_accession_no', sa.String(length=255), nullable=True))
    op.drop_column('repertoire', 'repository_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repertoire', sa.Column('repository_id', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('repertoire', 'rep_accession_no')
    op.add_column('inferred_sequence', sa.Column('repository_id', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('inferred_sequence', 'seq_accession_no')
    # ### end Alembic commands ###
