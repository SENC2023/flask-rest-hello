"""empty message

Revision ID: 45a13a9b2950
Revises: 7c4c19891c95
Create Date: 2024-04-24 10:26:20.760701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45a13a9b2950'
down_revision = '7c4c19891c95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('birth_year', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('eye_color', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('gender', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('hair_color', sa.String(length=250), nullable=False))
        batch_op.drop_column('model')
        batch_op.drop_column('vehicle_class')
        batch_op.drop_column('length')

    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('diameter', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('rotation_period', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('orbital_period', sa.String(length=250), nullable=False))
        batch_op.drop_column('model')
        batch_op.drop_column('vehicle_class')
        batch_op.drop_column('length')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('length', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('vehicle_class', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('model', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.drop_column('orbital_period')
        batch_op.drop_column('rotation_period')
        batch_op.drop_column('diameter')

    with op.batch_alter_table('favorite_characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('length', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('vehicle_class', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('model', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.drop_column('hair_color')
        batch_op.drop_column('gender')
        batch_op.drop_column('eye_color')
        batch_op.drop_column('birth_year')

    # ### end Alembic commands ###