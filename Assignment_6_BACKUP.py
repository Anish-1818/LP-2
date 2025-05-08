# --- Knowledge Base ---
RULES = [
    {
        "conditions": {"fever", "cough", "fatigue", "body_aches"},
        "conclusion": "Potential Flu. Consult a doctor.",
        "explanation": "Fever, cough, fatigue, and body aches indicate possible Influenza."
    },
    {
        "conditions": {"fever", "cough", "sore_throat"},
        "conclusion": "Possible Cold or Strep Throat.",
        "explanation": "Fever, cough, and sore throat could be common cold or strep throat."
    },
    {
        "conditions": {"cough", "runny_nose", "sneezing"},
        "conclusion": "Likely Common Cold.",
        "explanation": "These symptoms without fever usually indicate a cold."
    },
    {
        "conditions": {"fever", "shortness_of_breath", "chest_pain"},
        "conclusion": "SERIOUS: Possible Pneumonia. Seek help immediately.",
        "explanation": "Shortness of breath and chest pain with fever can be critical."
    },
    {
        "conditions": {"sore_throat", "difficulty_swallowing"},
        "conclusion": "Possible Strep or Tonsillitis.",
        "explanation": "Sore throat and trouble swallowing may suggest infection."
    },
    {
        "conditions": {"headache", "fatigue"},
        "conclusion": "General Symptoms. Rest and hydrate.",
        "explanation": "These symptoms may stem from stress, dehydration, or viral illness."
    },
    {
        "conditions": {"fever"},
        "conclusion": "Monitor Fever.",
        "explanation": "Could be early infection. Monitor and consult if persistent."
    }
]

# --- Inference Engine ---
def forward_chaining(rules, facts):
    conclusions = []
    seen = set()
    for rule in rules:
        if rule["conditions"].issubset(facts) and rule["conclusion"] not in seen:
            conclusions.append(rule)
            seen.add(rule["conclusion"])
    return conclusions


def get_user_facts():
    print("\n--- Medical Expert System ---")
    facts = set()
    all_conditions = set()
    
    for rule in RULES:
        for symptom in rule["conditions"]:
            all_conditions.add(symptom)

    for symptom in sorted(all_conditions):
        if input(f"Do you have '{symptom.replace('_', ' ')}'? (y/n): ").strip().lower().startswith('y'):
            facts.add(symptom)

    return facts



def main():
    facts = get_user_facts()

    if not facts:
        print("\nNo symptoms given. Unable to assess.")
        return

    print(f"\nYou reported: {', '.join(f.replace('_', ' ') for f in sorted(facts))}")
    conclusions = forward_chaining(RULES, facts)

    if conclusions:
        print("\n--- Assessment ---")
        for i, c in enumerate(conclusions, 1):
            print(f"{i}. {c['conclusion']}\n   {c['explanation']}\n")
    else:
        print("\nNo specific match. Please consult a doctor if symptoms persist.")

if __name__ == "__main__":
    main()