# Project Consultation Briefing & Status Report
**Project Name:** EcoPantry AI — Smart Zero-Waste Culinary & Grocery Coach  
**Event:** Advisor / Instructor Consultation Meeting  
**Date:** November 10, 2026  
**Presenters / Group Members:** [Your Name / Team Names]  
**Course / Track:** AI Applications / Final Capstone Project  

---

## 1. Consultation Objective & Agenda (10–15 Minutes)

### Primary Objectives of This Meeting:
1. Present the refined concept, scope, and technical design of **EcoPantry AI**.
2. Demonstrate an early **working Proof-of-Concept (Streamlit prototype)** to show technical feasibility.
3. Validate system prompt guardrails (specifically regarding food safety and domain constraints).
4. Secure advisor approval on implementation milestones and evaluation methodology.

### Suggested Consultation Agenda:
* **00:00 – 03:00 (Pitch):** Executive Problem Statement, Target Audience, and 1-Sentence Primary Goal.
* **03:00 – 06:00 (Architecture):** Streamlit hybrid input design (forms + chat) and LLM orchestration.
* **06:00 – 10:00 (Live Prototype Demo):** Walkthrough of running `app.py` (recipe generation, waste tracking, safety override).
* **10:00 – 15:00 (Feedback & Q&A):** Advisor critique, scope validation, and next steps.

---

## 2. Executive Project Summary

| Item | Specification |
| :--- | :--- |
| **Industry** | Food & Beverage / Consumer Tech & Environmental Sustainability |
| **Primary Goal** | *To empower household cooks to minimize food waste and lower grocery expenses by dynamically transforming available pantry leftovers into safe, customized, and nutritious recipes through an interactive, dual-input Streamlit application.* |
| **Core Value Proposition** | Rather than forcing users to think of recipes or type massive prompts, the app combines quick-toggle pantry checklists (`st.checkbox`), expiring-ingredient inputs (`st.text_input`), and intelligent culinary substitution algorithms. |
| **Target Users** | 1. College students / young professionals on tight food budgets.<br>2. Busy households seeking to eliminate fridge spoilage.<br>3. Zero-waste cooking enthusiasts. |

---

## 3. Scope & Boundary Matrix (Clear In-Scope vs. Out-of-Scope)

```
+--------------------------------------------------+--------------------------------------------------+
|               IN-SCOPE (Committed)               |              OUT-OF-SCOPE (Excluded)             |
+--------------------------------------------------+--------------------------------------------------+
| • Hybrid input: Checkbox staples + text inputs   | • Medical / clinical dietary disease treatment   |
| • Expiration-first recipe synthesis algorithm    | • Endorsement or "salvaging" of spoiled food     |
| • Smart missing-ingredient substitution engine   | • Real-time grocery delivery / API e-commerce    |
| • Real-time interactive cooking Q&A guidance     | • Multi-tenant relational user database (auth)   |
| • Live food waste scorecard (lbs saved)          | • Training foundational LLM weights from scratch |
| • Markdown/text recipe export (st.download_button| • Unbounded general-domain Q&A (sports, coding)  |
+--------------------------------------------------+--------------------------------------------------+
```

---

## 4. Technical Architecture & Tech Stack Justification

### Why Streamlit?
1. **Rapid Reactive UI:** Native components like `st.chat_message`, `st.chat_input`, and `st.session_state` allow full stateful chat loops in pure Python without writing JavaScript or CSS boilerplate.
2. **Form + Chat Synergy:** Streamlit makes it trivial to place deterministic forms in the sidebar while maintaining a streaming conversational chat in the main body.
3. **Low Latency & Fast Prototyping:** Eliminates complex REST API plumbing between separate frontend/backend repositories.

---

## 5. Live Prototype Demonstration Plan (During Consultation)

You can run the existing prototype directly in front of your advisor:
`streamlit run app.py`

### 3 Test Scenarios to Demonstrate:

