# ChefBot-AI
## ChefBot AI 🍽️🤖
ChefBot AI is an intelligent recipe generator powered by Qwen2.5, Ollama, LangGraph, and Gradio. This AI-driven system creates personalized recipes based on available ingredients, dietary preferences, spice levels, and regional flavors. Whether you're looking for a classic dish or something new, ChefBot AI is your smart cooking assistant!


## Table of Contents
- [Key Features](#key-features)
- [Supported Cuisines & Spice Levels](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Results & User Interface](#results)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Key Features:
1. ***🍳 AI-Powered Recipe Generation –*** Generates step-by-step recipes using Qwen2.5 via Ollama.
2. ***🥕 Ingredient-Based Recipe Suggestion –*** Extracts ingredients from user input and suggests suitable dishes.
3. ***🥗 Dietary Customization –*** Modifies recipes for Vegan, Keto, Gluten-Free, and other preferences.
4. ***🌶️ Spice Level & Regional Cuisine Options –*** Customize recipes to match your spice tolerance and preferred cuisine.
5. ***🔄 LangGraph Workflow –*** Uses modular AI agents for recipe parsing, filtering, and generation.
6. ***🖥️ Interactive UI with Gradio –*** Provides a user-friendly web interface for easy recipe generation.

## Supported Cuisines & Spice Levels 🥘🔥

This AI-powered recipe assistant allows users to select from various cuisines and adjust the spice levels to match their preferences:

| **Cuisine**            | **Region** | **Spice Levels** |
|-------------------------|---------|-----------------------------------------------------------|
| **Indian**        | `North, South`     | Normal, Spicy, Medium-Spicy|
| **American**          | `US, UK`     | Normal, Spicy, Medium-Spicy|
| **Asian**           | `Chinese, Japanese`     | Normal, Spicy, Medium-Spicy  |
| **European**   | `Italian, French`     |Normal, Spicy, Medium-Spicy|
| **Latin American**            | `Mexican, Brazilian`     |Normal, Spicy, Medium-Spicy |

## Installation
1. Create conda enviroenment 
    ```bash
    conda create -n env_name python=3.10
2. Activate conda enviroenment
    ```bash
    conda activate env_name
3. Clone this repository:
   ```bash
   git clone https://github.com/krishnapriya-nynaru/Multilingual-AI-Audiobook-Narrator.git
2. Change to Project directory
    ```bash
    cd ChefBot-AI
3. Install required packages :
    ```bash
    pip install -r requirements.txt

## Usage
1. Run the AI Recipe Generator:
    ```bash
    python app.py
2. Open your browser and navigate to: [http://127.0.0.1:7860/](http://127.0.0.1:7860/)

3. Interact with the UI:
    - Enter a recipe name(***Recipe search***) or list of ingredients(***Custom recepie***).
    - Select search Filters Protein source, Difficulty Level, Seasonal special. 
    - Select Advanced preferences like dietary preferences, Flavor profile and global settings.
    - Click ***Generate Recipe*** to get AI-powered cooking instructions.
    - View, save, or print the generated recipe!

## Results & User Interface

![alt_text](https://github.com/krishnapriya-nynaru/YOLOv11-FaceAnonymization/blob/main/
YOLOv11_faceanonymization/output_videos/result_video.gif)

## Contributing 
Contributions are welcome! To contribute to this project:
1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and ensure the code passes all tests.
4. Submit a pull request with a detailed description of your changes.

If you have any suggestions for improvements or features, feel free to open an issue!

## Acknowledgments  

💡 Powered by:

- [**Ollama**](https://ollama.com/library/qwen2.5) – Efficient local LLM inference
- [**Qwen2.5**](https://huggingface.co/Qwen/Qwen2.5-3B) – Advanced multilingual LLM for text generation
- [**LangGraph**](https://github.com/langchain-ai/langgraph) – AI workflow management framework
- [**Gradio**](https://www.gradio.app/) – User-friendly web UI framework

🔗 Explore, cook, and innovate with AI-driven recipes! 🚀🍽️

