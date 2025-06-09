# แบบฝึกหัด 2: การใช้งาน PyThaiNLP

"""
แบบฝึกหัดที่ 2: การใช้งาน PyThaiNLP

วัตถุประสงค์:
1. เรียนรู้การใช้งาน PyThaiNLP สำหรับการแยกคำภาษาไทย
2. เปรียบเทียบ engine ต่างๆ ใน PyThaiNLP
3. ฝึกการวิเคราะห์และประมวลผลข้อความภาษาไทย
4. สร้างแอปพลิเคชันง่ายๆ สำหรับการแยกคำ

คำแนะนำ:
- ติดตั้ง PyThaiNLP ก่อนใช้งาน: pip install pythainlp
- อ่านเอกสารและทดลองใช้งานฟังก์ชันต่างๆ
- สังเกตความแตกต่างของผลลัพธ์จาก engine ต่างๆ
"""

import sys

# ตรวจสอบและติดตั้ง PyThaiNLP
try:
    from pythainlp.tokenize import word_tokenize
    from pythainlp.corpus import thai_stopwords
    from pythainlp.util import normalize
    print("PyThaiNLP พร้อมใช้งาน")
except ImportError:
    print("กำลังติดตั้ง PyThaiNLP...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythainlp"])
    from pythainlp.tokenize import word_tokenize
    from pythainlp.corpus import thai_stopwords
    from pythainlp.util import normalize

# ===== แบบฝึกหัดที่ 2.1: เปรียบเทียบ Engine ต่างๆ =====
print("\n=== แบบฝึกหัดที่ 2.1: เปรียบเทียบ Engine ต่างๆ ===")

def compare_engines(text):
    """
    เปรียบเทียบผลลัพธ์จาก engine ต่างๆ ใน PyThaiNLP
    """
    engines = ['newmm', 'longest']  # เริ่มด้วย engine พื้นฐาน
    
    print(f"ข้อความ: '{text}'")
    print("-" * 50)
    
    results = {}
    for engine in engines:
        try:
            tokens = word_tokenize(text, engine=engine)
            results[engine] = tokens
            print(f"{engine:10}: {' | '.join(tokens)}")
            print(f"{'':10}  จำนวนคำ: {len(tokens)}")
        except Exception as e:
            print(f"{engine:10}: Error - {e}")
    
    return results

# ข้อความทดสอบ
test_sentences = [
    "นักเรียนไปโรงเรียน",
    "ฉันชอบกินข้าวผัด",
    "วันนี้อากาศดีมาก",
    "การประมวลผลภาษาธรรมชาติ"
]

print("ทดลองกับประโยคต่างๆ:")
for sentence in test_sentences:
    compare_engines(sentence)
    print()

# TODO: Exercise 2.1 - เพิ่ม engine อื่นๆ และสังเกตความแตกต่าง
print("TODO: ลองเพิ่ม engine อื่นๆ เช่น 'icu', 'attacut' (ถ้าติดตั้งแล้ว)")
print("สังเกตว่า engine ไหนให้ผลลัพธ์ที่ดีที่สุดสำหรับข้อความแต่ละประเภท")
print()

# ===== แบบฝึกหัดที่ 2.2: การจัดการ Stopwords =====
print("=== แบบฝึกหัดที่ 2.2: การจัดการ Stopwords ===")

def analyze_with_stopwords(text):
    """
    วิเคราะห์ข้อความโดยแยกคำสำคัญออกจาก stopwords
    """
    # แยกคำ
    tokens = word_tokenize(text, engine='newmm')
    
    # ดึง stopwords
    stopwords = thai_stopwords()
    
    # แยกคำสำคัญ
    content_words = [token for token in tokens if token not in stopwords and token.strip()]
    
    print(f"ข้อความ: '{text}'")
    print(f"คำทั้งหมด: {' | '.join(tokens)}")
    print(f"Stopwords ที่พบ: {[token for token in tokens if token in stopwords]}")
    print(f"คำสำคัญ: {' | '.join(content_words)}")
    print(f"อัตราส่วนคำสำคัญ: {len(content_words)}/{len(tokens)} = {len(content_words)/len(tokens)*100:.1f}%")
    print()

