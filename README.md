# vi-tts-text-fixes

Chuẩn hoá văn bản tiếng Việt trước khi đưa vào TTS (VieNeu, Piper, edge-tts…). Không cần thư viện ngoài.

- **Số thành chữ:** `27` → `hai mươi bảy`, `1.500.000` → `một triệu năm trăm nghìn`, có xử lý *mốt / lăm / tư / lẻ*
- **Bỏ ký tự TTS hay đọc lỗi:** `【】`, ngoặc, markdown, bullet, gạch ngang kép
- **Sửa cụm hay bị đọc dính**, cấu hình được. Ví dụ VieNeu Nano đọc *"thều thào van xin"* thành *"thều than xin"*; thêm dấu phẩy ngắt nhịp là đọc đúng.

Chỉ đổi chữ gửi vào TTS. Phụ đề nên giữ nguyên chữ gốc.

## Dùng

```python
from vi_tts_fixes import clean, number_to_words

clean("【Hệ thống】 còn 27 phút 31 giây, nàng thều thào van xin (lần 2).")
# 'Hệ thống còn hai mươi bảy phút ba mươi mốt giây, nàng thều thào, van xin, lần hai.'

number_to_words(105)   # 'một trăm lẻ năm'
number_to_words(2025)  # 'hai nghìn không trăm hai mươi lăm'

clean("text", fixes={"cụm sai": "cụm đúng"})
```

```bash
python vi_tts_fixes.py "Chương 12: còn 3 ngày"
```

Dùng trong pipeline audio của [Truyện Kể](https://truyenke.com).

## License

MIT
