"""empty message

Revision ID: 19f35d1c90f7
Revises: 
Create Date: 2022-01-27 19:46:35.481164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f35d1c90f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('whoLikes',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.memberId'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.postId'], ),
    sa.PrimaryKeyConstraint('member_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whoLikes')
    # ### end Alembic commands ###