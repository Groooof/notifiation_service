"""empty message

Revision ID: fd5696b02766
Revises: 
Create Date: 2022-08-26 22:06:07.297158

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fd5696b02766'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    CompositeFilter = sqlalchemy_utils.CompositeType('mailing_filter', [
        sa.Column('tags', sa.ARRAY(sa.String)),
        sa.Column('codes', sa.ARRAY(sa.String))
    ])

    CompositeFilter.create(op.get_bind())

    op.create_table('clients',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('tag', sa.String(length=255), nullable=False),
    sa.Column('tz', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mailings',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=False),
    sa.Column('date_stop', sa.DateTime(), nullable=False),
    sa.Column('text', sa.String(length=1024), nullable=False),
    sa.Column('filter', CompositeFilter),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('success', 'in_process', 'failed', name='status'), nullable=False),
    sa.Column('mailing_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('mailings')
    op.drop_table('clients')
    # ### end Alembic commands ###
