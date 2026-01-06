import re
from pathlib import Path

# ====== 配置区：只改这里 ======
PDF_DIR = Path(r"D:\Desktop\Neural Symbolic\Code\20260106\pdf_files")  # 你的PDF目录
DRY_RUN = False  # 先True预览；确认后改False执行

# 映射表：编号 -> 新名字（不含 .pdf）
# 例如把 001_*.pdf 改成 001_张三.pdf 或 张三.pdf 都行（你决定格式）
RENAME_MAP = {
    "001": "00-证明、计算以及它们的边界（上）",
    "002": "00-证明、计算以及它们的边界（下）",
    "003": "01-绪论",
    "004": "02-命题规则学习（上）",
    "005": "03-命题规则学习（下）",
    "006": "04-逻辑程序（上）",
    "007": "05-逻辑程序（下）",
    "008": "06-归纳逻辑程序（上）",
    "009": "07-归纳逻辑程序（中）",
    "101": "08-归纳逻辑程序（下）-MIL",
    "102": "08-归纳逻辑程序（下）-Popper",
    "011": "09-非经典逻辑与近似推理",
    "012": "10-概率逻辑系统及学习",
    # ...
}
# ==============================


INVALID_CHARS = r'<>:"/\\|?*'


def sanitize_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(f"[{re.escape(INVALID_CHARS)}]", "_", name)
    name = name.rstrip(" .")
    return name


def unique_path(dst: Path) -> Path:
    if not dst.exists():
        return dst
    stem, suffix = dst.stem, dst.suffix
    k = 2
    while True:
        cand = dst.with_name(f"{stem}_{k}{suffix}")
        if not cand.exists():
            return cand
        k += 1


def extract_id(filename: str) -> str | None:
    """
    从文件名提取编号：
    支持 001_xxx.pdf / 001-xxx.pdf / 001 xxx.pdf
    """
    m = re.match(r"^(\d{3})[\s_-].*\.pdf$", filename, flags=re.IGNORECASE)
    return m.group(1) if m else None


def main():
    if not PDF_DIR.exists():
        print(f"[ERROR] 目录不存在：{PDF_DIR}")
        return

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"[WARN] 没找到PDF：{PDF_DIR}")
        return

    plan = []
    for pdf in pdfs:
        id3 = extract_id(pdf.name)
        if not id3:
            continue
        if id3 not in RENAME_MAP:
            continue

        new_stem = sanitize_filename(RENAME_MAP[id3])
        if not new_stem:
            continue

        dst = unique_path(pdf.with_name(new_stem + ".pdf"))
        if dst.name == pdf.name:
            continue

        plan.append((pdf, dst))

    if not plan:
        print("[INFO] 没有匹配到需要改名的文件（可能编号提取规则不对，或 RENAME_MAP 没覆盖）。")
        return

    print(f"[INFO] 计划改名 {len(plan)} 个文件：")
    for src, dst in plan:
        print(f"  {src.name}  ->  {dst.name}")

    if DRY_RUN:
        print("\n[DRY_RUN=True] 仅预览未执行。确认无误后把 DRY_RUN 改成 False 再运行。")
        return

    for src, dst in plan:
        src.replace(dst)

    print("\n[DONE] 重命名完成。")


if __name__ == "__main__":
    main()
