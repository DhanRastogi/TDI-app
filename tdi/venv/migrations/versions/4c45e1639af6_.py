"""empty message

Revision ID: 4c45e1639af6
Revises: 03d576f190f5
Create Date: 2023-04-14 14:41:53.806719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c45e1639af6'
down_revision = '03d576f190f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('housekeeping', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('flat', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('room', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_housekeeping_flat'), ['flat'], unique=False)
        batch_op.create_index(batch_op.f('ix_housekeeping_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_housekeeping_room'), ['room'], unique=False)

    with op.batch_alter_table('maintenance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('flat', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('room', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_maintenance_flat'), ['flat'], unique=False)
        batch_op.create_index(batch_op.f('ix_maintenance_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_maintenance_room'), ['room'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_maintenance_room'))
        batch_op.drop_index(batch_op.f('ix_maintenance_name'))
        batch_op.drop_index(batch_op.f('ix_maintenance_flat'))
        batch_op.drop_column('room')
        batch_op.drop_column('flat')
        batch_op.drop_column('name')

    with op.batch_alter_table('housekeeping', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_housekeeping_room'))
        batch_op.drop_index(batch_op.f('ix_housekeeping_name'))
        batch_op.drop_index(batch_op.f('ix_housekeeping_flat'))
        batch_op.drop_column('room')
        batch_op.drop_column('flat')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
