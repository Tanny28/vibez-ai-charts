# Fresh test script that bypasses caching
import os
os.chdir(os.path.dirname(__file__))

from app.ml_vibe_engine import MLVibeEngine

print("="*60)
print("Testing ML Model with Fresh Load (No Cache)")
print("="*60)

# Force fresh instance (not using get_ml_engine cache)
engine = MLVibeEngine()
print(f"\n✅ Model trained: {engine.is_trained}")
print(f"✅ Model path: {os.path.abspath(engine.model_path)}")

if engine.is_trained:
    # Test with your actual prompts
    test_prompts = [
        "show the growth for first 2 years",
        "show sales trends over time",
        "compare revenue by region",
        "distribution of customer ages",
        "top 10 selling products",
        "relationship between price and demand",
        "market share breakdown"
    ]
    
    print("\nTesting predictions:")
    print("-" * 60)
    for prompt in test_prompts:
        result = engine.predict(prompt, get_probabilities=True)
        confidence = result['confidence']
        
        # Check if it would use ML or fallback (using 35% threshold like main.py)
        will_use_ml = confidence > 0.35
        method = "🤖 ML" if will_use_ml else "📋 Rule-based (ML confidence too low)"
        
        print(f"\nPrompt: '{prompt}'")
        print(f"  → ML predicted: {result['chart_type']} ({confidence:.1%} confidence)")
        print(f"  → Top 3: {result.get('top_predictions', [])}")
        print(f"  → System will use: {method}")
else:
    print("\n❌ Model not trained!")

print("\n" + "="*60)
print("Note: ML is used when confidence > 35%")
print("Otherwise, rule-based keyword matching is used as fallback")
print("="*60)
