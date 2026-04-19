from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

# Burada Flask-a deyirik ki, HTML faylları qovluğun içində deyil, birbaşa çöldədir
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    # Faylın adını tam olaraq səndə olduğu kimi bura yazdıq
    return render_template('Endirmə.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "Link yoxdur"}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            
        return jsonify({"download_url": direct_link})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
