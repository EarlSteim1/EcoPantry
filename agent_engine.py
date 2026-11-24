"""
EcoPantry AI - Agentic Reasoning & Tool Calling Engine
Implements a ReAct (Reasoning + Action) loop enabling the model to orchestrate
specialized external tools: nutrition calculator, shelf-life lookup, carbon-offset
estimator, and culinary science substitution solver.
"""
import json
import re
from typing import Dict, Any, List, Tuple

# =====================================================================
# Specialized External Tool Implementations
# =====================================================================

def tool_calculate_nutrition(ingredients_str: str) -> Dict[str, Any]:
    """
    Calculates estimated macro-nutritional profile (calories, protein, carbs, fat, fiber)
    based on ingredients.
    """
    ing_lower = ingredients_str.lower()
    calories = 180
    protein = 4
    carbs = 25
    fat = 4
    fiber = 2

    # Ingredient macro heuristics
    if any(k in ing_lower for k in ["chicken", "pork", "beef", "turkey", "meat", "tuna", "salmon"]):
        calories += 220
        protein += 28
        fat += 8
    if any(k in ing_lower for k in ["egg", "eggs"]):
        calories += 140
        protein += 12
        fat += 10
    if any(k in ing_lower for k in ["rice", "pasta", "noodle", "bread", "potato", "corn"]):
        calories += 180
        carbs += 38
        fiber += 2
    if any(k in ing_lower for k in ["spinach", "broccoli", "carrot", "vegetable", "kale", "greens"]):
        calories += 35
        fiber += 4
        carbs += 6
        protein += 2
    if any(k in ing_lower for k in ["cheese", "cream", "butter"]):
        calories += 110
        fat += 9
        protein += 5

    return {
        "status": "success",
        "ingredients_analyzed": ingredients_str,
        "nutrition_per_serving": {
            "calories_kcal": calories,
            "protein_g": protein,
            "carbohydrates_g": carbs,
            "fat_g": fat,
            "dietary_fiber_g": fiber
        },
        "health_score": "High Protein & Balanced Fiber"
    }

def tool_check_food_shelf_life(food_item: str, storage: str = "refrigerator") -> Dict[str, Any]:
    """
    Queries USDA FoodKeeper guidelines for maximum safe storage durations.
    """
    food_clean = food_item.lower().strip()
    storage_clean = storage.lower().strip()
    
    database = {
        "cooked meat": {"fridge": "3 to 4 days", "freezer": "2 to 6 months", "pantry": "Do not leave at room temp > 2 hrs"},
        "pork": {"fridge": "3 to 4 days (cooked) / 1 to 2 days (raw)", "freezer": "3 to 6 months", "pantry": "Unsafe"},
        "chicken": {"fridge": "3 to 4 days (cooked) / 1 to 2 days (raw)", "freezer": "9 months", "pantry": "Unsafe"},
        "spinach": {"fridge": "5 to 7 days", "freezer": "10 to 12 months (blanched)", "pantry": "1 to 2 days"},
        "eggs": {"fridge": "3 to 5 weeks in shell", "freezer": "Do not freeze whole shell; beat and freeze 1 year", "pantry": "Refrigeration recommended"},
        "milk": {"fridge": "7 days after opening", "freezer": "3 months", "pantry": "Unsafe once opened"},
        "rice": {"fridge": "3 to 4 days (cooked)", "freezer": "4 to 6 months", "pantry": "1 to 2 years (uncooked)"},
        "corn": {"fridge": "3 to 5 days after opening can", "freezer": "8 to 12 months", "pantry": "1 to 2 years (unopened can)"}
    }

    match_key = None
    for key in database:
        if key in food_clean or food_clean in key:
            match_key = key
            break

    if match_key:
        info = database[match_key]
        return {
            "food_item": food_item,
            "matched_category": match_key,
            "storage_medium": storage_clean,
            "safe_duration": info.get(storage_clean, info.get("fridge")),
            "usda_guideline": "Maintain refrigerator temperature strictly at or below 40°F (4.4°C)."
        }
    
    return {
        "food_item": food_item,
        "matched_category": "General Perishable Food",
        "storage_medium": storage_clean,
        "safe_duration": "3 to 4 days refrigerated",
        "usda_guideline": "When in doubt, check for sensory indicators (odor, slime, mold). Discard if held > 2 hrs at room temp."
    }

def tool_calculate_carbon_and_savings(weight_lbs: float, food_category: str = "mixed") -> Dict[str, Any]:
    """
    Deterministic environmental calculator: computes exact greenhouse gas emission offset
    (kg CO2e) and financial grocery savings ($).
    """
    category_factors = {
        "meat": {"co2_per_lb": 6.8, "cost_per_lb": 5.50},
        "dairy": {"co2_per_lb": 3.2, "cost_per_lb": 3.80},
        "produce": {"co2_per_lb": 1.4, "cost_per_lb": 2.40},
        "grains": {"co2_per_lb": 1.8, "cost_per_lb": 1.80},
        "mixed": {"co2_per_lb": 2.5, "cost_per_lb": 3.40}
    }
    
    factor = category_factors.get(food_category.lower(), category_factors["mixed"])
    co2_kg = round(weight_lbs * factor["co2_per_lb"], 2)
    dollars_saved = round(weight_lbs * factor["cost_per_lb"], 2)
    
    return {
        "weight_rescued_lbs": weight_lbs,
        "co2e_avoided_kg": co2_kg,
        "dollars_saved_usd": dollars_saved,
        "environmental_equivalent": f"Equivalent to driving {round(co2_kg * 2.5, 1)} fewer miles in an average gasoline car."
    }