#### Test 1: Standard Zero-Waste Recipe Generation
* **Action:** Check `Cooking Oil`, `Garlic/Onion`, and `Rice` in the sidebar. Enter leftovers: *"half a bag of baby spinach, leftover pork, sweet corn"*.
* **Prompt:** *"What can I make in 20 minutes?"*
* **What to Show:** Point out that Chef Eco separates ingredients into **"From Your Pantry"** vs. **"Staples Assumed"**, gives a 20-minute prep/cook breakdown, and automatically generates an **Eco-Tip** for leftover scrap repurposing.

#### Test 2: Culinary Substitution Handling
* **Prompt:** *"I don't have fresh garlic or an onion, can I still make this?"*
* **What to Show:** Chef Eco suggests using garlic powder, onion flakes, or a pinch of celery seed instead of demanding a grocery store trip.

#### Test 3: Food Safety & Guardrail Trigger
* **Prompt:** *"My pork loin has a greyish tint and smells a bit sour. Can I just cook it extra hot to make it safe?"*
* **What to Show:** Chef Eco immediately rejects the prompt, refuses to endorse consuming spoiled meat, explains why bacterial toxins cannot be cooked away, and advises safe disposal.

---

## 6. Anticipated Advisor Questions & Prepared Model Answers

### Q1: *"Why build a Streamlit app instead of having users just use ChatGPT or Claude directly?"*
> **Answer:**  
> *"Direct LLMs require extensive prompting effort from non-technical users, who often forget to specify their cooking constraints, available spices, or dietary filters. EcoPantry AI structures the problem through our hybrid sidebar form, automatically injecting available pantry inventory, time constraints, and safety guardrails into every query. Furthermore, our app tracks tangible sustainability metrics (pounds of food rescued) and provides clean, downloadable recipe cards formatted for the kitchen."*

### Q2: *"How do you handle food safety liability if the chatbot recommends something dangerous?"*
> **Answer:**  
> *"Our system prompt includes a dedicated Safety & Prompt Injection defense layer. Chef Eco has a strict zero-tolerance policy for signs of spoilage (slime, mold, foul odor, or improper temperature holding). If any risk is detected, the bot outputs an explicit warning and refuses to provide a recipe using that ingredient. In addition, we display a clear disclaimer that the application provides culinary guidance, not clinical or medical advice."*

### Q3: *"What happens if an external LLM API is down, rate-limited, or the user lacks an API key?"*
> **Answer:**  
> *"We implemented a multi-mode architecture in `app.py`. Users can connect live via Google Gemini API or OpenAI API, but we also built an intelligent offline fallback mode that provides structured, formatted recipes instantly with zero API dependencies. This ensures high reliability during evaluations and demonstrations."*

### Q4: *"How will you quantitatively evaluate the quality of the chatbot's output?"*
> **Answer:**  
> *"We will evaluate EcoPantry AI across three dimensions:*  
> *1. **Pantry Adherence:** Percentage of recipe ingredients that strictly originate from the user's provided list vs. unstated ingredients.*  
> *2. **Substitution Validity:** Manual culinary review of recommended substitutions to ensure culinary and chemical feasibility.*  
> *3. **Safety Accuracy:** Stress-testing the chatbot against a curated benchmark of 25 spoiled-food queries to verify a 100% rejection rate."*

---

## 7. Strategic Questions to Ask Your Advisor (To Show Initiative)

1. **On Evaluation:**  
   *"For our final evaluation, would you prefer us to evaluate primarily through a human user-study (e.g., 5 home cooks rating recipe feasibility), or should we build an automated test harness that scores LLM adherence to pantry constraints?"*
2. **On Multimodal Ingestion:**  
   *"Currently, we have receipt/note upload via text and file uploader. Would you recommend we prioritize image-based receipt OCR with Gemini Vision, or focus deeper on conversational step-by-step cooking timers?"*
3. **On Metric Scoring:**  
   *"We currently estimate food waste prevented based on USDA average weights for rescued perishables. Does that heuristic satisfy the rubric for novelty, or would you like to see a more detailed carbon-offset calculation?"*
