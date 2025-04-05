import os

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>抽象小站 | 代码游乐场</title>
    <style>
        :root {{
            --main-color: #ff69b4;
            --secondary-color: #40e0d0;
            --bg-gradient: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        }}

        body {{
            font-family: 'Comic Sans MS', cursive;
            background: var(--bg-gradient);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            padding: 20px;
        }}

        .code-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            transform-style: preserve-3d;
            transition: all 0.3s ease;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            border: 3px dashed var(--main-color);
        }}

        .code-card:hover {{
            transform: rotate(2deg) translateY(-5px);
            background: rgba(255, 255, 255, 1);
        }}

        .file-info {{
            background: #fff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 2px solid var(--secondary-color);
            position: relative;
        }}

        .file-info::before {{
            content: "📁";
            position: absolute;
            left: -15px;
            top: -15px;
            font-size: 24px;
            transform: rotate(-15deg);
        }}

        .code-preview {{
            font-family: 'Courier New', monospace;
            background: #1e1e1e;
            color: #fff;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            position: relative;
            white-space: pre-wrap;
        }}

        .tag {{
            display: inline-block;
            background: var(--main-color);
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.8em;
            transform: skewX(-10deg);
        }}

        .danger-level {{
            width: 100%;
            height: 10px;
            background: #ffd700;
            border-radius: 5px;
            margin: 10px 0;
            overflow: hidden;
        }}

        .danger-fill {{
            width: 70%;
            height: 100%;
            background: #ff4500;
            transition: width 0.3s ease;
        }}

        .emoji-rating {{
            font-size: 24px;
            margin: 10px 0;
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        .floating-icon {{
            animation: float 3s ease-in-out infinite;
        }}
    </style>
</head>
<body>
    <div class="container">
{cards_content}
    </div>

    <div style="position: fixed; bottom: 20px; right: 20px;" class="floating-icon">
        📌 抽象警告：本站代码仅供娱乐，切勿认真对待！
    </div>
</body>
</html>'''

def get_valid_input(prompt, validation_func, error_msg):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(error_msg)

def create_card():
    print("\n" + "="*30)
    print(" 创建新代码卡片 ".center(30, "="))
    
    title = input("请输入标题: ").strip()
    
    danger = get_valid_input(
        "请输入危险等级 (0-100): ",
        lambda x: x.isdigit() and 0 <= int(x) <= 100,
        "请输入0到100之间的整数"
    )
    
    tags = []
    while True:
        tag_input = input("请输入标签（多个标签用逗号分隔）: ").strip()
        if tag_input:
            tags = [t.strip() for t in tag_input.split(",") if t.strip()]
            if tags:
                break
        print("至少需要输入一个标签")
    
    emoji = get_valid_input(
        "请输入Emoji评分: ",
        lambda x: len(x) > 0,
        "评分不能为空"
    )
    
    print("请输入代码内容（输入空行结束）:")
    code_lines = []
    while True:
        line = input()
        if line.strip() == "" and len(code_lines) > 0:
            break
        code_lines.append(line)
    
    return {
        "title": title,
        "danger": danger,
        "tags": tags,
        "emoji": emoji,
        "code": "\n".join(code_lines)
    }

def generate_html(cards):
    cards_content = []
    for card in cards:
        tags_html = "\n".join([f'        <span class="tag">{tag}</span>' for tag in card["tags"]])
        card_html = f'''        <div class="code-card">
            <div class="file-info">
                <h2>{card["title"]}</h2>
                <div class="danger-level">
                    <div class="danger-fill" style="width: {card["danger"]}%"></div>
                </div>
                <div class="emoji-rating">{card["emoji"]}</div>
{tags_html}
            </div>
            <div class="code-preview">
{card["code"]}
            </div>
        </div>'''
        cards_content.append(card_html)
    
    return HTML_TEMPLATE.format(
        cards_content="\n".join(cards_content)
    )

def save_to_file(content):
    while True:
        path = input("请输入保存路径: ").strip()
        if not path:
            print("路径不能为空")
            continue
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"文件已成功保存到 {os.path.abspath(path)}")
            return True
        except Exception as e:
            print(f"保存失败: {str(e)}")
            retry = input("是否重试？(y/n): ").lower()
            if retry != "y":
                return False

def main():
    cards = []
    unsaved_changes = False
    
    print("欢迎使用抽象小站内容生成器！")
    print("可用命令: [C]创建内容 | [P]保存文件 | [E]退出")
    
    while True:
        action = input("\n请输入操作指令: ").strip().lower()
        
        if action == "c":
            card = create_card()
            cards.append(card)
            unsaved_changes = True
            print("\n卡片创建成功！当前卡片数量:", len(cards))
        elif action == "p":
            if not cards:
                print("当前没有需要保存的内容")
                continue
            html_content = generate_html(cards)
            if save_to_file(html_content):
                unsaved_changes = False
        elif action == "e":
            if unsaved_changes:
                save_choice = input("您有未保存的更改，是否保存？(y/n): ").lower()
                if save_choice == "y":
                    html_content = generate_html(cards)
                    save_to_file(html_content)
            print("感谢使用，再见！")
            break
        else:
            print("无效指令，请输入 [C]创建 | [P]保存 | [E]退出")

if __name__ == "__main__":
    main()