from flask import Flask, render_template, request, jsonify
import os
import random
import pdfplumber
import pytesseract
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -----------------------------
# Helper Functions
# -----------------------------

def read_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def read_image(filepath):
    img = cv2.imread(filepath)
    text = pytesseract.image_to_string(img)
    return text


def analyze_report_text(text):

    results = []

    # Simple rule-based detection
    if "glucose" in text.lower() or "sugar" in text.lower():
        results.append({
            "test": "Blood Sugar",
            "value": "Detected",
            "status": "Possible Diabetes",
            "doctor": "Endocrinologist",
            "hospital": "Apollo Hospital",
            "location": "Chennai"
        })

    if "hemoglobin" in text.lower():
        results.append({
            "test": "Hemoglobin",
            "value": "Detected",
            "status": "Possible Anemia",
            "doctor": "General Physician",
            "hospital": "Fortis Hospital",
            "location": "Chennai"
        })

    if "cholesterol" in text.lower():
        results.append({
            "test": "Cholesterol",
            "value": "Detected",
            "status": "High Cholesterol Risk",
            "doctor": "Cardiologist",
            "hospital": "MIOT Hospital",
            "location": "Chennai"
        })

    if len(results) == 0:
        results.append({
            "test": "General Health",
            "value": "Normal",
            "status": "Healthy",
            "doctor": "General Physician",
            "hospital": "Apollo Clinic",
            "location": "Chennai"
        })

    return results


def generate_diet_plan(results):

    diet = []

    for r in results:

        if "diabetes" in r["status"].lower():
            diet += [
                "Avoid sugar and sweets",
                "Eat whole grains",
                "Include vegetables like broccoli and spinach",
                "Walk 30 minutes daily"
            ]

        elif "anemia" in r["status"].lower():
            diet += [
                "Eat iron rich foods like spinach",
                "Include dates and pomegranate",
                "Eat more protein foods",
                "Drink plenty of water"
            ]

        elif "cholesterol" in r["status"].lower():
            diet += [
                "Avoid oily and fried food",
                "Eat oats and nuts",
                "Exercise regularly",
                "Eat fruits daily"
            ]

    if len(diet) == 0:
        diet = [
            "Maintain balanced diet",
            "Drink 2-3L water daily",
            "Exercise regularly"
        ]

    return list(set(diet))


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["report"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    text = ""

    if file.filename.endswith(".pdf"):
        text = read_pdf(filepath)

    elif file.filename.endswith(".png") or file.filename.endswith(".jpg"):
        text = read_image(filepath)

    results = analyze_report_text(text)

    diet_plan = generate_diet_plan(results)

    health_score = random.randint(65, 95)

    return jsonify({
        "results": results,
        "diet_plan": diet_plan,
        "health_score": health_score
    })


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    question = data["question"].lower()

    if "diabetes" in question:
        answer = "Diabetes is a condition where blood sugar becomes high. Maintain healthy diet and exercise."

    elif "cholesterol" in question:
        answer = "High cholesterol increases heart risk. Avoid oily foods and exercise regularly."

    elif "anemia" in question:
        answer = "Anemia occurs due to low hemoglobin. Eat iron rich foods."

    elif "diet" in question:
        answer = "Balanced diet includes vegetables, fruits, proteins and whole grains."

    else:
        answer = "Please consult a doctor for accurate diagnosis."

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)