# Quick test script for ML model
from app.ml_vibe_engine import get_ml_engine

print("="*60)
print("Testing ML Model with Your Prompts")
print("="*60)

engine = get_ml_engine()
print(f"\n✅ Model trained: {engine.is_trained}")
print(f"✅ Model path: {engine.model_path}")

if engine.is_trained:
    # Test with your actual prompts
    test_prompts = [
        "show the growth for first 2 years",
        "fhow the gowth for first 2 years",
        "show sales trends over time",
        "compare revenue by region",
        "distribution of customer ages"
    ]
    
    print("\nTesting predictions:")
    print("-" * 60)
    for prompt in test_prompts:
        result = engine.predict(prompt)
        confidence = result['confidence']
        
        # Check if it would use ML or fallback
        will_use_ml = confidence > 0.5
        method = "🤖 ML" if will_use_ml else "📋 Rule-based (ML confidence too low)"
        
        print(f"\nPrompt: '{prompt}'")
        print(f"  → ML predicted: {result['chart_type']} ({confidence:.1%} confidence)")
        print(f"  → System will use: {method}")
else:
    print("\n❌ Model not trained!")

print("\n" + "="*60)
print("Note: ML is used when confidence > 50%")
print("Otherwise, rule-based keyword matching is used as fallback")
print("="*60)

