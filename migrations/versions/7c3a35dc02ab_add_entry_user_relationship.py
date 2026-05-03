"""add entry user relationship

Revision ID: 7c3a35dc02ab
Revises: 76ac259eb0c0
Create Date: 2026-04-28 08:58:14.098271

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = '7c3a35dc02ab'
down_revision = '76ac259eb0c0'
branch_labels = None
depends_on = None

LEGACY_USER_EMAIL = 'test@test.de'

def upgrade():
    connection = op.get_bind()
    user_table = sa.table(
        'user',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String),
        sa.column('password', sa.String),
    )

    legacy_user_id = connection.execute(
        sa.select(user_table.c.id).where(user_table.c.email == LEGACY_USER_EMAIL)
    ).scalar_one_or_none()

    if legacy_user_id is None:
        connection.execute(
            user_table.insert().values(
                email=LEGACY_USER_EMAIL,
                password=generate_password_hash('legacyjournal'),
            )
        )
        legacy_user_id = connection.execute(
            sa.select(user_table.c.id).where(user_table.c.email == LEGACY_USER_EMAIL)
        ).scalar_one()

    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    connection.execute(
        sa.text('UPDATE entry SET user_id = :user_id WHERE user_id IS NULL'),
        {'user_id': legacy_user_id},
    )

    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.Integer(),
            nullable=False,
            server_default=sa.text(str(legacy_user_id)),
        )
        batch_op.create_foreign_key(
            'fk_entry_user_id_user',
            'user',
            ['user_id'],
            ['id'],
        )


def downgrade():
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.drop_constraint('fk_entry_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')
