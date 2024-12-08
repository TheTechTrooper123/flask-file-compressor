from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Komprimierung: Einfache Run-Length-Encoding (RLE)
def custom_compress(data):
    compressed = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            compressed.append(f"{count}{data[i - 1]}")
            count = 1
    compressed.append(f"{count}{data[-1]}")
    return ''.join(compressed)


# Dekomprimierung
def custom_decompress(data):
    decompressed = []
    i = 0
    while i < len(data):
        count = ""
        while data[i].isdigit():
            count += data[i]
            i += 1
        decompressed.append(data[i] * int(count))
        i += 1
    return ''.join(decompressed)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template_string(
        """
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Kanit&display=swap');
                body {
                    font-family: Kanit;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(to top right, #D74177, #FFE98A);
                }

                h2 {
                    color: black;
                    font-size: 24px;
                }

                form {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    width: 400px;
                    margin-left: auto;
                    margin-right: auto;
                }

                input[type="file"] {
                    margin-bottom: 10px;
                    padding: 10px;
                    width: 100%;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }

                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                }

                button:hover {
                    background-color: #45a049;
                }

                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    text-align: center;
                }

                .notice {
                    color: #f44336;
                    font-size: 14px;
                }

            </style>
        </head>
        <body>
            <div class="container">
                <h2>Datei hochladen und komprimieren</h2>
                <form method="POST" action="/compress" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">Komprimieren</button>
                </form>
                <br>
                <h2>Komprimierte Datei hochladen und entkomprimieren</h2>
                <form method="POST" action="/decompress" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">Entkomprimieren</button>
                </form>
            </div>
        </body>
        </html>
        """
    )


@app.route("/compress", methods=["POST"])
def compress():
    if "file" not in request.files:
        return "Keine Datei hochgeladen.", 400

    file = request.files["file"]
    if file.filename == "":
        return "Keine Datei ausgewählt.", 400

    # Datei lesen und komprimieren
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    compressed_path = os.path.join(UPLOAD_FOLDER, file.filename + ".compressed")
    file.save(input_path)

    with open(input_path, "r") as f:
        original_data = f.read()
    compressed_data = custom_compress(original_data)

    with open(compressed_path, "w") as f:
        f.write(compressed_data)

    return send_file(compressed_path, as_attachment=True)


@app.route("/decompress", methods=["POST"])
def decompress():
    if "file" not in request.files:
        return "Keine Datei hochgeladen.", 400

    file = request.files["file"]
    if file.filename == "":
        return "Keine Datei ausgewählt.", 400

    # Datei lesen und dekomprimieren
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    decompressed_path = os.path.join(UPLOAD_FOLDER, file.filename + ".decompressed")
    file.save(input_path)

    with open(input_path, "r") as f:
        compressed_data = f.read()
    decompressed_data = custom_decompress(compressed_data)

    with open(decompressed_path, "w") as f:
        f.write(decompressed_data)

    return send_file(decompressed_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
