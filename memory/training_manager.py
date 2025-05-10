from sqlalchemy.orm import Session
from db.models import TrainingData, ModelVersion, init_db
from datetime import datetime
import json
from typing import List, Dict, Any
import numpy as np
from sklearn.model_selection import train_test_split

class TrainingManager:
    def __init__(self):
        self.engine = init_db()
        
    def save_feedback(self, user_input: str, response: str, feedback_score: float, 
                     feedback_comment: str = None, is_helpful: bool = True) -> None:
        """Save user feedback for a response"""
        session = Session(self.engine)
        try:
            entry = TrainingData(
                user_input=user_input,
                response=response,
                feedback_score=feedback_score,
                feedback_comment=feedback_comment,
                is_helpful=is_helpful
            )
            session.add(entry)
            session.commit()
        finally:
            session.close()
            
    def get_training_data(self, min_feedback_score: float = 4.0, 
                         limit: int = 1000) -> List[Dict[str, Any]]:
        """Get high-quality training examples"""
        session = Session(self.engine)
        try:
            data = session.query(TrainingData)\
                .filter(TrainingData.feedback_score >= min_feedback_score)\
                .filter(TrainingData.used_for_training == False)\
                .limit(limit)\
                .all()
            return [{
                'input': d.user_input,
                'response': d.response,
                'feedback_score': d.feedback_score
            } for d in data]
        finally:
            session.close()
            
    def prepare_training_data(self, data: List[Dict[str, Any]], 
                            test_size: float = 0.2) -> Dict[str, Any]:
        """Prepare data for training by splitting into train/test sets"""
        # Split data into training and validation sets
        train_data, val_data = train_test_split(
            data, test_size=test_size, random_state=42
        )
        
        return {
            'train': train_data,
            'validation': val_data
        }
        
    def update_model_version(self, version: str, training_data_count: int, 
                           performance_metrics: Dict[str, float]) -> None:
        """Update model version information after training"""
        session = Session(self.engine)
        try:
            # Deactivate current active model
            session.query(ModelVersion)\
                .filter(ModelVersion.is_active == True)\
                .update({'is_active': False})
            
            # Create new model version
            new_version = ModelVersion(
                version=version,
                training_data_count=training_data_count,
                performance_metrics=json.dumps(performance_metrics),
                is_active=True
            )
            session.add(new_version)
            session.commit()
        finally:
            session.close()
            
    def mark_data_as_used(self, data_ids: List[int]) -> None:
        """Mark training data as used after training"""
        session = Session(self.engine)
        try:
            session.query(TrainingData)\
                .filter(TrainingData.id.in_(data_ids))\
                .update({'used_for_training': True})
            session.commit()
        finally:
            session.close()
            
    def get_active_model_version(self) -> Dict[str, Any]:
        """Get information about the currently active model version"""
        session = Session(self.engine)
        try:
            model = session.query(ModelVersion)\
                .filter(ModelVersion.is_active == True)\
                .first()
            if model:
                return {
                    'version': model.version,
                    'training_data_count': model.training_data_count,
                    'performance_metrics': json.loads(model.performance_metrics),
                    'created_at': model.created_at
                }
            return None
        finally:
            session.close() 