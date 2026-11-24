# EcoPantry AI: Zero-Waste Recipe & Culinary Coach 🌱

An interactive, multi-modal AI chatbot application built with **Streamlit** to help home cooks turn available fridge leftovers into delicious, cost-effective meals while actively reducing household food waste.

---

## 🌟 Key Application Features

1. **Dual-Input Pantry Management:**
   - Interactive sidebar checklist for standard household staples (`st.checkbox`).
   - Free-form text input for perishable fridge leftovers (`st.text_input`).
   - Document & grocery note ingestion (.txt) to automatically parse items (`st.file_uploader`).

2. **Waste-First Dynamic Recipe Engine:**
   - Prioritizes highly perishable items to prevent food spoilage.
   - Respects user-defined cooking duration (`st.slider`) and dietary restrictions (`st.selectbox`).

3. **Smart Kitchen Substitutions:**
   - Suggests chemistry-safe culinary alternatives when minor ingredients are missing.

4. **Interactive Cooking Utilities:**
   - **Kitchen Step Timer:** An interactive countdown timer widget with progress tracking right in the interface.
   - **Quick Action Prompts:** Clickable buttons for 1-click recipes, veggie rescues, substitutions, and safety checks.

5. **Live Sustainability Scorecard:**
   - Tracks rescued food weight (lbs), estimated grocery money saved ($), and CO₂ emissions avoided (kg) using real-time metrics (`st.metric`).

6. **Safety & Anti-Jailbreak Guardrails:**
   - Detects spoiled, moldy, or foul-smelling items and issues strict food-safety warnings.
   - Resistant to prompt injection attacks and out-of-domain queries.

7. **Export & Session Management:**
   - One-click export of complete recipes and chat transcripts to Markdown (`st.download_button`).

---

## 🚀 How to Run the App

### 1. Launch the Streamlit Interface
Open your terminal in this directory and execute:

```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

### 2. Choose Your Inference Engine
* **Smart Offline Engine (Default):** Runs immediately with **zero API key required**. Great for grading, offline demos, and testing!
* **Google Gemini API / OpenAI API:** Enter your API key directly in the sidebar to enable live Large Language Model inference.

---

## 🧪 Automated Testing

EcoPantry AI includes an automated unit and integration test suite covering safety guardrails, output formatting, substitution logic, and canary attention checks.

To execute the test suite:

```bash
python test_app.py
```

*Expected output: `Ran 5 tests ... OK`*