def tool_substitute_ingredient(missing_item: str, dish_type: str = "cooking") -> Dict[str, Any]:
    """
    Returns culinary science substitution ratios with preparation instructions.
    """
    missing_lower = missing_item.lower().strip()
    sub_table = {
        "garlic": {"substitute": "1/2 tsp Garlic Powder or 1/4 cup minced shallot/onion per clove", "notes": "Add powder during saucing to prevent burning."},
        "onion": {"substitute": "Shallots, leeks, scallion whites, or 1 tbsp onion powder", "notes": "Shallots offer slightly sweeter flavor."},
        "buttermilk": {"substitute": "1 cup whole milk + 1 tbsp lemon juice or white vinegar", "notes": "Let sit 5 minutes to curdle."},
        "egg": {"substitute": "1/4 cup applesauce or 1 tbsp ground flaxseed + 3 tbsp water", "notes": "Ideal for baked goods and binding."},
        "heavy cream": {"substitute": "3/4 cup milk + 1/4 cup melted butter", "notes": "Whisk thoroughly; do not use for whipped cream."},
        "soy sauce": {"substitute": "1 tbsp Worcestershire sauce + 1 pinch salt, or coconut aminos", "notes": "Provides dark umami depth."}
    }

    for key, data in sub_table.items():
        if key in missing_lower:
            return {"missing_item": missing_item, "primary_substitute": data["substitute"], "culinary_notes": data["notes"]}

    return {
        "missing_item": missing_item,
        "primary_substitute": "Universal pantry swap: Season with pinch of salt, splash of mild vinegar/lemon for acid, and a pinch of black pepper.",
        "culinary_notes": "Balanced seasoning mimics the aromatic profile of missing minor ingredients."
    }

# =====================================================================
# Agentic ReAct Controller
# =====================================================================

class EcoAgentController:
    """
    Orchestrates the Reasoning + Action loop.
    Decides which tools to trigger based on user intent and executes them.
    """
    def __init__(self):
        self.available_tools = {
            "calculate_nutrition": tool_calculate_nutrition,
            "check_food_shelf_life": tool_check_food_shelf_life,
            "calculate_carbon_and_savings": tool_calculate_carbon_and_savings,
            "substitute_ingredient": tool_substitute_ingredient
        }

    def plan_and_execute(self, query: str, context: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Reasoning loop: evaluates query intent and dispatches tool executions.
        Returns: (reasoning_traces, synthesized_tool_data)
        """
        traces = []
        synthesized_data = {}
        q_lower = query.lower()
        leftovers = context.get("leftovers", "mixed ingredients")
        
        # Reason 1: Nutrition Query or Recipe Request
        if any(w in q_lower for w in ["nutrition", "calories", "protein", "macros", "healthy", "recipe", "make", "cook"]):
            thought = f"User is asking for a meal plan with '{leftovers}'. I should calculate the macro-nutritional breakdown."
            tool_name = "calculate_nutrition"
            action_input = leftovers
            output = tool_calculate_nutrition(action_input)
            traces.append({"step": 1, "thought": thought, "tool": tool_name, "input": action_input, "output": output})
            synthesized_data["nutrition"] = output["nutrition_per_serving"]

        # Reason 2: Shelf-Life or Spoilage Safety Query
        if any(w in q_lower for w in ["expire", "shelf life", "how long", "refrigerate", "keep", "freeze", "bad", "safe", "spoil"]):
            target_food = leftovers.split(",")[0] if leftovers else "cooked meat"
            thought = f"User inquired about storage duration or freshness for '{target_food}'. Querying USDA FoodKeeper database."
            tool_name = "check_food_shelf_life"
            action_input = {"food": target_food, "storage": "refrigerator"}
            output = tool_check_food_shelf_life(target_food)
            traces.append({"step": len(traces) + 1, "thought": thought, "tool": tool_name, "input": str(action_input), "output": output})
            synthesized_data["shelf_life"] = output

        # Reason 3: Substitution Query
        if any(w in q_lower for w in ["substitute", "swap", "replace", "don't have", "out of", "instead"]):
            # Extract missing item candidate
            missing_item = "garlic"
            for candidate in ["garlic", "onion", "egg", "milk", "buttermilk", "cream", "soy sauce"]:
                if candidate in q_lower:
                    missing_item = candidate
                    break
            thought = f"User is missing '{missing_item}'. Dispatched culinary substitution solver."
            tool_name = "substitute_ingredient"
            action_input = missing_item
            output = tool_substitute_ingredient(action_input)
            traces.append({"step": len(traces) + 1, "thought": thought, "tool": tool_name, "input": action_input, "output": output})
            synthesized_data["substitution"] = output

        # Always calculate environmental carbon savings
        tool_name = "calculate_carbon_and_savings"
        thought = "Calculate exact carbon footprint emissions offset and financial grocery savings from this rescued food."
        action_input = 1.2
        output = tool_calculate_carbon_and_savings(action_input, "mixed")
        traces.append({"step": len(traces) + 1, "thought": thought, "tool": tool_name, "input": f"{action_input} lbs", "output": output})
        synthesized_data["carbon_savings"] = output

        return traces, synthesized_data
