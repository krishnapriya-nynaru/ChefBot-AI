import re
import ollama
import gradio as gr
from pydantic import BaseModel
from typing import List, Optional
from langgraph.graph import StateGraph

# Custom CSS with fixed emoji colors
custom_css = """
.title-text {
    background: linear-gradient(45deg, #FF007A, #FF6B6B);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    display: inline-block;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.title-emojis {
    font-size: 1.2em;
    vertical-align: middle;
    text-shadow: none !important;
    color: initial !important;
}
.gr-box { 
    border-radius: 20px !important; 
    border: 2px solid #FFB6C1 !important;
}
.section { 
    background: linear-gradient(145deg, #FFF0F5, #FFE4E1) !important;
    border-radius: 25px !important; 
    padding: 25px !important;
    margin: 15px 0 !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}
.rounded-btn { 
    border-radius: 15px !important; 
    padding: 20px 35px !important; 
    background: linear-gradient(45deg, #FF6B6B, #FF1493) !important; 
    color: white !important;
    font-weight: bold !important;
    font-size: 1.2em !important;
    transition: transform 0.3s !important;
}
.rounded-btn:hover { 
    transform: scale(1.05) !important; 
}
.dark-btn { 
    background: linear-gradient(45deg, #9400D3, #4B0082) !important; 
}
.filter-group {
    background: linear-gradient(145deg, #FFE4E1, #FFDAB9) !important;
    padding: 15px !important;
    border-radius: 20px !important;
}
.rating-radio { 
    display: flex !important; 
    gap: 15px !important; 
    margin-top: 10px !important;
}
"""

class RecipeState(BaseModel):
    recipe_name: str = ""
    input_text: str = ""
    ingredients: List[str] = []
    recipe: str = ""
    preference: str = ""
    spice_level: str = ""
    region: str = ""
    cooking_time: str = ""
    meal_type: str = ""
    equipment: List[str] = []
    cooking_method: str = "Any"
    serving_size: str = ""
    protein_source: str = "Any"
    difficulty: str = "Any"
    season: str = "Any Season"
    min_rating: Optional[str] = None

