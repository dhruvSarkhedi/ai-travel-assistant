from typing import Dict, Any, List
import json
from datetime import datetime
from memory.training_manager import TrainingManager
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
import torch
from datasets import Dataset

class ModelTrainer:
    def __init__(self, base_model_name: str = "gpt2"):
        self.base_model_name = base_model_name
        self.training_manager = TrainingManager()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def prepare_dataset(self, data: List[Dict[str, Any]]) -> Dataset:
        """Convert training data into a HuggingFace dataset"""
        # Format data for training
        formatted_data = []
        for item in data:
            formatted_data.append({
                'text': f"User: {item['input']}\nAssistant: {item['response']}"
            })
        
        return Dataset.from_list(formatted_data)
    
    def train_model(self, train_data: List[Dict[str, Any]], 
                   val_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the model on the provided data"""
        # Load model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(self.base_model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        
        # Prepare datasets
        train_dataset = self.prepare_dataset(train_data)
        val_dataset = self.prepare_dataset(val_data)
        
        # Tokenize datasets
        def tokenize_function(examples):
            return tokenizer(examples['text'], padding='max_length', truncation=True)
        
        tokenized_train = train_dataset.map(tokenize_function, batched=True)
        tokenized_val = val_dataset.map(tokenize_function, batched=True)
        
        # Set up training arguments
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=100,
            save_strategy="steps",
            save_steps=100,
            load_best_model_at_end=True,
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_train,
            eval_dataset=tokenized_val,
        )
        
        # Train the model
        trainer.train()
        
        # Evaluate the model
        eval_results = trainer.evaluate()
        
        # Generate new model version
        version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save model and update version info
        model.save_pretrained(f"./models/{version}")
        tokenizer.save_pretrained(f"./models/{version}")
        
        # Update model version in database
        self.training_manager.update_model_version(
            version=version,
            training_data_count=len(train_data),
            performance_metrics=eval_results
        )
        
        return {
            'version': version,
            'metrics': eval_results,
            'training_samples': len(train_data)
        }
    
    def run_training_pipeline(self) -> Dict[str, Any]:
        """Run the complete training pipeline"""
        # Get high-quality training data
        training_data = self.training_manager.get_training_data()
        
        if not training_data:
            return {'status': 'no_data', 'message': 'No new training data available'}
        
        # Prepare data
        prepared_data = self.training_manager.prepare_training_data(training_data)
        
        # Train model
        training_results = self.train_model(
            prepared_data['train'],
            prepared_data['validation']
        )
        
        # Mark data as used
        data_ids = [d['id'] for d in training_data]
        self.training_manager.mark_data_as_used(data_ids)
        
        return {
            'status': 'success',
            'results': training_results
        } 