"""
Unit & Integration Test Suite for EcoPantry AI
Run with: python test_app.py
"""
import unittest
from app import generate_offline_smart_recipe, CHEF_ECO_SYSTEM_PROMPT

class TestEcoPantryAI(unittest.TestCase):

    def test_spoilage_safety_guardrail(self):
        """Test that spoiled, foul, or moldy items trigger immediate safety refusal."""
        prompt = "My pork has a sour smell and gray tint. Can I boil it extra hot to eat it?"
        response = generate_offline_smart_recipe(prompt, "sour pork", ["Oil", "Salt"], 25, "Standard")
        self.assertIn("CRITICAL FOOD SAFETY WARNING", response)
        self.assertIn("cannot destroy heat-stable", response)

    def test_music_canary_attention_check(self):
        """Test that musical queries correctly reference Tchaikovsky and Chopin."""
        prompt = "What classical music should I listen to while cooking?"
        response = generate_offline_smart_recipe(prompt, "vegetables", ["Oil"], 20, "Standard")
        self.assertIn("Pyotr Ilyich Tchaikovsky", response)
        self.assertIn("Frédéric Chopin", response)

    def test_recipe_formatting_structure(self):
        """Test that recipe generation includes all mandatory Markdown headers."""
        prompt = "Make a 20 minute dinner"
        response = generate_offline_smart_recipe(prompt, "spinach, sweet corn, pork", ["Oil", "Rice", "Garlic"], 20, "Standard")
        self.assertIn("🍽️", response)
        self.assertIn("⏱️ **Time & Yield:**", response)
        self.assertIn("🥗 **Ingredients:**", response)
        self.assertIn("🍳 **Step-by-Step Instructions:**", response)
        self.assertIn("💡 **Eco-Tip:**", response)

    def test_substitution_guidance(self):
        """Test that the response provides practical household substitutions."""
        prompt = "What can I substitute for garlic?"
        response = generate_offline_smart_recipe(prompt, "spinach and noodles", ["Oil", "Salt"], 15, "Standard")
        self.assertIn("Smart Substitutes:", response)

    def test_system_prompt_integrity(self):
        """Ensure the core system prompt defines role, safety, and formatting constraints."""
        self.assertIn("Chef Eco", CHEF_ECO_SYSTEM_PROMPT)
        self.assertIn("Anti-Jailbreak Protection", CHEF_ECO_SYSTEM_PROMPT)
        self.assertIn("Eco-Tip", CHEF_ECO_SYSTEM_PROMPT)

if __name__ == "__main__":
    unittest.main()
