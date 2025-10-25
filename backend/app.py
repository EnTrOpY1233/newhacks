from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from elevenlabs import generate, save
import requests
from io import BytesIO

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置 API 密钥
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# 配置 Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    logger.warning("GEMINI_API_KEY not found in environment variables")

# 创建临时文件夹
AUDIO_FOLDER = 'temp_audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'gemini_configured': bool(GEMINI_API_KEY),
        'elevenlabs_configured': bool(ELEVENLABS_API_KEY),
        'maps_configured': bool(GOOGLE_MAPS_API_KEY)
    })


@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary():
    """生成旅行行程"""
    try:
        data = request.get_json()
        city = data.get('city', '')
        days = data.get('days', 3)

        if not city:
            return jsonify({'error': '请提供城市名称'}), 400

        if not GEMINI_API_KEY:
            # 返回示例数据用于测试
            return jsonify({
                'itinerary': get_sample_itinerary(city, days)
            })

        # 构建提示词
        prompt = f"""
请为{city}创建一个{days}天的旅游行程计划。

要求：
1. 每天推荐3-5个景点
2. 包含景点名称、简介、建议停留时间、类型（历史、自然、美食等）
3. 给出实用的旅行小贴士

请以JSON格式返回，结构如下：
{{
    "city": "{city}",
    "days": {days},
    "schedule": [
        {{
            "day": 1,
            "places": [
                {{
                    "name": "景点名称",
                    "description": "详细介绍（100-150字）",
                    "duration": "建议停留时间",
                    "category": "类型"
                }}
            ]
        }}
    ],
    "tips": ["小贴士1", "小贴士2", "小贴士3"]
}}

只返回JSON，不要添加任何其他文字。
"""

        # 调用 Gemini API
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # 清理响应文本
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # 解析JSON
        itinerary = json.loads(response_text)

        # 扁平化景点列表用于地图显示
        all_places = []
        for day in itinerary.get('schedule', []):
            all_places.extend(day.get('places', []))
        
        itinerary['places'] = all_places

        logger.info(f"Successfully generated itinerary for {city}")
        return jsonify({'itinerary': itinerary})

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        # 返回示例数据
        return jsonify({
            'itinerary': get_sample_itinerary(city, days)
        })
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        return jsonify({'error': f'生成行程失败: {str(e)}'}), 500


@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """生成景点语音讲解"""
    try:
        data = request.get_json()
        place_name = data.get('place_name', '')
        description = data.get('description', '')

        if not place_name:
            return jsonify({'error': '请提供景点名称'}), 400

        if not ELEVENLABS_API_KEY:
            # 返回示例音频URL
            return jsonify({
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'message': 'ElevenLabs API未配置，返回示例音频'
            })

        # 生成讲解文本
        text = f"{place_name}。{description}"

        # 使用 ElevenLabs 生成语音
        audio = generate(
            text=text,
            voice="Bella",  # 可以选择不同的声音
            api_key=ELEVENLABS_API_KEY
        )

        # 保存音频文件
        audio_filename = f"{place_name.replace(' ', '_')}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        save(audio, audio_path)

        logger.info(f"Successfully generated audio for {place_name}")
        
        # 返回音频URL
        return jsonify({
            'audio_url': f'/api/audio/{audio_filename}'
        })

    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return jsonify({'error': f'生成语音失败: {str(e)}'}), 500


@app.route('/api/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """提供音频文件"""
    try:
        audio_path = os.path.join(AUDIO_FOLDER, filename)
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f"Error serving audio: {str(e)}")
        return jsonify({'error': '音频文件不存在'}), 404


@app.route('/api/generate-poster', methods=['POST'])
def generate_poster():
    """生成目的地海报（可选功能）"""
    try:
        data = request.get_json()
        city = data.get('city', '')

        if not city:
            return jsonify({'error': '请提供城市名称'}), 400

        # 使用 Gemini 或其他 API 生成图片
        # 这里返回占位符
        poster_url = f"https://source.unsplash.com/800x600/?{city},travel"

        return jsonify({
            'poster_url': poster_url
        })

    except Exception as e:
        logger.error(f"Error generating poster: {str(e)}")
        return jsonify({'error': f'生成海报失败: {str(e)}'}), 500


def get_sample_itinerary(city, days):
    """返回示例行程数据"""
    return {
        "city": city,
        "days": days,
        "schedule": [
            {
                "day": 1,
                "places": [
                    {
                        "name": f"{city}中心广场",
                        "description": f"位于{city}市中心的标志性广场，是游客必访之地。这里汇集了城市的历史与现代文化，周围环绕着重要的历史建筑和现代商业区。广场常年举办各类文化活动和节日庆典。",
                        "duration": "1-2小时",
                        "category": "历史文化"
                    },
                    {
                        "name": f"{city}博物馆",
                        "description": f"收藏了丰富的历史文物和艺术珍品，展示了{city}及周边地区的历史发展和文化变迁。博物馆建筑本身也是一件艺术品，结合了传统与现代设计元素。",
                        "duration": "2-3小时",
                        "category": "文化教育"
                    },
                    {
                        "name": f"{city}老城区",
                        "description": f"保存完好的历史街区，漫步其中可以感受到{city}的传统风貌。狭窄的街道两旁是特色小店、传统餐厅和咖啡馆，是体验当地生活的好去处。",
                        "duration": "2-3小时",
                        "category": "历史文化"
                    }
                ]
            },
            {
                "day": 2,
                "places": [
                    {
                        "name": f"{city}公园",
                        "description": f"{city}最大的城市公园，绿树成荫，湖光山色。是市民休闲娱乐的热门场所，也是观赏城市天际线的最佳地点之一。春秋季节景色尤为迷人。",
                        "duration": "2-3小时",
                        "category": "自然风光"
                    },
                    {
                        "name": f"{city}美食街",
                        "description": f"汇集了{city}各种特色美食的街区，从传统小吃到现代餐饮应有尽有。夜晚的美食街灯火通明，热闹非凡，是品尝地道美食的最佳选择。",
                        "duration": "2-3小时",
                        "category": "美食购物"
                    },
                    {
                        "name": f"{city}观景台",
                        "description": f"位于城市制高点的观景平台，可以360度俯瞰整个{city}的壮丽景色。日落时分来访可以欣赏到最美的城市夜景。",
                        "duration": "1-2小时",
                        "category": "观光休闲"
                    }
                ]
            },
            {
                "day": 3,
                "places": [
                    {
                        "name": f"{city}市场",
                        "description": f"当地最有特色的传统市场，售卖各种新鲜食材、手工艺品和纪念品。在这里可以近距离接触当地人的日常生活，是购买特色礼品的好地方。",
                        "duration": "1-2小时",
                        "category": "购物体验"
                    },
                    {
                        "name": f"{city}艺术区",
                        "description": f"充满创意的艺术街区，遍布画廊、工作室、独立书店和咖啡馆。墙面上的涂鸦艺术和街头表演为这里增添了独特的文化气息。",
                        "duration": "2-3小时",
                        "category": "艺术文化"
                    }
                ]
            }
        ],
        "tips": [
            f"提前查看{city}的天气预报，准备合适的衣物",
            "建议购买当地的交通卡，可以节省不少费用",
            "尊重当地文化和习俗，注意言行举止",
            "保管好个人财物，注意人身安全",
            "可以下载翻译软件和离线地图以备不时之需"
        ],
        "places": []  # 将在后续填充
    }


if __name__ == '__main__':
    logger.info("Starting TripTeller Backend Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

