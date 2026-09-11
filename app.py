import os
from flask import Flask, render_template, request, jsonify, Response
from src.data_loader import load_data
from src.processor import clean_conflict_data, aggregate_deaths
from src.analysis import analyze_by_region, generate_conflict_map
from src.ai_assistant import WarIntelligenceAI
from src.war_data import WAR_METADATA

app = Flask(__name__)

# Initialize dataset and AI Assistant
try:
    df_raw = load_data()
    df_cleaned = clean_conflict_data(df_raw)
    df_processed = aggregate_deaths(df_cleaned)
    ai_assistant = WarIntelligenceAI(df_processed)
except Exception as e:
    df_processed = None
    ai_assistant = WarIntelligenceAI()
    print(f"Warning: Failed to auto-load dataset: {e}")

@app.route('/')
def index():
    if df_processed is not None:
        total_events = len(df_processed)
        total_fatalities = int(df_processed['total_deaths'].sum()) if 'total_deaths' in df_processed.columns else 0
        total_regions = df_processed['region'].nunique() if 'region' in df_processed.columns else 0
        total_countries = df_processed['country'].nunique() if 'country' in df_processed.columns else 0
        regional_stats = analyze_by_region(df_processed).to_dict(orient='records')
    else:
        total_events = total_fatalities = total_regions = total_countries = 0
        regional_stats = []

    return render_template(
        'index.html',
        total_events=total_events,
        total_fatalities=total_fatalities,
        total_regions=total_regions,
        total_countries=total_countries,
        regional_stats=regional_stats,
        leaders=WAR_METADATA
    )

@app.route('/map')
def get_map():
    try:
        if df_processed is not None and len(df_processed) > 0:
            folium_map = generate_conflict_map(df_processed, output_path=None)
            map_html = folium_map.get_root().render()
            return Response(map_html, mimetype='text/html')
        else:
            return "<div style='color:white; background:#121418; padding:20px; font-family:sans-serif;'>Conflict map data currently unavailable.</div>", 200
    except Exception as e:
        print(f"Error rendering conflict map: {e}")
        return f"<div style='color:#ff6b6b; background:#121418; padding:20px; font-family:sans-serif;'>Unable to render interactive map: {e}</div>", 500

@app.route('/api/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json(silent=True) or {}
        question = data.get('question', '') if isinstance(data, dict) else ''
        response_text = ai_assistant.ask(question)
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error handling AI ask request: {e}")
        return jsonify({'response': f"AI processing error: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
