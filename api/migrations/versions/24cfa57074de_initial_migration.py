"""Initial migration

Revision ID: 24cfa57074de
Revises: 
Create Date: 2022-08-11 14:55:46.006947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24cfa57074de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('creationDate', sa.DateTime(), nullable=False),
    sa.Column('productList', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_model.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_list')
    op.drop_table('user_model')
    # ### end Alembic commands ###
