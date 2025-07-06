# fastapi_app/services/graph_service.py
import matplotlib.pyplot as plt
import io
import base64

def create_hrv_graph(hrv_score: float) -> str:
    print("그래프를 생성합니다...")
    fig, ax = plt.subplots()
    color = 'lightcoral' if hrv_score < 60 else 'skyblue'
    ax.bar(['Your Score'], [hrv_score], color=color)
    ax.set_ylim(0, 100)
    ax.set_ylabel('HRV Score')
    ax.set_title('HRV Analysis Result')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{base64_image}"
