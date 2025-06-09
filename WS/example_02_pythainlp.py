# ตัวอย่างโค้ด 2: การใช้งาน PyThaiNLP

import sys

# ตรวจสอบและติดตั้ง PyThaiNLP หากยังไม่มี
try:
    import pythainlp
    print("PyThaiNLP version:", pythainlp.__version__)
except ImportError:
    print("Installing PyThaiNLP...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythainlp"])
    import pythainlp

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
import time

def compare_tokenizers(text):
    """
    เปรียบเทียบ tokenizer ต่างๆ ใน PyThaiNLP
    
    Args:
        text (str): ข้อความภาษาไทยที่ต้องการแยกคำ
    
    Returns:
        dict: ผลลัพธ์จาก tokenizer ต่างๆ
    """
    engines = ['newmm', 'longest', 'icu']
    results = {}
    
    print(f"ข้อความต้นฉบับ: '{text}'")
    print("=" * 60)
    
    for engine in engines:
        try:
            start_time = time.time()
            tokens = word_tokenize(text, engine=engine)
            end_time = time.time()
            
            results[engine] = {
                'tokens': tokens,
                'time': end_time - start_time,
                'word_count': len(tokens)
            }
            
            print(f"Engine: {engine}")
            print(f"ผลลัพธ์: {' | '.join(tokens)}")
            print(f"จำนวนคำ: {len(tokens)}")
            print(f"เวลาที่ใช้: {(end_time - start_time)*1000:.2f} ms")
            print("-" * 40)
            
        except Exception as e:
            print(f"Error with {engine}: {e}")
            results[engine] = None
    
    return results

def remove_stopwords(tokens):
    """
    ลบ stopwords ออกจากรายการคำ
    
    Args:
        tokens (list): รายการคำ
    
    Returns:
        list: รายการคำที่ไม่มี stopwords
    """
    stopwords = thai_stopwords()
    return [token for token in tokens if token not in stopwords and token.strip()]

def analyze_text(text):
    """
    วิเคราะห์ข้อความภาษาไทยอย่างละเอียด
    
    Args:
        text (str): ข้อความภาษาไทย
    """
    print("=== การวิเคราะห์ข้อความภาษาไทย ===")
    
    # แยกคำด้วย newmm (engine ที่แนะนำ)
    tokens = word_tokenize(text, engine='newmm')
    
    # ลบ stopwords
    content_words = remove_stopwords(tokens)
    
    print(f"ข้อความต้นฉบับ: '{text}'")
    print(f"คำทั้งหมด: {' | '.join(tokens)}")
    print(f"จำนวนคำทั้งหมด: {len(tokens)}")
    print(f"คำสำคัญ (ไม่รวม stopwords): {' | '.join(content_words)}")
    print(f"จำนวนคำสำคัญ: {len(content_words)}")
    
    # สถิติเพิ่มเติม
    char_count = len(text)
    avg_word_length = sum(len(token) for token in tokens) / len(tokens) if tokens else 0
    
    print(f"จำนวนตัวอักษร: {char_count}")
    print(f"ความยาวเฉลี่ยของคำ: {avg_word_length:.2f} ตัวอักษร")

if __name__ == "__main__":
    # ข้อความทดสอบภาษาไทย
    thai_texts = [
        "นักเรียนไปโรงเรียนเพื่อเรียนหนังสือ",
        "วันนี้อากาศดีมากเหมาะสำหรับการเดินทางท่องเที่ยว",
        "การประมวลผลภาษาธรรมชาติเป็นสาขาที่น่าสนใจ",
        "ฉันชอบกินข้าวผัดและส้มตำ"
    ]
    
    for i, text in enumerate(thai_texts, 1):
        print(f"\n{'='*20} ตัวอย่างที่ {i} {'='*20}")
        compare_tokenizers(text)
        print("\n" + "="*60)
        analyze_text(text)
        print("\n" + "="*80)

