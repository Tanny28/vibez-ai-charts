# backend/app/ml_vibe_engine.py
# ML-enhanced vibe engine with training capability
import os
import json
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class MLVibeEngine:
    """ML-powered chart recommendation engine that can be trained on real data."""
    
    def __init__(self, model_path: str = None):
        # Use absolute path to avoid issues with working directory
        if model_path is None:
            base_dir = Path(__file__).parent.parent
            model_path = str(base_dir / "models" / "vibe_classifier.pkl")
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(
            max_features=1000,  # Increased from 500 for better feature coverage
            ngram_range=(1, 4),  # Added 4-grams for better phrase matching
            stop_words='english',
            min_df=1,  # Include even rare terms
            sublinear_tf=True  # Use log-scaling for term frequencies
        )
        self.classifier = RandomForestClassifier(
            n_estimators=200,  # Increased from 100 for better ensemble
            max_depth=15,  # Increased from 10 for more complex patterns
            min_samples_split=3,  # More sensitive to patterns
            min_samples_leaf=1,  # Allow finer granularity
            random_state=42,
            class_weight='balanced'  # Handle class imbalance better
        )
        self.chart_types = [
            "line", "grouped_bar", "histogram", "scatter", 
            "stacked_bar", "horizontal_bar", "choropleth"
        ]
        self.is_trained = False
        self.load_model()
    
    def train(self, training_data: List[Tuple[str, str]]):
        """
        Train the model on labeled data.
        
        Args:
            training_data: List of (prompt, chart_type) tuples
            
        Example:
            training_data = [
                ("show sales trends over time", "line"),
                ("compare revenue by region", "grouped_bar"),
                ("distribution of customer ages", "histogram"),
            ]
        """
        if len(training_data) < 10:
            raise ValueError("Need at least 10 training examples")
        
        # Separate features and labels
        prompts, labels = zip(*training_data)
        
        # Vectorize text
        X = self.vectorizer.fit_transform(prompts)
        y = np.array(labels)
        
        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train classifier
        self.classifier.fit(X_train, y_train)
        
        # Calculate accuracy
        train_acc = self.classifier.score(X_train, y_train)
        val_acc = self.classifier.score(X_val, y_val)
        
        self.is_trained = True
        
        print(f"Training complete!")
        print(f"Training accuracy: {train_acc:.2%}")
        print(f"Validation accuracy: {val_acc:.2%}")
        
        # Save model
        self.save_model()
        
        return {
            "train_accuracy": train_acc,
            "validation_accuracy": val_acc,
            "num_examples": len(training_data)
        }
    
    def predict(self, prompt: str, get_probabilities: bool = False) -> Dict:
        """
        Predict the best chart type for a given prompt.
        
        Args:
            prompt: User's data goal text
            get_probabilities: Whether to return confidence scores
            
        Returns:
            Dict with prediction and optional probabilities
        """
        if not self.is_trained:
            return {
                "chart_type": "grouped_bar",  # Fallback
                "confidence": 0.0,
                "method": "fallback",
                "message": "Model not trained. Using fallback."
            }
        
        # Vectorize input
        X = self.vectorizer.transform([prompt])
        
        # Predict
        prediction = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [
            {
                "chart_type": self.classifier.classes_[idx],
                "confidence": float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        result = {
            "chart_type": prediction,
            "confidence": float(max(probabilities)),
            "method": "ml_model",
            "top_predictions": top_predictions if get_probabilities else None
        }
        
        return result
    
    def save_model(self):
        """Save the trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            "vectorizer": self.vectorizer,
            "classifier": self.classifier,
            "chart_types": self.chart_types,
            "is_trained": self.is_trained
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a trained model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.vectorizer = model_data["vectorizer"]
                self.classifier = model_data["classifier"]
                self.chart_types = model_data["chart_types"]
                self.is_trained = model_data["is_trained"]
                
                print(f"Model loaded from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model: {e}")
                self.is_trained = False
        else:
            print("No pre-trained model found. Use train() to create one.")
    
    def add_feedback(self, prompt: str, correct_chart_type: str, 
                     feedback_file: str = None):
        """
        Record user feedback for continuous improvement.
        
        Args:
            prompt: The original user prompt
            correct_chart_type: The chart type that worked best
            feedback_file: Path to append feedback
        """
        if feedback_file is None:
            base_dir = Path(__file__).parent.parent
            feedback_file = str(base_dir / "data" / "user_feedback.jsonl")
        
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        
        feedback = {
            "prompt": prompt,
            "chart_type": correct_chart_type,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback) + '\n')
        
        print(f"Feedback recorded: {prompt} -> {correct_chart_type}")
    
    def retrain_from_feedback(self, feedback_file: str = None):
        """
        Retrain the model using collected user feedback.
        
        Args:
            feedback_file: Path to feedback JSONL file
        """
        if feedback_file is None:
            base_dir = Path(__file__).parent.parent
            feedback_file = str(base_dir / "data" / "user_feedback.jsonl")
        
        if not os.path.exists(feedback_file):
            raise FileNotFoundError(f"No feedback file found at {feedback_file}")
        
        # Load feedback
        training_data = []
        with open(feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                training_data.append((data["prompt"], data["chart_type"]))
        
        print(f"Loaded {len(training_data)} examples from feedback")
        
        # Retrain
        return self.train(training_data)


# Global instance
_ml_engine = None

def get_ml_engine() -> MLVibeEngine:
    """Get or create the global ML engine instance."""
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = MLVibeEngine()
    return _ml_engine