# ทดสอบการจัดการ stopwords
stopword_test_sentences = [
    "ฉันไปที่โรงเรียนเพื่อเรียนหนังสือ",
    "เขาเป็นคนที่ดีมากและใจดี",
    "นี่คือการทดสอบระบบประมวลผลภาษาไทย"
]

for sentence in stopword_test_sentences:
    analyze_with_stopwords(sentence)

# TODO: Exercise 2.2 - สร้างฟังก์ชันกรองคำตามเกณฑ์ต่างๆ
print("TODO: สร้างฟังก์ชันที่กรองคำตามเกณฑ์ต่างๆ เช่น:")
print("- กรองคำที่สั้นเกินไป (น้อยกว่า 2 ตัวอักษร)")
print("- กรองเฉพาะคำนาม หรือคำกริยา")
print("- กรองคำที่เป็นตัวเลขหรือสัญลักษณ์")
print()

# ===== แบบฝึกหัดที่ 2.3: การปรับปรุงข้อความ =====
print("=== แบบฝึกหัดที่ 2.3: การปรับปรุงข้อความ ===")

def preprocess_text(text):
    """
    ปรับปรุงข้อความก่อนการแยกคำ
    """
    # TODO: Exercise 2.3 - เติมโค้ดการปรับปรุงข้อความ
    # 1. ใช้ normalize() เพื่อปรับปรุงข้อความ
    # 2. ลบช่องว่างส่วนเกิน
    # 3. จัดการกับตัวเลขและสัญลักษณ์
    
    # ตัวอย่างพื้นฐาน
    processed = text.strip()
    
    # ใช้ normalize ของ PyThaiNLP
    try:
        processed = normalize(processed)
    except:
        pass
    
    return processed

def advanced_tokenize(text):
    """
    การแยกคำขั้นสูงที่รวมการปรับปรุงข้อความ
    """
    # ปรับปรุงข้อความก่อน
    processed_text = preprocess_text(text)
    
    # แยกคำ
    tokens = word_tokenize(processed_text, engine='newmm')
    
    # กรองและปรับปรุงผลลัพธ์
    filtered_tokens = []
    for token in tokens:
        token = token.strip()
        if token and len(token) > 0:  # ลบช่องว่างและคำว่าง
            filtered_tokens.append(token)
    
    return {
        'original': text,
        'processed': processed_text,
        'tokens': filtered_tokens,
        'token_count': len(filtered_tokens)
    }

# ทดสอบกับข้อความที่มีปัญหา
problematic_texts = [
    "  นี่คือ   ข้อความที่มี ช่องว่าง   มาก  ",
    "ข้อความ123ที่มี456ตัวเลข789",
    "ข้อความ!@#ที่มี$%^สัญลักษณ์&*()",
    "ข้อความภาษาไทยผสมEnglishและ123"
]

print("ทดสอบการปรับปรุงข้อความ:")
for text in problematic_texts:
    result = advanced_tokenize(text)
    print(f"ต้นฉบับ: '{result['original']}'")
    print(f"ปรับปรุง: '{result['processed']}'")
    print(f"ผลลัพธ์: {' | '.join(result['tokens'])}")
    print(f"จำนวนคำ: {result['token_count']}")
    print("-" * 50)

print()

# ===== แบบฝึกหัดที่ 2.4: สร้างแอปพลิเคชันง่ายๆ =====
print("=== แบบฝึกหัดที่ 2.4: สร้างแอปพลิเคชันง่ายๆ ===")

