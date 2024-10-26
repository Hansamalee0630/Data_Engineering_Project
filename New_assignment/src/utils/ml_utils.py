import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.config import ML_CONFIG

class CustomerPredictor:
    def __init__(self):
        self.model = LogisticRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_data(self, df):
        # Create features
        features_df = df.groupby('customer_id').agg({
            'display_order_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        
        # Create target (repeat purchaser = more than 1 order)
        features_df['is_repeat'] = (features_df['display_order_id'] > 1).astype(int)
        
        return features_df
        
    def train(self, df):
        if len(df) < 50:  # Minimum data requirement
            return False, "Insufficient data for training (minimum 50 customers required)"
            
        features_df = self.prepare_data(df)
        
        X = features_df[['display_order_id', 'total_amount']]
        y = features_df['is_repeat']
        
        # Check if we have both classes
        if len(np.unique(y)) < 2:
            return False, "Insufficient class variation in the data"
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        return True, f"Model trained successfully with accuracy: {accuracy:.2f}"
        
    def predict(self, orders, total_amount):
        if not self.is_trained:
            return None, "Model not trained yet"
            
        features = np.array([[orders, total_amount]])
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)
        probability = self.model.predict_proba(features_scaled)[0]
        
        return prediction[0], probability