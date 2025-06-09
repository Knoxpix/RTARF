# แบบฝึกหัด 1: การใช้งาน Maximum Matching Algorithm

"""
แบบฝึกหัดที่ 1: การใช้งาน Maximum Matching Algorithm

วัตถุประสงค์:
1. เข้าใจหลักการทำงานของ Maximum Matching Algorithm
2. ฝึกการเขียนโค้ดและปรับปรุงอัลกอริทึม
3. ทดลองกับข้อมูลต่างๆ และวิเคราะห์ผลลัพธ์

คำแนะนำ:
- อ่านโค้ดตัวอย่างให้เข้าใจก่อน
- ทำแบบฝึกหัดตามลำดับ
- ทดลองปรับเปลี่ยนค่าต่างๆ เพื่อดูผลลัพธ์
"""

# โค้ดพื้นฐานสำหรับการฝึกหัด
def maximum_matching_exercise(text, dictionary):
    """
    Maximum Matching Algorithm สำหรับแบบฝึกหัด
    """
    text = text.lower()
    tokens = []
    i = 0
    
    while i < len(text):
        max_word = ""
        
        # TODO: Exercise 1.1 - เติมโค้ดการหาคำที่ยาวที่สุด
        # ให้นักเรียนเติมโค้ดในส่วนนี้
        
        if max_word:
            tokens.append(max_word)
            i += len(max_word)
        else:
            tokens.append(text[i])
            i += 1
    
    return tokens

# ===== แบบฝึกหัดที่ 1.1: เติมโค้ดพื้นฐาน =====
print("=== แบบฝึกหัดที่ 1.1: เติมโค้ดพื้นฐาน ===")
print("คำแนะนำ: เติมโค้ดในฟังก์ชัน maximum_matching_exercise")
print("ให้หาคำที่ยาวที่สุดที่เริ่มต้นจากตำแหน่ง i")
print()

# ===== แบบฝึกหัดที่ 1.2: ทดลองกับพจนานุกรมต่างๆ =====
print("=== แบบฝึกหัดที่ 1.2: ทดลองกับพจนานุกรมต่างๆ ===")

# พจนานุกรมตัวอย่าง
dict1 = {"this", "is", "insane", "the", "cat", "hat"}
dict2 = {"this", "is", "in", "sane", "the", "cat", "hat"}  # แยก "insane" เป็น "in" + "sane"
dict3 = {"thisis", "insane", "the", "cat", "hat"}  # รวม "this" + "is" เป็น "thisis"

test_text = "thisisinsane"

print(f"ข้อความทดสอบ: '{test_text}'")
print()

# TODO: ทดลองใช้พจนานุกรมต่างๆ และสังเกตผลลัพธ์
print("ทดลองใช้พจนานุกรมต่างๆ:")
print("dict1:", dict1)
print("dict2:", dict2) 
print("dict3:", dict3)
print()
print("คำถาม: ผลลัพธ์จะแตกต่างกันอย่างไร? เพราะอะไร?")
print()

# ===== แบบฝึกหัดที่ 1.3: วิเคราะห์ความซับซ้อน =====
print("=== แบบฝึกหัดที่ 1.3: วิเคราะห์ความซับซ้อน ===")

import time

def measure_performance(text, dictionary, algorithm_func):
    """วัดประสิทธิภาพของอัลกอริทึม"""
    start_time = time.time()
    result = algorithm_func(text, dictionary)
    end_time = time.time()
    
    return {
        'result': result,
        'time': end_time - start_time,
        'text_length': len(text),
        'dict_size': len(dictionary),
        'word_count': len(result)
    }

# ข้อความทดสอบความยาวต่างๆ
test_texts = [
    "hello",
    "helloworld",
    "helloworldthisisatest",
    "helloworldthisisatestofmaximummatchingalgorithm"
]

large_dict = {
    "hello", "world", "this", "is", "a", "test", "of", "maximum", "matching", 
    "algorithm", "the", "cat", "in", "hat", "python", "programming", "natural",
    "language", "processing", "machine", "learning", "artificial", "intelligence"
}

print("ทดสอบประสิทธิภาพ:")
print("ความยาวข้อความ | เวลา (ms) | จำนวนคำ")
print("-" * 45)

# TODO: ทดลองวัดประสิทธิภาพและวิเคราะห์ผลลัพธ์
for text in test_texts:
    # ใช้ฟังก์ชันที่เติมโค้ดแล้วจากแบบฝึกหัด 1.1
    # performance = measure_performance(text, large_dict, maximum_matching_exercise)
    # print(f"{len(text):15} | {performance['time']*1000:8.2f} | {performance['word_count']:9}")
    pass

print()
print("คำถาม:")
print("1. ความซับซ้อนของอัลกอริทึมเป็น O(?) เมื่อเทียบกับความยาวของข้อความ?")
print("2. ขนาดของพจนานุกรมส่งผลต่อประสิทธิภาพอย่างไร?")
print()

# ===== แบบฝึกหัดที่ 1.4: จัดการกับปัญหาพิเศษ =====
print("=== แบบฝึกหัดที่ 1.4: จัดการกับปัญหาพิเศษ ===")

