"""Clean Vietnamese text before sending it to a TTS engine.

- numbers -> Vietnamese words ("27" -> "hai mươi bảy")
- strip symbols TTS engines read badly (【】, brackets, markdown, bullets)
- phrase fixes for words a model tends to slur (configurable)

Subtitles should keep the original text; only the audio input is changed.
"""
import re

DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

# Cụm hay bị đọc dính/sai -> bản đọc đúng. Thêm tuỳ theo engine.
DEFAULT_FIXES = {
    "thều thào": "thều thào,",  # VieNeu Nano đọc "thều thào van xin" thành "thều than xin"
}


def _read_hundreds(n, full):
    h, t, u = n // 100, (n // 10) % 10, n % 10
    out = []
    if h or full:
        out += [DIGITS[h], "trăm"]
    if t == 0:
        if u and (h or full):
            out.append("lẻ")
    elif t == 1:
        out.append("mười")
    else:
        out += [DIGITS[t], "mươi"]
    if u:
        if u == 1 and t > 1:
            out.append("mốt")
        elif u == 5 and t > 0:
            out.append("lăm")
        elif u == 4 and t > 1:
            out.append("tư")
        else:
            out.append(DIGITS[u])
    return out


def number_to_words(n):
    """0 <= n < 10^12 -> Vietnamese words."""
    n = int(n)
    if n == 0:
        return "không"
    units = ["", "nghìn", "triệu", "tỷ"]
    groups = []
    while n:
        groups.append(n % 1000)
        n //= 1000
    words = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        words += _read_hundreds(g, full=i < len(groups) - 1)
        if units[i]:
            words.append(units[i])
    return " ".join(words)


def numbers_to_words(text):
    def rep(m):
        s = m.group(0).replace(".", "").replace(",", "")
        return number_to_words(s) if len(s) <= 12 else m.group(0)
    # 1.000.000 / 1,000 kiểu Việt hoặc số thường
    return re.sub(r"\d{1,3}(?:[.,]\d{3})+(?!\d)|\d+", rep, text)


def strip_symbols(text):
    text = re.sub(r"[【】\[\]{}<>*#_~|•►▶]", " ", text)
    text = re.sub(r"[()（）]", ", ", text)
    text = re.sub(r"\s*[-–—]{2,}\s*", ", ", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r",+\s*([.!?;:])", r"\1", text)   # ", ." -> "."
    text = re.sub(r"([,.!?;:])\1+", r"\1", text)
    text = re.sub(r"^[,\s]+|[,\s]+$", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def apply_fixes(text, fixes=None):
    for a, b in (fixes or DEFAULT_FIXES).items():
        text = re.sub(r"(?i)(?<!\w)" + re.escape(a) + r"(?!\w)",
                      lambda m, b=b: (b[:1].upper() + b[1:]) if m.group(0)[:1].isupper() else b, text)
    return re.sub(r",\s*,", ",", text)


def clean(text, fixes=None):
    return apply_fixes(strip_symbols(numbers_to_words(text)), fixes)


if __name__ == "__main__":
    import sys
    print(clean(" ".join(sys.argv[1:]) or "【Hệ thống】 còn 27 phút 31 giây, nàng thều thào van xin (lần 2)."))
