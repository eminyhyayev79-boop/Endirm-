from flask import Flask, render_template, request, jsonify
import yt_dlp
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

    # Bura diqqət! YouTube bloklarını keçmək üçün xüsusi başlıqlar (headers) əlavə etdik
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Bəzi saytlarda 'url' yoxdur, 'formats' içindən götürürük
            direct_link = info.get('url') or info.get('formats')[0].get('url')
            
        return jsonify({"download_url": direct_link})
        
    except Exception as e:
        # Xətanın nə olduğunu görmək üçün terminala yazdırırıq
        print(f"Xəta baş verdi: {e}")
        return jsonify({"error": "Video tapılmadı və ya sayt blokladı"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
