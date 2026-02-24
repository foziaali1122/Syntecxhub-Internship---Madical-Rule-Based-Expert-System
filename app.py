import streamlit as st

# ==========================================
# FORWARD CHAINING ENGINE
# ==========================================
def forward_chaining(facts, rules):
    reasoning = []
    new_fact = True

    while new_fact:
        new_fact = False
        for rule in rules:
            if rule["if"].issubset(facts) and rule["then"] not in facts:
                facts.add(rule["then"])
                reasoning.append(
                    f"Because ({', '.join(rule['if'])}) → I diagnosed **{rule['then']}**"
                )
                new_fact = True

    return facts, reasoning


# ==========================================
# RULE BASE (Doctor Knowledge)
# ==========================================
rules = [

    {"if": {"fever", "cough"}, "then": "flu"},
    {"if": {"flu", "body pain"}, "then": "severe flu"},
    {"if": {"sore throat", "fever"}, "then": "throat infection"},
    {"if": {"fatigue", "body pain"}, "then": "viral infection"},
    {"if": {"cough", "sore throat"}, "then": "upper respiratory infection"},
    {"if": {"body pain"}, "then": "muscle strain"},
    {"if": {"severe flu"}, "then": "doctor consultation"},
    {"if": {"upper respiratory infection"}, "then": "home care advised"}
]


# ==========================================
# DOCTOR KNOWLEDGE BASE
# ==========================================
doctor_knowledge = {

    "flu": {
        "reason": "Your symptoms indicate a viral respiratory infection.",
        "care": "Take rest, drink warm fluids, and use paracetamol for fever.",
        "warning": "If fever lasts more than 3 days, consult a doctor."
    },

    "severe flu": {
        "reason": "Combination of flu and body pain suggests worsening condition.",
        "care": "Immediate medical consultation recommended.",
        "warning": "Do not ignore prolonged weakness."
    },

    "throat infection": {
        "reason": "Sore throat with fever indicates throat infection.",
        "care": "Warm salt water gargles and hydration.",
        "warning": "Seek medical help if pain increases."
    },

    "viral infection": {
        "reason": "Fatigue and body pain suggest viral infection.",
        "care": "Rest and proper hydration.",
        "warning": "Avoid antibiotics unless prescribed."
    },

    "upper respiratory infection": {
        "reason": "Cough and sore throat suggest upper respiratory tract infection.",
        "care": "Steam inhalation and warm fluids.",
        "warning": "Consult doctor if breathing difficulty occurs."
    },

    "muscle strain": {
        "reason": "Body pain alone may indicate muscle fatigue or strain.",
        "care": "Rest and light stretching.",
        "warning": "Avoid heavy physical activity."
    },

    "doctor consultation": {
        "reason": "Symptoms indicate serious condition.",
        "care": "Visit a certified medical professional immediately.",
        "warning": "Do not delay treatment."
    },

    "home care advised": {
        "reason": "Condition appears mild.",
        "care": "Rest and monitor symptoms.",
        "warning": "Seek medical help if symptoms worsen."
    }
}


# ==========================================
# STREAMLIT UI
# ==========================================
st.set_page_config(page_title="Medical Expert Doctor System", page_icon="🩺")

st.title("🩺 Medical Rule-Based Expert Doctor System")
st.write("Select your symptoms and get expert medical diagnosis with reasoning.")

symptoms_list = [
    "fever",
    "cough",
    "sore throat",
    "headache",
    "body pain",
    "fatigue"
]

selected_symptoms = st.multiselect(
    "Select Symptoms:",
    symptoms_list
)

if st.button("Analyze Symptoms"):

    if not selected_symptoms:
        st.warning("Doctor says: Please select at least one symptom for diagnosis.")
    else:
        facts = set(selected_symptoms)
        final_facts, reasoning_path = forward_chaining(facts, rules)

        st.subheader("Reasoning Path (How Doctor Diagnosed)")

        if reasoning_path:
            for step in reasoning_path:
                st.write("•", step)
        else:
            st.write("Based on provided symptoms, no major disease rule triggered.")
            st.write("However, general medical guidance is provided below.")

        st.subheader("🩺 Doctor Diagnosis & Recommendation")

        disease_found = False

        for fact in final_facts:
            if fact in doctor_knowledge:
                disease_found = True
                info = doctor_knowledge[fact]

                st.markdown(f"### 🔹 {fact.upper()}")
                st.write("**Why this happened:**", info["reason"])
                st.write("**What you should do:**", info["care"])
                st.warning(info["warning"])

        if not disease_found:
            st.markdown("### 🔹 GENERAL MEDICAL ADVICE")
            st.write("Symptoms are mild or incomplete for specific diagnosis.")
            st.write("Maintain rest, hydration, and monitor condition.")
            st.warning("Consult a doctor if symptoms persist or worsen.")