class ThaiTextAnalyzer:
    """
    คลาสสำหรับวิเคราะห์ข้อความภาษาไทย
    """
    
    def __init__(self, engine='newmm'):
        self.engine = engine
        self.stopwords = thai_stopwords()
    
    def analyze(self, text):
        """
        วิเคราะห์ข้อความอย่างครอบคลุม
        """
        # TODO: Exercise 2.4 - เติมโค้ดการวิเคราะห์
        result = {
            'original_text': text,
            'character_count': len(text),
            'tokens': [],
            'word_count': 0,
            'content_words': [],
            'content_word_count': 0,
            'stopwords_found': [],
            'average_word_length': 0,
            'unique_words': set(),
            'word_frequency': {}
        }
        
        # เติมโค้ดการวิเคราะห์ที่นี่
        
        return result
    
    def compare_engines(self, text, engines=['newmm', 'longest']):
        """
        เปรียบเทียบผลลัพธ์จาก engine ต่างๆ
        """
        # TODO: Exercise 2.4 - เติมโค้ดการเปรียบเทียบ
        results = {}
        
        for engine in engines:
            try:
                tokens = word_tokenize(text, engine=engine)
                results[engine] = {
                    'tokens': tokens,
                    'word_count': len(tokens),
                    'unique_words': len(set(tokens))
                }
            except Exception as e:
                results[engine] = {'error': str(e)}
        
        return results
    
    def batch_analyze(self, texts):
        """
        วิเคราะห์ข้อความหลายๆ ข้อความพร้อมกัน
        """
        # TODO: Exercise 2.4 - เติมโค้ดการวิเคราะห์แบบ batch
        results = []
        
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        
        return results

# ทดสอบแอปพลิเคชัน
analyzer = ThaiTextAnalyzer()

sample_texts = [
    "นักเรียนไปโรงเรียนเพื่อเรียนหนังสือ",
    "วันนี้อากาศดีมากเหมาะสำหรับการเดินทาง",
    "การประมวลผลภาษาธรรมชาติเป็นสาขาที่น่าสนใจ"
]

print("ทดสอบแอปพลิเคชันวิเคราะห์ข้อความ:")
print("TODO: เติมโค้ดในคลาส ThaiTextAnalyzer และทดสอบการทำงาน")
print()

# ===== แบบฝึกหัดที่ 2.5: โปรเจกต์ขนาดเล็ก =====
print("=== แบบฝึกหัดที่ 2.5: โปรเจกต์ขนาดเล็ก ===")

def create_word_frequency_report(texts, min_frequency=2):
    """
    สร้างรายงานความถี่ของคำจากข้อความหลายๆ ข้อความ
    """
    # TODO: Exercise 2.5 - สร้างรายงานความถี่ของคำ
    from collections import Counter
    
    all_words = []
    
    # รวบรวมคำจากทุกข้อความ
    for text in texts:
        tokens = word_tokenize(text, engine='newmm')
        # กรองเฉพาะคำสำคัญ (ไม่รวม stopwords)
        stopwords = thai_stopwords()
        content_words = [token for token in tokens if token not in stopwords and len(token) > 1]
        all_words.extend(content_words)
    
    # นับความถี่
    word_freq = Counter(all_words)
    
    # กรองคำที่มีความถี่ต่ำ
    frequent_words = {word: freq for word, freq in word_freq.items() if freq >= min_frequency}
    
    return {
        'total_words': len(all_words),
        'unique_words': len(word_freq),
        'frequent_words': frequent_words,
        'top_words': word_freq.most_common(10)
    }

# ข้อความตัวอย่างสำหรับโปรเจกต์
project_texts = [
    "นักเรียนไปโรงเรียนทุกวัน นักเรียนเรียนหนังสือ",
    "ครูสอนนักเรียนในโรงเรียน ครูเป็นคนดี",
    "โรงเรียนมีนักเรียนมาก โรงเรียนใหญ่",
    "การเรียนการสอนในโรงเรียนดี นักเรียนชอบเรียน"
]

print("โปรเจกต์: วิเคราะห์ความถี่ของคำ")
report = create_word_frequency_report(project_texts)
print(f"จำนวนคำทั้งหมด: {report['total_words']}")
print(f"จำนวนคำที่ไม่ซ้ำ: {report['unique_words']}")
print(f"คำที่พบบ่อย (top 10): {report['top_words']}")

print("\n" + "="*60)
print("คำแนะนำสำหรับการทำแบบฝึกหัด:")
print("1. เติมโค้ดในส่วนที่มี TODO")
print("2. ทดลองรันและสังเกตผลลัพธ์")
print("3. ปรับปรุงโค้ดให้ทำงานได้ดีขึ้น")
print("4. ลองใช้ข้อมูลของตัวเองในการทดสอบ")
print("="*60)

