# โปรเจกต์ปฏิบัติ: ระบบวิเคราะห์ข้อความภาษาไทย

"""
โปรเจกต์ปฏิบัติ: ระบบวิเคราะห์ข้อความภาษาไทย

วัตถุประสงค์:
1. สร้างระบบวิเคราะห์ข้อความที่ครอบคลุม
2. ประยุกต์ใช้ความรู้เกี่ยวกับ Word Segmentation
3. สร้าง GUI หรือ Web Interface (ขั้นสูง)
4. ฝึกการทำงานกับข้อมูลจริง

คำแนะนำ:
- เริ่มจากฟังก์ชันพื้นฐานก่อน
- ทดสอบทีละส่วน
- ปรับปรุงและเพิ่มฟีเจอร์ตามต้องการ
"""

import sys
import json
from collections import Counter, defaultdict
from datetime import datetime
import re

# ติดตั้ง dependencies
try:
    from pythainlp.tokenize import word_tokenize
    from pythainlp.corpus import thai_stopwords
    from pythainlp.util import normalize
    from pythainlp.tag import pos_tag
except ImportError:
    print("กำลังติดตั้ง PyThaiNLP...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythainlp"])
    from pythainlp.tokenize import word_tokenize
    from pythainlp.corpus import thai_stopwords
    from pythainlp.util import normalize
    from pythainlp.tag import pos_tag

