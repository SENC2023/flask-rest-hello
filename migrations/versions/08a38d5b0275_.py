"""empty message

Revision ID: 08a38d5b0275
Revises: 8f355eb0a261
Create Date: 2024-04-24 10:12:59.371895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08a38d5b0275'
down_revision = '8f355eb0a261'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('vehicle_class', sa.String(length=250), nullable=False),
    sa.Column('length', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('vehicle_class', sa.String(length=250), nullable=False),
    sa.Column('length', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favorite_vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('vehicle_class', sa.String(length=250), nullable=False),
    sa.Column('length', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_vehicles')
    op.drop_table('favorite_user')
    op.drop_table('favorite_planets')
    op.drop_table('favorite_characters')
    # ### end Alembic commands ###