def improved_maximum_matching(text, dictionary, handle_unknown=True):
    """
    Maximum Matching ที่ปรับปรุงแล้ว
    
    Args:
        text (str): ข้อความที่ต้องการแยกคำ
        dictionary (set): พจนานุกรม
        handle_unknown (bool): จัดการกับคำที่ไม่รู้จักหรือไม่
    """
    text = text.lower()
    tokens = []
    i = 0
    
    while i < len(text):
        max_word = ""
        
        # หาคำที่ยาวที่สุด
        for j in range(i, len(text)):
            temp_word = text[i:j+1]
            if temp_word in dictionary and len(temp_word) > len(max_word):
                max_word = temp_word
        
        if max_word:
            tokens.append(max_word)
            i += len(max_word)
        else:
            if handle_unknown:
                # TODO: Exercise 1.4 - เติมโค้ดการจัดการกับคำที่ไม่รู้จัก
                # ลองใช้วิธีต่างๆ เช่น:
                # 1. ถือว่าตัวอักษรเดี่ยวเป็นคำ
                # 2. ลองรวมตัวอักษรหลายตัวเป็นคำ
                # 3. ใช้ heuristics อื่นๆ
                tokens.append(text[i])  # วิธีพื้นฐาน
                i += 1
            else:
                tokens.append(text[i])
                i += 1
    
    return tokens

# ทดสอบกับข้อความที่มีคำไม่รู้จัก
problematic_texts = [
    "thisisunknownword",  # มีคำที่ไม่อยู่ในพจนานุกรม
    "abc123def",          # มีตัวเลข
    "hello-world",        # มีเครื่องหมาย
    ""                    # ข้อความว่าง
]

print("ทดสอบกับข้อความที่มีปัญหา:")
for text in problematic_texts:
    if text:  # ข้ามข้อความว่าง
        print(f"'{text}' -> ต้องการการจัดการพิเศษ")

print()
print("คำถาม:")
print("1. ควรจัดการกับตัวเลขและเครื่องหมายอย่างไร?")
print("2. ควรจัดการกับคำที่ไม่อยู่ในพจนานุกรมอย่างไร?")
print("3. มีวิธีใดบ้างในการปรับปรุงอัลกอริทึมให้ดีขึ้น?")
print()

# ===== แบบฝึกหัดที่ 1.5: เปรียบเทียบกับวิธีอื่น =====
print("=== แบบฝึกหัดที่ 1.5: เปรียบเทียบกับวิธีอื่น ===")

def shortest_matching(text, dictionary):
    """
    Shortest Matching Algorithm (ตรงข้ามกับ Maximum Matching)
    """
    text = text.lower()
    tokens = []
    i = 0
    
    while i < len(text):
        # TODO: Exercise 1.5 - เติมโค้ด Shortest Matching
        # หาคำที่สั้นที่สุดแทนที่จะเป็นยาวที่สุด
        min_word = ""
        
        # เติมโค้ดที่นี่
        
        if min_word:
            tokens.append(min_word)
            i += len(min_word)
        else:
            tokens.append(text[i])
            i += 1
    
    return tokens

def random_matching(text, dictionary):
    """
    Random Matching Algorithm (เลือกคำแบบสุ่ม)
    """
    import random
    
    text = text.lower()
    tokens = []
    i = 0
    
    while i < len(text):
        possible_words = []
        
        # หาคำที่เป็นไปได้ทั้งหมด
        for j in range(i, len(text)):
            temp_word = text[i:j+1]
            if temp_word in dictionary:
                possible_words.append(temp_word)
        
        if possible_words:
            # เลือกคำแบบสุ่ม
            chosen_word = random.choice(possible_words)
            tokens.append(chosen_word)
            i += len(chosen_word)
        else:
            tokens.append(text[i])
            i += 1
    
    return tokens

# ทดสอบเปรียบเทียบ
comparison_text = "thisisinsane"
comparison_dict = {"this", "is", "in", "sane", "insane", "th", "hi", "si"}

print(f"ข้อความทดสอบ: '{comparison_text}'")
print(f"พจนานุกรม: {comparison_dict}")
print()

# TODO: เปรียบเทียบผลลัพธ์จากอัลกอริทึมต่างๆ
print("เปรียบเทียบผลลัพธ์:")
print("Maximum Matching: [ให้นักเรียนรันและดูผลลัพธ์]")
print("Shortest Matching: [ให้นักเรียนเติมโค้ดและรัน]")
print("Random Matching: [ลองรันหลายครั้งเพื่อดูความแตกต่าง]")
print()

print("คำถาม:")
print("1. อัลกอริทึมไหนให้ผลลัพธ์ที่ดีที่สุด? วัดจากอะไร?")
print("2. ข้อดีข้อเสียของแต่ละอัลกอริทึมคืออะไร?")
print("3. ในสถานการณ์ใดควรใช้อัลกอริทึมแต่ละแบบ?")

print("\n" + "="*60)
print("หมายเหตุ: นี่เป็นแบบฝึกหัดสำหรับการเรียนรู้")
print("ให้นักเรียนเติมโค้ดในส่วนที่มี TODO และทดลองรันเพื่อดูผลลัพธ์")
print("="*60)

