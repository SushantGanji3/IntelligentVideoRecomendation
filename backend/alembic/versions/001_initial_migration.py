"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create videos table
    op.create_table(
        'videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('views', sa.Integer(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_videos_id'), 'videos', ['id'], unique=False)
    op.create_index(op.f('ix_videos_video_id'), 'videos', ['video_id'], unique=True)
    op.create_index(op.f('ix_videos_title'), 'videos', ['title'], unique=False)
    op.create_index(op.f('ix_videos_category'), 'videos', ['category'], unique=False)

    # Create watch_history table
    op.create_table(
        'watch_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.Integer(), nullable=False),
        sa.Column('watch_duration', sa.Float(), nullable=True),
        sa.Column('watch_percentage', sa.Float(), nullable=True),
        sa.Column('watched_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watch_history_id'), 'watch_history', ['id'], unique=False)
    op.create_index(op.f('ix_watch_history_user_id'), 'watch_history', ['user_id'], unique=False)
    op.create_index(op.f('ix_watch_history_video_id'), 'watch_history', ['video_id'], unique=False)
    op.create_index(op.f('ix_watch_history_watched_at'), 'watch_history', ['watched_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_watch_history_watched_at'), table_name='watch_history')
    op.drop_index(op.f('ix_watch_history_video_id'), table_name='watch_history')
    op.drop_index(op.f('ix_watch_history_user_id'), table_name='watch_history')
    op.drop_index(op.f('ix_watch_history_id'), table_name='watch_history')
    op.drop_table('watch_history')
    op.drop_index(op.f('ix_videos_category'), table_name='videos')
    op.drop_index(op.f('ix_videos_title'), table_name='videos')
    op.drop_index(op.f('ix_videos_video_id'), table_name='videos')
    op.drop_index(op.f('ix_videos_id'), table_name='videos')
    op.drop_table('videos')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

