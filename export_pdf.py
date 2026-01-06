import shutil
from pathlib import Path

# ====== 配置区：只改这里 ======
SRC_ROOT = Path(r"D:\Desktop\Neural Symbolic\Code\20260106\batch_output")  # 你的批量输出根目录
DST_DIR  = Path(r"D:\Desktop\Neural Symbolic\Code\20260106\pdf_files")      # 你想收集到的目标目录

MOVE_INSTEAD_OF_COPY = False  # False=复制；True=移动（移动会把原文件夹里的 pdf 拿走）
# =============================


def unique_path(dst: Path) -> Path:
    """如果目标文件已存在，则自动加 _2, _3 ... 避免覆盖"""
    if not dst.exists():
        return dst
    stem, suffix = dst.stem, dst.suffix
    k = 2
    while True:
        cand = dst.with_name(f"{stem}_{k}{suffix}")
        if not cand.exists():
            return cand
        k += 1


def main():
    DST_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(SRC_ROOT.rglob("*.pdf"))
    if not pdfs:
        print(f"[WARN] 没找到任何 PDF：{SRC_ROOT}")
        return

    ok = 0
    for pdf in pdfs:
        # 跳过目标目录里本来就有的（避免重复复制）
        if DST_DIR in pdf.parents:
            continue

        dst = unique_path(DST_DIR / pdf.name)
        if MOVE_INSTEAD_OF_COPY:
            shutil.move(str(pdf), str(dst))
            action = "MOVE"
        else:
            shutil.copy2(str(pdf), str(dst))
            action = "COPY"

        ok += 1
        if ok % 20 == 0:
            print(f"[INFO] 已处理 {ok} 个...")

    print(f"[DONE] 共处理 {ok} 个 PDF -> {DST_DIR}")


if __name__ == "__main__":
    main()