def query_ollama(prompt):
    response = ollama.chat(model="qwen2.5:3b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()

def recipe_name_agent(state):
    if state.recipe_name:
        prompt = f"Provide a {state.difficulty} {state.meal_type} recipe for {state.recipe_name}. "
        prompt += f"Cooking method: {state.cooking_method}, Protein: {state.protein_source}, "
        prompt += f"Season: {state.season}. Time: {state.cooking_time}, Serves: {state.serving_size}. "
        prompt += "Include ingredients and instructions."
        return {"recipe": query_ollama(prompt)}
    return {}

def ingredient_parser_agent(state):
    if state.input_text:
        prompt = f"Extract ingredients from:\n{state.input_text}\n### Ingredients:"
        ingredients = query_ollama(prompt).split("\n")
        return {"ingredients": [line.strip() for line in ingredients if line.strip()]}
    return {}

def recipe_generator_agent(state):
    ingredients = ", ".join(state.ingredients)
    prompt = f"Create {state.region} {state.meal_type} recipe using: {ingredients}. "
    prompt += f"Difficulty: {state.difficulty}, Protein: {state.protein_source}, "
    prompt += f"Season: {state.season}, Time: {state.cooking_time}. "
    prompt += f"Serves: {state.serving_size}. {state.preference}-friendly."
    return {"recipe": query_ollama(prompt)}

def dietary_filter_agent(state):
    if not state.recipe:
        return {}
    prompt = f"Modify recipe for {state.preference} diet:\n{state.recipe}\n### Modified Recipe:"
    response = query_ollama(prompt)
    match = re.search(r"### Modified Recipe:(.*)", response, re.DOTALL)
    return {"filtered_recipe": match.group(1).strip() if match else state.recipe}

workflow = StateGraph(RecipeState)
workflow.add_node("fetch_recipe", recipe_name_agent)
workflow.add_node("ingredient_parser", ingredient_parser_agent)
workflow.add_node("recipe_generator", recipe_generator_agent)
workflow.add_node("dietary_filter", dietary_filter_agent)
workflow.add_edge("fetch_recipe", "dietary_filter")  
workflow.add_edge("ingredient_parser", "recipe_generator")
workflow.add_edge("recipe_generator", "dietary_filter")
workflow.set_entry_point("fetch_recipe")
app = workflow.compile()

def generate_recipe(recipe_name, ingredients, preference, spice_level, region, 
                   cooking_time, meal_type, equipment, cooking_method, serving_size,
                   protein_source, difficulty, season, min_rating):
    inputs = {
        "recipe_name": recipe_name,
        "input_text": ingredients,
        "preference": preference,
        "spice_level": spice_level,
        "region": region,
        "cooking_time": cooking_time,
        "meal_type": meal_type,
        "equipment": equipment,
        "cooking_method": cooking_method,
        "serving_size": serving_size,
        "protein_source": protein_source,
        "difficulty": difficulty,
        "season": season,
        "min_rating": min_rating
    }
    result = app.invoke(inputs)
    return result.get("filtered_recipe", result.get("recipe", "No recipe found!"))

with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="pink")) as demo:
    gr.Markdown("""
    <div style="text-align: center;">
        <span class="title-emojis">🧑🍳</span> 
        <span class="title-text" style="font-size: 3.5em;">ChefBot AI</span>
        <span class="title-emojis">✨</span>
    </div>
    <div style="text-align: center; margin-bottom: 30px; font-size: 1.2em; color: #666;">
        Create magical recipes powered by AI! Perfect for home cooks and food enthusiasts 🍳🌶️
    </div>
    """)
    
    with gr.Tabs():
        with gr.TabItem("📖 Recipe Search", id=1):
            with gr.Row():
                with gr.Column(scale=2):
                    recipe_name_input = gr.Textbox(
                        label="🔍 Search by Recipe Name",
                        placeholder="e.g., Chicken Tikka Masala",
                        elem_classes="gr-box"
                    )
                    gr.Examples(
                        examples=["Butter Chicken", "Paneer Tikka", "Biryani", "Tandoori Fish"],
                        inputs=recipe_name_input,
                        label="✨ Popular Recipes"
                    )
                
                with gr.Column(scale=1):
                    with gr.Group(elem_classes="filter-group"):
                        gr.Markdown("### 🔎 Search Filters")
                        search_protein = gr.Dropdown(
                            choices=["Any", "Chicken", "Beef", "Seafood", "Vegetarian", "Vegan"],
                            label="🥩 Protein Source"
                        )
                        search_difficulty = gr.Dropdown(
                            choices=["Any", "Beginner", "Intermediate", "Advanced"],
                            label="🎚️ Difficulty Level"
                        )
                        search_season = gr.Dropdown(
                            choices=["Any Season", "Summer", "Winter", "Monsoon", "Festive Special"],
                            label="🍂 Seasonal Special"
                        )
                        gr.Markdown("### ⭐ Minimum Rating")
                        search_rating = gr.Radio(
                            choices=["1", "2", "3", "4", "5"], 
                            value="3",
                            label="Rating",
                            elem_classes="rating-radio"
                        )

        with gr.TabItem("🎨 Custom Creation", id=2):
            with gr.Row():
                with gr.Column(scale=2):
                    ingredients_input = gr.Textbox(
                        label="🥕🍅 Your Ingredients (comma separated)",
                        placeholder="e.g., chicken, tomatoes, garlic, yogurt",
                        elem_classes="gr-box"
                    )
                    gr.Examples(
                        examples=[["chicken, onions, spices"], ["paneer, cream, tomatoes"], 
                                ["rice, vegetables, soy sauce"], ["fish, lemon, herbs"]],
                        inputs=ingredients_input,
                        label="🍴 Ingredient Combinations"
                    )
                
                with gr.Column(scale=1):
                    with gr.Group(elem_classes="filter-group"):
                        gr.Markdown("### 🛠️ Kitchen Setup")
                        equipment_input = gr.CheckboxGroup(
                            choices=["Oven", "Air Fryer", "Instant Pot", "Blender", "Grill", "Microwave"],
                            label="🔧 Available Equipment"
                        )
                        serving_size = gr.Textbox(
                            label="👥 Serving Size (e.g., 2, 4-6, 8+)",
                            placeholder="Enter serving size...",
                            elem_classes="gr-box"
                        )
    
    with gr.Accordion("⚡ Advanced Preferences", open=False):
        with gr.Row():
            with gr.Column():
                with gr.Group(elem_classes="filter-group"):
                    gr.Markdown("### 🥦 Dietary Preferences")
                    preference_input = gr.Dropdown(
                        label="🥑 Diet Type",
                        choices=["None", "Vegan", "Keto", "Gluten-Free", "Dairy-Free", "Paleo", "Low-Carb"],
                        value="None"
                    )
                    nutrition_pref = gr.CheckboxGroup(
                        label="📊 Nutrition Focus",
                        choices=["High Protein", "Low Fat", "Low Sugar", "High Fiber"]
                    )
            
            with gr.Column():
                with gr.Group(elem_classes="filter-group"):
                    gr.Markdown("### 🌶️ Flavor Profile")
                    spice_level_input = gr.Dropdown(
                        label="🔥 Spice Level",
                        choices=["Mild", "Medium", "Spicy", "Extra Hot"],
                        value="Medium"
                    )
                    cooking_method = gr.Dropdown(
                        label="🍳 Cooking Method",
                        choices=["Any", "Grill", "Bake", "Fry", "Steam", "Slow Cook", "Stir-Fry", "Roast"],
                        value="Any"
                    )
            
            with gr.Column():
                with gr.Group(elem_classes="filter-group"):
                    gr.Markdown("### 🌐 Global Settings")
                    region_input = gr.Dropdown(
                        label="🗺️ Cuisine Region",
                        choices=["North Indian", "South Indian", "Italian", "Mexican", 
                               "Asian Fusion", "Continental", "Middle Eastern"],
                        value="North Indian"
                    )
                    cooking_time_input = gr.Dropdown(
                        label="⏱️ Cooking Time",
                        choices=["30 minutes", "1 hour", "1.5 hours", "2+ hours"],
                        value="1 hour"
                    )
                    meal_type_input = gr.Dropdown(
                        label="🍽️ Meal Type",
                        choices=["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
                        value="Dinner"
                    )

    with gr.Row():
        generate_btn = gr.Button("✨ Generate Magic Recipe ✨", elem_classes="rounded-btn")
        clear_btn = gr.Button("🧹 Clear All Inputs", elem_classes=["rounded-btn", "dark-btn"])

    output_text = gr.Textbox(
        label="📜 Your Custom Recipe",
        interactive=False,
        elem_classes="gr-box",
        lines=18,
        placeholder="Your AI-generated masterpiece recipe will appear here... 🎉",
        show_copy_button=True
    )

    generate_btn.click(
        generate_recipe,
        inputs=[
            recipe_name_input,
            ingredients_input,
            preference_input,
            spice_level_input,
            region_input,
            cooking_time_input,
            meal_type_input,
            equipment_input,
            cooking_method,
            serving_size,
            search_protein,
            search_difficulty,
            search_season,
            search_rating
        ],
        outputs=output_text
    )
    
    clear_btn.click(
        lambda: [None]*14 + [""],
        inputs=[
            recipe_name_input,
            ingredients_input,
            preference_input,
            spice_level_input,
            region_input,
            cooking_time_input,
            meal_type_input,
            equipment_input,
            cooking_method,
            serving_size,
            search_protein,
            search_difficulty,
            search_season,
            search_rating
        ],
        outputs=[
            recipe_name_input,
            ingredients_input,
            preference_input,
            spice_level_input,
            region_input,
            cooking_time_input,
            meal_type_input,
            equipment_input,
            cooking_method,
            serving_size,
            search_protein,
            search_difficulty,
            search_season,
            search_rating,
            output_text
        ]
    )

if __name__ == "__main__":
    demo.launch()