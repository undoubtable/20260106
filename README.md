# Neural Symbolic — 批量导出与重命名工具集合

这是一个小型工具集合，用于从 HTML 幻灯片或网页导出图像、批量生成 PDF/PPT ，并按映射表重命名输出文件，适合课程幻灯片、讲义等批量处理场景。
目前测试提取的是戴望川老师的符号学习简介PPT。链接如下：https://daiwz.net/teaching/


**目录结构：**
- `test.py`：简单的测试/示例用法脚本。
- `batch_export.py`：批量导出脚本（将网页/幻灯片转换为图片）。
- `export_pdf.py`：把导出的图片合并为 PDF 的脚本。
- `rename_by_map.py`：按映射表（JSON/CSV）重命名文件。

- `batch_output/`：脚本运行时的中间输出目录（每个输入生成单独子目录）。
- `output/`：最终的图片输出目录。
- `pdf_files/`：生成的 PDF 存放目录。

**环境与依赖**
- Python 3.8+。
- 建议使用虚拟环境（`venv` 或 `conda`）。
- 依赖库请查看脚本顶部的 `import`，常见会用到 `Pillow`, `img2pdf`, `requests` 等；可根据需要安装：

```powershell
python -m pip install Pillow img2pdf requests
```

**快速开始 / 使用说明**

1. 批量导出（示例）：

```powershell
python batch_export.py
```

脚本会读取 `urls.txt` 或内置配置（视脚本实现），将每个源生成到 `batch_output/` 下的子目录，图片会放在 `png/` 子目录中。

2. 合并为 PDF：

```powershell
python export_pdf.py
```

该脚本会扫描 `output/png/`（或 `batch_output` 中的 png 文件），并将图片按顺序合并为 PDF，输出到 `pdf_files/`。

3. 按映射表重命名（示例）：

```powershell
python rename_by_map.py mapping.json
```

`mapping.json`（或 CSV）示例格式：

```json
{
	"old_name1.png": "lecture01_slide01.png",
	"old_name2.png": "lecture01_slide02.png"
}
```

4. 运行测试示例：

```powershell
python test.py
```

**输出说明**
- 中间文件位于 `batch_output/_tmp/`，可用于调试或二次处理。
- 最终图片位于 `output/png/`，生成的 PDF 位于 `pdf_files/`。

**常见问题**
- 路径问题：在 Windows 下注意使用反斜杠或原始字符串，脚本内通常使用相对路径更稳妥。
- 字符编码：若处理含中文文件名或文本，确保 Python 默认编码或文件读取时指定 `utf-8`。
