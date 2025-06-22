# 确保文件以 UTF-8 编码保存
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def home():
    # 准备中文内容
    html_content = "<h1>你好，uv 的世界！</h1>"
    html_content += "<p>这个 Demo 演示了如何使用 <b>uv venv</b> 来管理项目环境。</p>"
    html_content += "<p>这是一个纯中文的网页内容。</p>"

    # 使用 Response 对象并明确指定 UTF-8 编码，确保浏览器正确解析
    return Response(html_content, mimetype='text/html; charset=utf-8')

if __name__ == '__main__':
    print("服务已启动，请在浏览器中访问 http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)