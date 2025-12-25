from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

EMAIL_RECEIVER = "dakecivil@gmail.com"     # là où tu veux recevoir les messages
EMAIL_SENDER = "dakecivil@gmail.com"       # le mail qui envoie
EMAIL_PASSWORD = "kognveozhnbglole"      # mot de passe d’application Gmail

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    nom = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not nom or not email or not message:
        return jsonify({"error": "Champs manquants"}), 400

    try:
        msg = EmailMessage()
        msg["Subject"] = "📩 Nouveau message - DAKE CIVIL"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content(
            f"Nom : {nom}\n"
            f"Email : {email}\n\n"
            f"Message :\n{message}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
   