from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Endirmə.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "Link yoxdur"}), 400

    try:
        # TikTok üçün xüsusi və sürətli API (TikWM)
        # Bu API TikTok-un bloklarını özü keçir
        api_url = f"https://www.tikwm.com/api/?url={video_url}"
        response = requests.get(api_url).json()
        
        if response.get('code') == 0:
            # TikTok videosunun birbaşa (watermark-sız) linki
            direct_link = response['data']['play']
            return jsonify({"download_url": direct_link})
        else:
            return jsonify({"error": "Video tapılmadı və ya link səhvdir"}), 400
            
    except Exception as e:
        return jsonify({"error": "Sistemdə xəta baş verdi"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
