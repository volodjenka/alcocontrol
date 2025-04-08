"""initial

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создание таблицы users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('telegram_id', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('telegram_id'),
        sa.UniqueConstraint('username')
    )
    
    # Создание индексов для users
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_telegram_id', 'users', ['telegram_id'])
    
    # Создание таблицы drinks
    op.create_table(
        'drinks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('volume', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('alcohol_content', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создание индексов для drinks
    op.create_index('idx_drinks_user_id', 'drinks', ['user_id'])
    op.create_index('idx_drinks_created_at', 'drinks', ['created_at'])
    op.create_index('idx_drinks_user_date', 'drinks', ['user_id', 'created_at'])
    
    # Создание таблицы drink_types
    op.create_table(
        'drink_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Создание таблицы user_settings
    op.create_table(
        'user_settings',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('daily_limit', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('notification_enabled', sa.Boolean(), server_default=sa.text('true')),
        sa.Column('notification_time', sa.Time(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id')
    )
    
    # Добавление проверок для drinks
    op.create_check_constraint(
        'check_volume_positive',
        'drinks',
        sa.text('volume > 0')
    )
    op.create_check_constraint(
        'check_alcohol_content',
        'drinks',
        sa.text('alcohol_content >= 0 AND alcohol_content <= 100')
    )

def downgrade():
    # Удаление таблиц в обратном порядке
    op.drop_table('user_settings')
    op.drop_table('drink_types')
    op.drop_table('drinks')
    op.drop_table('users') 