"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-12-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'], unique=False)
    
    op.create_table('maternal_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('systolic_bp', sa.Integer(), nullable=False),
    sa.Column('diastolic_bp', sa.Integer(), nullable=False),
    sa.Column('bs', sa.Float(), nullable=False),
    sa.Column('body_temp', sa.Float(), nullable=False),
    sa.Column('heart_rate', sa.Integer(), nullable=False),
    sa.Column('risk_level', sa.String(), nullable=False),
    sa.Column('model_used', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maternal_records_id'), 'maternal_records', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_maternal_records_id'), table_name='maternal_records')
    op.drop_table('maternal_records')
    op.drop_index(op.f('ix_patients_id'), table_name='patients')
    op.drop_table('patients')
