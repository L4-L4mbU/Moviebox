from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    print("REQUEST:", request.method)

    if request.method == "POST":
        print("FORM DATA:", request.form)

        url = request.form.get("url")
        print("URL:", url)

        # existing code...

        filename = str(uuid.uuid4())

        output = os.path.join(
            DOWNLOAD_DIR,
            filename + ".%(ext)s"
        )

        options = {
            "format": "bestaudio/best",
            "outtmpl": output,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ]
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        mp3 = os.path.join(
            DOWNLOAD_DIR,
            filename + ".mp3"
        )

        return send_file(
            mp3,
            as_attachment=True,
            download_name="audio.mp3"
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
