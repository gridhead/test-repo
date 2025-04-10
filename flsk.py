import json

from flask import Flask, request

app = Flask(__name__)

"""
Comment
"""


@app.route("/webhook", methods=["POST"])
def webhook():
    text = ""
    text += "=== Incoming Webhook ===\n"

    # Print headers
    text += "\n--- Headers ---\n"
    for header, value in request.headers.items():
        text += f"{header}: {value}\n"

    # Print raw body

    text += "\n--- Raw Body ---\n"
    text += json.dumps(json.loads(request.get_data(as_text=True)), indent=2)

    # Print JSON body if possible
    try:
        json_data = request.get_json(force=False, silent=True)
        if json_data is not None:
            text += "\n--- JSON Body --- \n"
            text += json.dumps(json_data, indent=2)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")

    # Print form data if present
    if request.form:
        text += "\n--- Form Data ---\n"
        for key, value in request.form.items():
            text += f"{key}: {value}\n"

    name = f"github/{request.headers.get("X-GitHub-Event")}--{request.headers.get("X-GitHub-Delivery")}"
    with open(name, "w") as file:
        file.write(text)

    print(name)

    return "Webhook received", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # noqa: S104, S201