class ThaiTextAnalysisSystem:
    """
    ระบบวิเคราะห์ข้อความภาษาไทยแบบครอบคลุม
    """
    
    def __init__(self, default_engine='newmm'):
        self.default_engine = default_engine
        self.stopwords = thai_stopwords()
        self.analysis_history = []
        
        # สถิติระบบ
        self.system_stats = {
            'total_analyses': 0,
            'total_texts_processed': 0,
            'total_words_processed': 0,
            'engines_used': defaultdict(int)
        }
    
    def preprocess_text(self, text):
        """
        ปรับปรุงข้อความก่อนการวิเคราะห์
        """
        if not text or not isinstance(text, str):
            return ""
        
        # ลบช่องว่างส่วนเกิน
        text = re.sub(r'\s+', ' ', text.strip())
        
        # ใช้ normalize ของ PyThaiNLP
        try:
            text = normalize(text)
        except:
            pass
        
        return text
    
    def tokenize_with_multiple_engines(self, text, engines=['newmm', 'longest']):
        """
        แยกคำด้วย engine หลายตัวและเปรียบเทียบ
        """
        results = {}
        
        for engine in engines:
            try:
                tokens = word_tokenize(text, engine=engine)
                results[engine] = {
                    'tokens': tokens,
                    'word_count': len(tokens),
                    'unique_words': len(set(tokens)),
                    'avg_word_length': sum(len(token) for token in tokens) / len(tokens) if tokens else 0
                }
                self.system_stats['engines_used'][engine] += 1
            except Exception as e:
                results[engine] = {'error': str(e)}
        
        return results
    
    def extract_content_words(self, tokens):
        """
        สกัดคำสำคัญ (ไม่รวม stopwords และคำที่ไม่สำคัญ)
        """
        content_words = []
        stopwords_found = []
        
        for token in tokens:
            token = token.strip()
            if not token:
                continue
                
            if token in self.stopwords:
                stopwords_found.append(token)
            elif len(token) > 1 and not re.match(r'^[0-9\W]+$', token):
                content_words.append(token)
        
        return content_words, stopwords_found
    
    def calculate_text_statistics(self, text, tokens):
        """
        คำนวณสถิติต่างๆ ของข้อความ
        """
        content_words, stopwords_found = self.extract_content_words(tokens)
        
        stats = {
            'character_count': len(text),
            'word_count': len(tokens),
            'content_word_count': len(content_words),
            'stopword_count': len(stopwords_found),
            'unique_words': len(set(tokens)),
            'unique_content_words': len(set(content_words)),
            'avg_word_length': sum(len(token) for token in tokens) / len(tokens) if tokens else 0,
            'content_ratio': len(content_words) / len(tokens) if tokens else 0,
            'word_frequency': Counter(content_words),
            'stopwords_found': stopwords_found
        }
        
        return stats
    
    def analyze_single_text(self, text, engine=None, include_pos=False):
        """
        วิเคราะห์ข้อความเดี่ยวอย่างละเอียด
        """
        if engine is None:
            engine = self.default_engine
        
        # เตรียมข้อความ
        original_text = text
        processed_text = self.preprocess_text(text)
        
        if not processed_text:
            return {'error': 'ข้อความว่างหรือไม่ถูกต้อง'}
        
        # แยกคำ
        tokens = word_tokenize(processed_text, engine=engine)
        
        # คำนวณสถิติ
        stats = self.calculate_text_statistics(processed_text, tokens)
        
        # วิเคราะห์ POS (ถ้าต้องการ)
        pos_analysis = None
        if include_pos:
            try:
                pos_tags = pos_tag(tokens, engine='perceptron')
                pos_analysis = {
                    'pos_tags': pos_tags,
                    'pos_distribution': Counter([tag for word, tag in pos_tags])
                }
            except Exception as e:
                pos_analysis = {'error': str(e)}
        
        # สร้างผลลัพธ์
        result = {
            'timestamp': datetime.now().isoformat(),
            'original_text': original_text,
            'processed_text': processed_text,
            'engine_used': engine,
            'tokens': tokens,
            'statistics': stats,
            'pos_analysis': pos_analysis
        }
        
        # บันทึกประวัติ
        self.analysis_history.append(result)
        self.system_stats['total_analyses'] += 1
        self.system_stats['total_texts_processed'] += 1
        self.system_stats['total_words_processed'] += len(tokens)
        
        return result
    
    def analyze_multiple_texts(self, texts, engine=None):
        """
        วิเคราะห์ข้อความหลายข้อความพร้อมกัน
        """
        results = []
        combined_stats = {
            'total_texts': len(texts),
            'total_words': 0,
            'total_content_words': 0,
            'combined_word_frequency': Counter(),
            'engine_comparison': {}
        }
        
        for i, text in enumerate(texts):
            result = self.analyze_single_text(text, engine)
            results.append(result)
            
            if 'error' not in result:
                combined_stats['total_words'] += result['statistics']['word_count']
                combined_stats['total_content_words'] += result['statistics']['content_word_count']
                combined_stats['combined_word_frequency'].update(result['statistics']['word_frequency'])
        
        # เปรียบเทียบ engine (ถ้ามีข้อความมากกว่า 1 ข้อความ)
        if len(texts) > 0 and 'error' not in results[0]:
            sample_text = texts[0]
            engine_comparison = self.tokenize_with_multiple_engines(sample_text)
            combined_stats['engine_comparison'] = engine_comparison
        
        return {
            'individual_results': results,
            'combined_statistics': combined_stats,
            'top_words': combined_stats['combined_word_frequency'].most_common(20)
        }
    
    def generate_report(self, analysis_result, format='text'):
        """
        สร้างรายงานจากผลการวิเคราะห์
        """
        if format == 'text':
            return self._generate_text_report(analysis_result)
        elif format == 'json':
            return json.dumps(analysis_result, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_text_report(self, result):
        """
        สร้างรายงานแบบข้อความ
        """
        if 'error' in result:
            return f"ข้อผิดพลาด: {result['error']}"
        
        report = []
        report.append("=== รายงานการวิเคราะห์ข้อความภาษาไทย ===")
        report.append(f"เวลา: {result['timestamp']}")
        report.append(f"Engine: {result['engine_used']}")
        report.append("")
        
        report.append("ข้อความต้นฉบับ:")
        report.append(f"'{result['original_text']}'")
        report.append("")
        
        if result['processed_text'] != result['original_text']:
            report.append("ข้อความหลังปรับปรุง:")
            report.append(f"'{result['processed_text']}'")
            report.append("")
        
        report.append("ผลการแยกคำ:")
        report.append(" | ".join(result['tokens']))
        report.append("")
        
        stats = result['statistics']
        report.append("สถิติ:")
        report.append(f"  จำนวนตัวอักษร: {stats['character_count']}")
        report.append(f"  จำนวนคำทั้งหมด: {stats['word_count']}")
        report.append(f"  จำนวนคำสำคัญ: {stats['content_word_count']}")
        report.append(f"  จำนวน stopwords: {stats['stopword_count']}")
        report.append(f"  จำนวนคำที่ไม่ซ้ำ: {stats['unique_words']}")
        report.append(f"  ความยาวเฉลี่ยของคำ: {stats['avg_word_length']:.2f}")
        report.append(f"  อัตราส่วนคำสำคัญ: {stats['content_ratio']:.2%}")
        report.append("")
        
        if stats['word_frequency']:
            report.append("คำที่พบบ่อย (top 10):")
            for word, freq in stats['word_frequency'].most_common(10):
                report.append(f"  {word}: {freq}")
            report.append("")
        
        if result['pos_analysis'] and 'error' not in result['pos_analysis']:
            report.append("การวิเคราะห์ชนิดของคำ:")
            pos_dist = result['pos_analysis']['pos_distribution']
            for pos, count in pos_dist.most_common():
                report.append(f"  {pos}: {count}")
            report.append("")
        
        return "\n".join(report)
    
    def get_system_statistics(self):
        """
        ดูสถิติการใช้งานระบบ
        """
        return {
            'system_stats': self.system_stats,
            'history_count': len(self.analysis_history),
            'available_engines': ['newmm', 'longest', 'icu', 'attacut'],
            'last_analysis': self.analysis_history[-1]['timestamp'] if self.analysis_history else None
        }
    
    def save_analysis_history(self, filename):
        """
        บันทึกประวัติการวิเคราะห์ลงไฟล์
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_history, f, ensure_ascii=False, indent=2)
            return f"บันทึกประวัติ {len(self.analysis_history)} รายการลงไฟล์ {filename}"
        except Exception as e:
            return f"ข้อผิดพลาดในการบันทึก: {e}"

# ===== ตัวอย่างการใช้งาน =====
def demo_analysis_system():
    """
    สาธิตการใช้งานระบบวิเคราะห์ข้อความ
    """
    print("=== สาธิตระบบวิเคราะห์ข้อความภาษาไทย ===\n")
    
    # สร้างระบบ
    analyzer = ThaiTextAnalysisSystem()
    
    # ข้อความทดสอบ
    sample_texts = [
        "นักเรียนไปโรงเรียนเพื่อเรียนหนังสือทุกวัน",
        "วันนี้อากาศดีมากเหมาะสำหรับการเดินทางท่องเที่ยว",
        "การประมวลผลภาษาธรรมชาติเป็นสาขาที่น่าสนใจและมีประโยชน์",
        "ฉันชอบกินข้าวผัดและส้มตำมากที่สุด"
    ]
    
    # วิเคราะห์ข้อความเดี่ยว
    print("1. การวิเคราะห์ข้อความเดี่ยว:")
    result = analyzer.analyze_single_text(sample_texts[0], include_pos=True)
    print(analyzer.generate_report(result))
    
    # วิเคราะห์ข้อความหลายข้อความ
    print("\n2. การวิเคราะห์ข้อความหลายข้อความ:")
    batch_result = analyzer.analyze_multiple_texts(sample_texts)
    
    print(f"จำนวนข้อความ: {batch_result['combined_statistics']['total_texts']}")
    print(f"จำนวนคำรวม: {batch_result['combined_statistics']['total_words']}")
    print(f"จำนวนคำสำคัญรวม: {batch_result['combined_statistics']['total_content_words']}")
    
    print("\nคำที่พบบ่อยที่สุด:")
    for word, freq in batch_result['top_words'][:10]:
        print(f"  {word}: {freq}")
    
    # เปรียบเทียบ engine
    print("\n3. การเปรียบเทียบ engine:")
    comparison = batch_result['combined_statistics']['engine_comparison']
    for engine, data in comparison.items():
        if 'error' not in data:
            print(f"  {engine}: {data['word_count']} คำ, {data['unique_words']} คำไม่ซ้ำ")
        else:
            print(f"  {engine}: {data['error']}")
    
    # สถิติระบบ
    print("\n4. สถิติระบบ:")
    sys_stats = analyzer.get_system_statistics()
    print(f"  การวิเคราะห์ทั้งหมด: {sys_stats['system_stats']['total_analyses']}")
    print(f"  ข้อความที่ประมวลผล: {sys_stats['system_stats']['total_texts_processed']}")
    print(f"  คำที่ประมวลผล: {sys_stats['system_stats']['total_words_processed']}")
    
    # บันทึกประวัติ
    save_result = analyzer.save_analysis_history('analysis_history.json')
    print(f"\n5. การบันทึกประวัติ: {save_result}")

# ===== Interactive Mode =====
def interactive_mode():
    """
    โหมดการใช้งานแบบ interactive
    """
    analyzer = ThaiTextAnalysisSystem()
    
    print("=== โหมดการใช้งานแบบ Interactive ===")
    print("พิมพ์ 'quit' เพื่อออก, 'help' เพื่อดูคำสั่ง")
    
    while True:
        try:
            user_input = input("\nกรุณาใส่ข้อความที่ต้องการวิเคราะห์: ").strip()
            
            if user_input.lower() == 'quit':
                print("ขอบคุณที่ใช้งาน!")
                break
            elif user_input.lower() == 'help':
                print("คำสั่งที่ใช้ได้:")
                print("  - ใส่ข้อความเพื่อวิเคราะห์")
                print("  - 'stats' เพื่อดูสถิติระบบ")
                print("  - 'history' เพื่อดูประวัติ")
                print("  - 'quit' เพื่อออก")
                continue
            elif user_input.lower() == 'stats':
                stats = analyzer.get_system_statistics()
                print(f"การวิเคราะห์ทั้งหมด: {stats['system_stats']['total_analyses']}")
                print(f"คำที่ประมวลผล: {stats['system_stats']['total_words_processed']}")
                continue
            elif user_input.lower() == 'history':
                print(f"ประวัติการวิเคราะห์: {len(analyzer.analysis_history)} รายการ")
                if analyzer.analysis_history:
                    last = analyzer.analysis_history[-1]
                    print(f"ล่าสุด: '{last['original_text'][:50]}...' ({last['timestamp']})")
                continue
            
            if not user_input:
                print("กรุณาใส่ข้อความ")
                continue
            
            # วิเคราะห์ข้อความ
            result = analyzer.analyze_single_text(user_input)
            print("\n" + analyzer.generate_report(result))
            
        except KeyboardInterrupt:
            print("\n\nขอบคุณที่ใช้งาน!")
            break
        except Exception as e:
            print(f"ข้อผิดพลาด: {e}")

if __name__ == "__main__":
    print("เลือกโหมดการใช้งาน:")
    print("1. สาธิตระบบ (Demo)")
    print("2. โหมด Interactive")
    
    try:
        choice = input("เลือก (1 หรือ 2): ").strip()
        
        if choice == "1":
            demo_analysis_system()
        elif choice == "2":
            interactive_mode()
        else:
            print("เริ่มโหมดสาธิต...")
            demo_analysis_system()
            
    except KeyboardInterrupt:
        print("\nขอบคุณที่ใช้งาน!")
    except Exception as e:
        print(f"ข้อผิดพลาด: {e}")
        print("เริ่มโหมดสาธิต...")
        demo_analysis_system()

