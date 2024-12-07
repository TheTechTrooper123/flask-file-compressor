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
                    background: linear-gradient(to top right, #ECE9E0, #3C3635);
                }

                h2 {
                    color: #EBEBEB;
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

                button {
                    background-color: #45A29F;
                    color: #66FCF1;
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
                
                
                
                
                
                
                
                .custum-file-upload {
                  display: flex;
                  flex-direction: column;
                  align-items: space-between;
                  gap: 20px;
                  cursor: pointer;
                  align-items: center;
                  justify-content: center;
                  border: 2px dashed #e8e8e8;
                  background-color: #212121;
                  padding: 1.5rem;
                  border-radius: 10px;
                  box-shadow: 0px 48px 35px -48px #e8e8e8;
                }
                
                .custum-file-upload .icon {
                  display: flex;
                  align-items: center;
                  justify-content: center;
                }
                
                .custum-file-upload .icon svg {
                  height: 80px;
                  fill: #e8e8e8;
                }
                
                .custum-file-upload .text {
                  display: flex;
                  align-items: center;
                  justify-content: center;
                }
                
                .custum-file-upload .text span {
                  font-weight: 400;
                  color: #e8e8e8;
                }
                
                .custum-file-upload input {
                  display: none;
                }
                
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Datei hochladen und komprimieren</h2>
                <form method="POST" action="/compress" enctype="multipart/form-data">
                    <label for="file" class="custum-file-upload">
                    <div class="icon">
                    <svg viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M10 1C9.73478 1 9.48043 1.10536 9.29289 1.29289L3.29289 7.29289C3.10536 7.48043 3 7.73478 3 8V20C3 21.6569 4.34315 23 6 23H7C7.55228 23 8 22.5523 8 22C8 21.4477 7.55228 21 7 21H6C5.44772 21 5 20.5523 5 20V9H10C10.5523 9 11 8.55228 11 8V3H18C18.5523 3 19 3.44772 19 4V9C19 9.55228 19.4477 10 20 10C20.5523 10 21 9.55228 21 9V4C21 2.34315 19.6569 1 18 1H10ZM9 7H6.41421L9 4.41421V7ZM14 15.5C14 14.1193 15.1193 13 16.5 13C17.8807 13 19 14.1193 19 15.5V16V17H20C21.1046 17 22 17.8954 22 19C22 20.1046 21.1046 21 20 21H13C11.8954 21 11 20.1046 11 19C11 17.8954 11.8954 17 13 17H14V16V15.5ZM16.5 11C14.142 11 12.2076 12.8136 12.0156 15.122C10.2825 15.5606 9 17.1305 9 19C9 21.2091 10.7909 23 13 23H20C22.2091 23 24 21.2091 24 19C24 17.1305 22.7175 15.5606 20.9844 15.122C20.7924 12.8136 18.858 11 16.5 11Z" fill=""></path> </g></svg>
                    </div>
                    <div class="text">
                       <span>Click to upload file</span>
                       </div>
                       <input type="file" name="file" id="file" required>
                    </label>
                    <button type="submit">Komprimieren</button>
                </form>
                <br>
                <h2>Komprimierte Datei hochladen und entkomprimieren</h2>
                <form method="POST" action="/decompress" enctype="multipart/form-data">
                    <label for="file" class="custum-file-upload">
                    <div class="icon">
                    <svg viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M10 1C9.73478 1 9.48043 1.10536 9.29289 1.29289L3.29289 7.29289C3.10536 7.48043 3 7.73478 3 8V20C3 21.6569 4.34315 23 6 23H7C7.55228 23 8 22.5523 8 22C8 21.4477 7.55228 21 7 21H6C5.44772 21 5 20.5523 5 20V9H10C10.5523 9 11 8.55228 11 8V3H18C18.5523 3 19 3.44772 19 4V9C19 9.55228 19.4477 10 20 10C20.5523 10 21 9.55228 21 9V4C21 2.34315 19.6569 1 18 1H10ZM9 7H6.41421L9 4.41421V7ZM14 15.5C14 14.1193 15.1193 13 16.5 13C17.8807 13 19 14.1193 19 15.5V16V17H20C21.1046 17 22 17.8954 22 19C22 20.1046 21.1046 21 20 21H13C11.8954 21 11 20.1046 11 19C11 17.8954 11.8954 17 13 17H14V16V15.5ZM16.5 11C14.142 11 12.2076 12.8136 12.0156 15.122C10.2825 15.5606 9 17.1305 9 19C9 21.2091 10.7909 23 13 23H20C22.2091 23 24 21.2091 24 19C24 17.1305 22.7175 15.5606 20.9844 15.122C20.7924 12.8136 18.858 11 16.5 11Z" fill=""></path> </g></svg>
                    </div>
                    <div class="text">
                       <span>Click to upload file</span>
                       </div>
                       <input type="file" name="file" id="file" required>
                    </label>
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