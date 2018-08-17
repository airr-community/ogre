"""empty message

Revision ID: f5d1a02db088
Revises: 
Create Date: 2018-07-30 16:17:15.812865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5d1a02db088'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.String(length=255), nullable=True),
    sa.Column('submission_date', sa.Date(), nullable=True),
    sa.Column('submission_status', sa.String(length=255), nullable=True),
    sa.Column('submitter_name', sa.String(length=255), nullable=True),
    sa.Column('submitter_address', sa.String(length=255), nullable=True),
    sa.Column('submitter_email', sa.String(length=255), nullable=True),
    sa.Column('submitter_phone', sa.String(length=255), nullable=True),
    sa.Column('species', sa.String(length=255), nullable=True),
    sa.Column('population_ethnicity', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('Submission')
    # ### end Alembic commands ###