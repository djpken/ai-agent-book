#!/usr/bin/env python3
"""Chapter 8 figures — Agent 的自我進化.

NOTE: this generator was previously a stray copy of chapter 9's figures, which
left fig8-1..fig8-7 showing chapter-9 content. It has been rewritten so each
figure matches its caption in chapter8.md. Figures are built with svg_lib;
titles live in the body text (svg_lib strips in-figure titles).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svg_lib import SVG, FS_SMALL, FS_TINY, FS_BODY

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


def _pipeline(stages, fname, W=880, feedback=None):
    """Horizontal stage pipeline with an optional dashed feedback loop."""
    n = len(stages)
    bw = min(190, (W - 40 - (n - 1) * 22) // n)
    bh, gap = 84, 22
    H = 234 if feedback else 174   # +24 for the 40px title-crop margin
    s = SVG(W, H)
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    y = 48                          # start below the TITLE_CROP_PX=40 line
    pos = []
    for i, (lab, sub) in enumerate(stages):
        x = x0 + i * (bw + gap)
        s.box(x, y, bw, bh, lab, sublabel=sub, bold=True, fill='light')
        pos.append(x)
        if i > 0:
            s.arrow(pos[i - 1] + bw + 2, y + bh / 2, x - 2, y + bh / 2)
    if feedback:
        lx = pos[-1] + bw / 2
        fx = pos[0] + bw / 2
        ry = y + bh + 34
        s.line(lx, y + bh, lx, ry, dash=True)
        s.line(lx, ry, fx, ry, dash=True)
        s.arrow(fx, ry, fx, y + bh + 2, dash=True)
        s.text((lx + fx) / 2, ry + 18, feedback, size=FS_SMALL, fill='text_light')
    s.save(os.path.join(OUT, fname + '.svg'))


def fig8_1():  # 外部化學習循環
    _pipeline([("完成任務", "產生原始經驗"), ("提煉經驗", "總結·壓縮·結構化"),
               ("存入外部系統", "知識庫/工具，可檢索"), ("檢索複用", "下次任務調用")],
              'fig8-1', feedback="經驗持續沉澱，跨會話複用")


def fig8_2():  # GAIA 經驗學習系統
    _pipeline([("成功軌跡", "完成任務的過程"), ("策略總結", "提煉為知識摘要"),
               ("知識摘要庫", "建立語義索引"), ("檢索注入", "Agent 決策時取用")],
              'fig8-2', feedback="相似任務複用歷史經驗")


def fig8_3():  # Agent 自我進化流水線（需求識別→工具搜索→代碼封裝→工具註冊）
    _pipeline([("① 需求識別", "現有工具不足"), ("② 工具搜索", "開放世界查找"),
               ("③ 代碼封裝", "生成並封裝"), ("④ 工具註冊", "納入庫可複用")],
              'fig8-3', feedback="新工具註冊後可被後續任務複用，持續擴展能力邊界")


def fig8_4():  # Voyager 持續學習架構（課程生成器 + 技能庫 + 迭代提示）
    _pipeline([("課程生成器", "提出漸進式新任務"), ("迭代提示機制", "生成並調試技能代碼"),
               ("技能庫", "存儲可複用技能")],
              'fig8-4', W=760, feedback="技能積累後解鎖更難的任務（開放世界探索）")


def fig8_5():  # 實驗 8-4 自我進化流水線（搜索→評估→測試→封裝→複用）
    _pipeline([("① 搜索", "開放網絡找工具"), ("② 評估", "判斷是否合適"), ("③ 測試", "驗證可用性"),
               ("④ 封裝", "包成標準工具"), ("⑤ 複用", "納入工具庫")],
              'fig8-5', W=940, feedback="新工具沉澱後供後續任務複用")


if __name__ == '__main__':
    for fn in (fig8_1, fig8_2, fig8_3, fig8_4, fig8_5):
        fn()
        print('saved', fn.__name__)
