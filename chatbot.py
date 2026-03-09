def medical_chatbot(question):

    question = question.lower()

    if "fever" in question:
        return "Drink plenty of fluids and take paracetamol if necessary."

    elif "diabetes" in question:
        return "Maintain a low sugar diet and regular exercise."

    elif "bp" in question or "blood pressure" in question:
        return "Reduce salt intake and monitor BP regularly."

    else:
        return "Please consult a doctor for accurate medical advice."