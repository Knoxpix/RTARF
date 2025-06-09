# ตัวอย่างโค้ด 1: Maximum Matching Algorithm พื้นฐาน

def maximum_matching_basic(text, dictionary):
    """
    Maximum Matching Algorithm แบบพื้นฐาน
    
    Args:
        text (str): ข้อความที่ต้องการแยกคำ
        dictionary (set): พจนานุกรมคำศัพท์
    
    Returns:
        list: รายการคำที่แยกได้
    """
    text = text.lower()  # แปลงเป็นตัวพิมพ์เล็ก
    tokens = []
    i = 0
    
    while i < len(text):
        max_word = ""
        
        # ค้นหาคำที่ยาวที่สุดที่เริ่มต้นจากตำแหน่ง i
        for j in range(i, len(text)):
            temp_word = text[i:j+1]
            if temp_word in dictionary and len(temp_word) > len(max_word):
                max_word = temp_word
        
        # ถ้าพบคำ ให้เพิ่มเข้าไปในผลลัพธ์
        if max_word:
            tokens.append(max_word)
            i += len(max_word)
        else:
            # ถ้าไม่พบคำ ให้ถือว่าตัวอักษรนั้นเป็นคำ
            tokens.append(text[i])
            i += 1
    
    return tokens

# ทดสอบการทำงาน
if __name__ == "__main__":
    # พจนานุกรมตัวอย่าง
    sample_dictionary = {
        "this", "is", "insane", "the", "cat", "in", "hat", 
        "tomorrow", "sunday", "hello", "world", "python", "programming"
    }
    
    # ข้อความทดสอบ
    test_texts = [
        "thisisinsane",
        "tomorrowissunday", 
        "helloworld",
        "pythonprogramming"
    ]
    
    print("=== Maximum Matching Algorithm Demo ===")
    for text in test_texts:
        result = maximum_matching_basic(text, sample_dictionary)
        print(f"Input: '{text}'")
        print(f"Output: {result}")
        print(f"Joined: '{' | '.join(result)}'")
        print("-" * 40)

