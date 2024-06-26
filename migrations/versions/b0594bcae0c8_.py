"""empty message

Revision ID: b0594bcae0c8
Revises: 05eb56b87977
Create Date: 2024-04-24 10:52:18.387725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0594bcae0c8'
down_revision = '05eb56b87977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('vehicles', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user'], ['id'])
        batch_op.create_foreign_key(None, 'vehicles', ['vehicles'], ['id'])
        batch_op.drop_column('name')
        batch_op.drop_column('length')
        batch_op.drop_column('model')
        batch_op.drop_column('vehicle_class')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_class', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('model', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('length', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('vehicles')
        batch_op.drop_column('user')

    # ### end Alembic commands ###
