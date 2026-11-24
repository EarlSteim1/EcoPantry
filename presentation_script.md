# EcoPantry AI: 3-Minute Project Presentation & Demo Script 🎙️

**Presenter:** [Your Name / Team Members]  
**Topic:** Final Project Proposal — Streamlit AI Chatbot (EcoPantry AI)  
**Target Duration:** ~3 minutes  

---

## ⏱️ [0:00 - 0:40] Part 1: The Problem & Our Goal
*(Slide / Screen: Show the EcoPantry Title & Problem Statement)*

> "Hello everyone and [Professor/Instructor's Name]. 
> 
> Did you know that the average household throws away over 30% of the food they buy, costing hundreds of dollars every year and creating significant carbon emissions? Often, it’s not because people don't want to cook—it's because they stare into their fridge, see half an onion, wilting spinach, and leftover cooked meat, and have no idea how to turn those random leftovers into a cohesive meal.
> 
> To solve this, our team proposed and built **EcoPantry AI**: a smart, zero-waste culinary assistant designed to empower home cooks to minimize food waste and lower grocery bills by dynamically transforming leftover pantry ingredients into safe, delicious, and tailored recipes."

---

## ⏱️ [0:40 - 1:20] Part 2: Architecture & Key Features
*(Slide / Screen: Point to the Streamlit UI and Sidebar)*

> "Unlike generic chatbots where you have to type everything from scratch, EcoPantry AI uses a **hybrid dual-input system**:
> 
> 1. In the sidebar, users can quickly check off their standard household staples like cooking oil, garlic, and rice, or drag-and-drop a grocery receipt.
> 2. Users simply type whatever perishable leftovers they need to rescue today.
> 3. Users can set constraints like maximum cooking time—say, 25 minutes—and filter by dietary preferences like vegetarian or gluten-free.
> 
> Under the hood, the app tracks food waste reduction in real-time with an interactive sustainability scorecard, showing exactly how many pounds of food were rescued."

---

## ⏱️ [1:20 - 2:20] Part 3: Live Application Walkthrough
*(Action: Type into the Streamlit input: *"I have baby spinach, cooked pork loin, and sweet corn. What can I make in 20 minutes?"*)*

> "Let's see it in action. Here, I've checked off cooking oil, garlic, and rice in our sidebar. I'll ask Chef Eco: *'I have half a bag of baby spinach, cooked pork loin, and sweet corn. What can I make in 20 minutes?'*
> 
> Notice how Chef Eco responds using a clean, structured recipe card:
> - It breaks down ingredients into what we already have versus assumed staples.
> - It gives us actionable, step-by-step cooking instructions.
> - It provides a smart substitution—such as using garlic powder if we lack fresh cloves.
> - And crucially, it includes an **Eco-Tip**, showing us how to repurpose leftovers like freezing sweet corn liquid for vegetable stock."

---

## ⏱️ [2:20 - 3:00] Part 4: Safety Guardrails & Conclusion
*(Slide / Screen: Show System Prompt & Export Button)*

> "Finally, we engineered robust safety and anti-injection rules into Chef Eco’s system prompt:
> - If an ingredient smells bad or has mold, Chef Eco immediately triggers a food safety warning and refuses to approve spoiled food.
> - It resists prompt injection attacks and stays strictly within its culinary domain.
> - And users can export their entire recipe transcript with a single click using the `Export Chat` button.
> 
> In summary, EcoPantry AI bridges the gap between AI reasoning and domestic sustainability, helping users save money, eat healthier, and fight food waste one meal at a time. Thank you, and we'd love to answer any questions!"
