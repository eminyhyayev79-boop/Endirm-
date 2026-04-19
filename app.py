from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Endirmə.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "Link yoxdur"}), 400

    # Bu API 4 platformanın hamısını (və daha çoxunu) dəstəkləyir
    # Cobalt API istifadə edirik - pulsuz və güclüdür
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "url": url,
        "vQuality": "720"  # Video keyfiyyəti
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        res_data = response.json()
        
        # Əgər video tapılarsa
        if res_data.get('status') == 'stream' or res_data.get('status') == 'redirect':
            video_link = res_data.get('url')
            return jsonify({"download_url": video_link})
        elif res_data.get('status') == 'picker':
            # Bəzən çoxlu seçim verir (məsələn Instagram postunda bir neçə şəkil/video)
            video_link = res_data.get('picker')[0].get('url')
            return jsonify({"download_url": video_link})
        else:
            return jsonify({"error": "Video tapılmadı və ya sayt blokladı"}), 400
            
    except Exception as e:
        return jsonify({"error": "Serverlə əlaqə kəsildi"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
