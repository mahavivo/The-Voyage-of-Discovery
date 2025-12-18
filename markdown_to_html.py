import markdown
import re
import os

def generate_ebook(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"找不到文件: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    toc_entries = []
    processed_lines = []
    
    # 1. 扫描并处理 🔴 开头的行
    # 我们将这些行替换为带有 ID 的 HTML 标签，以便目录跳转
    section_count = 0
    for line in lines:
        if line.strip().startswith('🔴'):
            section_count += 1
            title = line.strip().replace('🔴', '').strip()
            anchor_id = f"section-{section_count}"
            
            # 记录目录项
            toc_entries.append({'title': title, 'id': anchor_id})
            
            # 将原始行替换为带有 ID 的 HTML 标题，方便 Markdown 渲染
            processed_lines.append(f'<h2 id="{anchor_id}">🔴 {title}</h2>\n')
        else:
            processed_lines.append(line)

    full_text = "".join(processed_lines)

    # 2. 转换 Markdown 为 HTML
    # 包含表格和代码块支持
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
    content_html = md.convert(full_text)

    # 3. 手动构建目录 HTML 列表
    toc_html_list = "<ul>"
    for entry in toc_entries:
        toc_html_list += f'<li><a href="#{entry["id"]}">{entry["title"]}</a></li>'
    toc_html_list += "</ul>"

    # 4. 定义 CSS 样式
    css = """
    body {
        margin: 0;
        padding: 0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        background-color: #f5f7f9;
        display: flex;
    }

    /* 侧边栏目录 */
    #sidebar {
        width: 280px;
        height: 100vh;
        position: fixed;
        left: 0;
        top: 0;
        background-color: #ffffff;
        border-right: 1px solid #dcdfe6;
        padding: 30px 20px;
        overflow-y: auto;
        box-sizing: border-box;
    }

    #sidebar h2 {
        font-size: 1.1rem;
        color: #909399;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }

    #sidebar ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    #sidebar li {
        margin-bottom: 10px;
    }

    #sidebar a {
        text-decoration: none;
        color: #606266;
        font-size: 0.95rem;
        line-height: 1.4;
        display: block;
        transition: all 0.3s;
    }

    #sidebar a:hover {
        color: #409EFF;
        transform: translateX(5px);
    }

    /* 正文容器：实现左右居中 */
    #content-wrapper {
        flex: 1;
        margin-left: 280px; /* 避开固定定位的侧边栏 */
        display: flex;
        justify-content: center; /* 水平居中核心 */
        min-height: 100vh;
    }

    /* 正文内容区域 */
    #main-content {
        background-color: #ffffff;
        width: 100%;
        max-width: 960px; /* 限制正文最大宽度，提升阅读体验 */
        padding: 45px 45px;
        box-shadow: 0 0 20px rgba(0,0,0,0.05);
        box-sizing: border-box;
    }

    /* 正文排版细节 */
    h2[id^="section-"] {
        color: #1f2f3d;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px dashed #eee;
    }

    # p {
    #     line-height: 1.5;
    #     margin-bottom: 1.2rem;
    #     font-size: 1rem;
    # }

    img {
    max-width: 100%;    /* 宽度最大不会超过父容器 */
    height: auto;       /* 高度根据宽度自动缩放，不会变形 */
    display: block;     /* 转为块级元素，方便设置居中 */
    margin: 25px auto;  /* 图像上下留白，左右自动居中 */
    border-radius: 4px; /* 可选：给图片加一点圆角显得更柔和 */
    box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* 可选：给图片加一点点阴影提升质感 */
}

    blockquote {
        margin: 20px 0;
        padding: 15px 25px;
        background-color: #f8f9fa;
        border-left: 5px solid #409EFF;
        font-style: italic;
        color: #555;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }

    table th, table td {
        border: 1px solid #ebeef5;
        padding: 12px;
        text-align: left;
    }

    table th {
        background-color: #fafafa;
    }

    /* 移动端适配 */
    @media (max-width: 1000px) {
        #sidebar { display: none; }
        #content-wrapper { margin-left: 0; }
        #main-content { padding: 30px 20px; }
    }
    """

    # 5. 组装 HTML
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>电子书 - {os.path.basename(input_file)}</title>
    <style>{css}</style>
</head>
<body>
    <div id="sidebar">
        <h2>目录导读</h2>
        {toc_html_list}
    </div>
    <div id="content-wrapper">
        <article id="main-content">
            {content_html}
        </article>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"转换完成！生成的 HTML 已保存在: {output_file}")

if __name__ == "__main__":
    generate_ebook("哲学的历程.md", "哲学的历程.html")