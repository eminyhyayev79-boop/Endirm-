from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Bu hissə templates/index.html faylını ekrana gətirir
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "Link daxil edilməyib"}), 400

    try:
        # Videonu serverə yükləmədən birbaşa endirmə linkini tapırıq
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Videonun gizli, birbaşa yükləmə linkini alırıq
            direct_link = info.get('url')
            
        return jsonify({"download_url": direct_link})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render və digər serverlər üçün port tənzimləməsi
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
