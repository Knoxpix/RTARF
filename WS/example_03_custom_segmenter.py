# ตัวอย่างโค้ด 3: การสร้าง Custom Word Segmenter

import re
from collections import defaultdict, Counter

class CustomWordSegmenter:
    """
    Custom Word Segmenter ที่รวมหลายเทคนิค
    """
    
    def __init__(self):
        self.dictionary = set()
        self.word_frequencies = defaultdict(int)
        self.bigram_frequencies = defaultdict(int)
        
    def add_words_to_dictionary(self, words):
        """เพิ่มคำเข้าพจนานุกรม"""
        if isinstance(words, str):
            words = [words]
        for word in words:
            self.dictionary.add(word.lower())
    
    def train_from_text(self, text, delimiter=' '):
        """ฝึกโมเดลจากข้อความที่แยกคำแล้ว"""
        words = text.split(delimiter)
        
        # นับความถี่ของคำ
        for word in words:
            word = word.strip().lower()
            if word:
                self.word_frequencies[word] += 1
                self.dictionary.add(word)
        
        # นับความถี่ของ bigram
        for i in range(len(words) - 1):
            word1 = words[i].strip().lower()
            word2 = words[i + 1].strip().lower()
            if word1 and word2:
                self.bigram_frequencies[(word1, word2)] += 1
    
    def maximum_matching(self, text, direction='forward'):
        """
        Maximum Matching Algorithm
        
        Args:
            text (str): ข้อความที่ต้องการแยกคำ
            direction (str): 'forward' หรือ 'backward'
        
        Returns:
            list: รายการคำที่แยกได้
        """
        text = text.lower().strip()
        tokens = []
        
        if direction == 'forward':
            i = 0
            while i < len(text):
                max_word = ""
                for j in range(i, len(text)):
                    temp_word = text[i:j+1]
                    if temp_word in self.dictionary and len(temp_word) > len(max_word):
                        max_word = temp_word
                
                if max_word:
                    tokens.append(max_word)
                    i += len(max_word)
                else:
                    tokens.append(text[i])
                    i += 1
        
        elif direction == 'backward':
            i = len(text) - 1
            while i >= 0:
                max_word = ""
                for j in range(i + 1):
                    temp_word = text[j:i+1]
                    if temp_word in self.dictionary and len(temp_word) > len(max_word):
                        max_word = temp_word
                
                if max_word:
                    tokens.insert(0, max_word)
                    i -= len(max_word)
                else:
                    tokens.insert(0, text[i])
                    i -= 1
        
        return tokens
    
    def bidirectional_matching(self, text):
        """
        Bidirectional Maximum Matching
        เปรียบเทียบผลลัพธ์จาก forward และ backward แล้วเลือกที่ดีที่สุด
        """
        forward_result = self.maximum_matching(text, 'forward')
        backward_result = self.maximum_matching(text, 'backward')
        
        # เกณฑ์การเลือก: จำนวนคำน้อยกว่า หรือ จำนวนตัวอักษรเดี่ยวน้อยกว่า
        forward_score = self._calculate_score(forward_result)
        backward_score = self._calculate_score(backward_result)
        
        if forward_score >= backward_score:
            return forward_result, 'forward'
        else:
            return backward_result, 'backward'
    
    def _calculate_score(self, tokens):
        """คำนวณคะแนนของการแยกคำ (คะแนนสูง = ดีกว่า)"""
        if not tokens:
            return 0
        
        # คะแนนพื้นฐาน: จำนวนคำน้อย = ดี
        base_score = 1000 / len(tokens)
        
        # ลดคะแนนสำหรับตัวอักษรเดี่ยว
        single_char_penalty = sum(1 for token in tokens if len(token) == 1) * 10
        
        # เพิ่มคะแนนสำหรับคำที่อยู่ในพจนานุกรม
        dict_bonus = sum(10 for token in tokens if token in self.dictionary)
        
        # เพิ่มคะแนนสำหรับคำที่มีความถี่สูง
        freq_bonus = sum(self.word_frequencies.get(token, 0) for token in tokens)
        
        return base_score - single_char_penalty + dict_bonus + freq_bonus
    
    def statistical_segmentation(self, text, use_bigrams=True):
        """
        การแยกคำโดยใช้ข้อมูลทางสถิติ
        """
        text = text.lower().strip()
        tokens = []
        i = 0
        
        while i < len(text):
            best_word = ""
            best_score = -1
            
            # ลองแยกคำในความยาวต่างๆ
            for j in range(i, min(i + 10, len(text))):  # จำกัดความยาวสูงสุด
                candidate = text[i:j+1]
                score = self._calculate_word_score(candidate, tokens, use_bigrams)
                
                if score > best_score:
                    best_score = score
                    best_word = candidate
            
            if best_word:
                tokens.append(best_word)
                i += len(best_word)
            else:
                tokens.append(text[i])
                i += 1
        
        return tokens
    
    def _calculate_word_score(self, word, previous_tokens, use_bigrams=True):
        """คำนวณคะแนนของคำตามข้อมูลทางสถิติ"""
        score = 0
        
        # คะแนนจากความถี่ของคำ
        score += self.word_frequencies.get(word, 0)
        
        # คะแนนจากการอยู่ในพจนานุกรม
        if word in self.dictionary:
            score += 100
        
        # คะแนนจาก bigram (ถ้าใช้)
        if use_bigrams and previous_tokens:
            prev_word = previous_tokens[-1]
            bigram_freq = self.bigram_frequencies.get((prev_word, word), 0)
            score += bigram_freq * 10
        
        # ลดคะแนนสำหรับตัวอักษรเดี่ยว
        if len(word) == 1:
            score -= 50
        
        return score
    
    def segment_text(self, text, method='bidirectional'):
        """
        แยกคำด้วยวิธีที่เลือก
        
        Args:
            text (str): ข้อความที่ต้องการแยกคำ
            method (str): 'forward', 'backward', 'bidirectional', 'statistical'
        
        Returns:
            list: รายการคำที่แยกได้
        """
        if method == 'forward':
            return self.maximum_matching(text, 'forward')
        elif method == 'backward':
            return self.maximum_matching(text, 'backward')
        elif method == 'bidirectional':
            result, direction = self.bidirectional_matching(text)
            return result
        elif method == 'statistical':
            return self.statistical_segmentation(text)
        else:
            raise ValueError(f"Unknown method: {method}")

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # สร้าง segmenter
    segmenter = CustomWordSegmenter()
    
    # เพิ่มคำเข้าพจนานุกรม
    english_words = [
        "this", "is", "insane", "the", "cat", "in", "hat", "hello", "world",
        "python", "programming", "natural", "language", "processing",
        "machine", "learning", "artificial", "intelligence", "computer", "science"
    ]
    segmenter.add_words_to_dictionary(english_words)
    
    # ฝึกจากข้อความตัวอย่าง
    training_text = "this is a test hello world python programming natural language processing"
    segmenter.train_from_text(training_text)
    
    # ทดสอบการแยกคำ
    test_texts = [
        "thisisinsane",
        "helloworld", 
        "pythonprogramming",
        "naturallanguageprocessing"
    ]
    
    methods = ['forward', 'backward', 'bidirectional', 'statistical']
    
    for text in test_texts:
        print(f"\n{'='*60}")
        print(f"ข้อความทดสอบ: '{text}'")
        print('='*60)
        
        for method in methods:
            try:
                result = segmenter.segment_text(text, method)
                score = segmenter._calculate_score(result)
                print(f"{method:15}: {' | '.join(result)} (score: {score:.1f})")
            except Exception as e:
                print(f"{method:15}: Error - {e}")
    
    print(f"\n{'='*60}")
    print("สถิติพจนานุกรม:")
    print(f"จำนวนคำในพจนานุกรม: {len(segmenter.dictionary)}")
    print(f"จำนวนคำที่มีความถี่: {len(segmenter.word_frequencies)}")
    print(f"จำนวน bigrams: {len(segmenter.bigram_frequencies)}")
    
    # แสดงคำที่มีความถี่สูงสุด
    if segmenter.word_frequencies:
        top_words = Counter(segmenter.word_frequencies).most_common(5)
        print(f"คำที่มีความถี่สูงสุด: {top_words}")

