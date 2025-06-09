#!/usr/bin/env python3
"""
Machine Translation Demo Script
ตัวอย่างการใช้งาน Machine Translation ด้วย Python

Author: AI Course Development System
Date: 2025
"""

import time
import warnings
warnings.filterwarnings("ignore")

def demo_basic_translation():
    """Demo 1: การแปลภาษาพื้นฐาน"""
    print("=" * 60)
    print("Demo 1: การแปลภาษาพื้นฐาน")
    print("=" * 60)
    
    try:
        from transformers import pipeline
        
        print("กำลังโหลดโมเดล...")
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-th")
        
        test_sentences = [
            "Hello, how are you?",
            "I love learning about machine translation.",
            "Python is a great programming language.",
            "The weather is beautiful today."
        ]
        
        for sentence in test_sentences:
            start_time = time.time()
            result = translator(sentence)
            end_time = time.time()
            
            print(f"EN: {sentence}")
            print(f"TH: {result[0]['translation_text']}")
            print(f"Time: {end_time - start_time:.2f} seconds")
            print("-" * 50)
            
    except ImportError:
        print("Error: กรุณาติดตั้ง transformers library")
        print("pip install transformers torch")
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_batch_processing():
    """Demo 2: การประมวลผลแบบ Batch"""
    print("=" * 60)
    print("Demo 2: การประมวลผลแบบ Batch")
    print("=" * 60)
    
    try:
        from transformers import pipeline
        import pandas as pd
        
        # สร้างข้อมูลตัวอย่าง
        sample_texts = [
            "Artificial intelligence is transforming industries.",
            "Machine learning algorithms can process vast amounts of data.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning models require significant computational resources.",
            "Translation technology has improved dramatically in recent years."
        ]
        
        print("กำลังโหลดโมเดล...")
        translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        
        print("กำลังแปลข้อมูลแบบ batch...")
        start_time = time.time()
        results = translator(sample_texts)
        end_time = time.time()
        
        # สร้าง DataFrame
        df = pd.DataFrame({
            'English': sample_texts,
            'Thai': [result['translation_text'] for result in results]
        })
        
        print(f"แปลเสร็จสิ้น! ใช้เวลา {end_time - start_time:.2f} วินาที")
        print("\nผลลัพธ์:")
        for i, row in df.iterrows():
            print(f"{i+1}. EN: {row['English']}")
            print(f"   TH: {row['Thai']}")
            print()
            
    except ImportError as e:
        print(f"Error: กรุณาติดตั้ง libraries ที่จำเป็น - {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_evaluation():
    """Demo 3: การประเมินคุณภาพการแปล"""
    print("=" * 60)
    print("Demo 3: การประเมินคุณภาพการแปล")
    print("=" * 60)
    
    try:
        # ข้อมูลตัวอย่างสำหรับการประเมิน
        predictions = [
            "สวัสดี คุณเป็นอย่างไรบ้าง",
            "ฉันชอบเรียนรู้เกี่ยวกับการแปลเครื่อง",
            "ไพธอนเป็นภาษาการเขียนโปรแกรมที่ดี"
        ]
        
        references = [
            "สวัสดี คุณสบายดีไหม",
            "ฉันรักการเรียนรู้เกี่ยวกับการแปลภาษาด้วยเครื่อง",
            "Python เป็นภาษาโปรแกรมมิ่งที่ยอดเยี่ยม"
        ]
        
        # คำนวณ BLEU score แบบง่าย
        def simple_bleu(pred, ref):
            pred_words = pred.split()
            ref_words = ref.split()
            
            # นับคำที่ตรงกัน
            matches = 0
            for word in pred_words:
                if word in ref_words:
                    matches += 1
            
            # คำนวณ precision
            precision = matches / len(pred_words) if pred_words else 0
            return precision
        
        print("การประเมินคุณภาพการแปล:")
        total_score = 0
        
        for i, (pred, ref) in enumerate(zip(predictions, references)):
            score = simple_bleu(pred, ref)
            total_score += score
            
            print(f"\nประโยคที่ {i+1}:")
            print(f"Prediction: {pred}")
            print(f"Reference:  {ref}")
            print(f"Simple BLEU: {score:.4f}")
        
        avg_score = total_score / len(predictions)
        print(f"\nคะแนนเฉลี่ย: {avg_score:.4f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_domain_specific():
    """Demo 4: การแปลเฉพาะโดเมน"""
    print("=" * 60)
    print("Demo 4: การแปลเฉพาะโดเมน (การแพทย์)")
    print("=" * 60)
    
    try:
        from transformers import pipeline
        
        class DomainTranslator:
            def __init__(self, model_name, glossary=None):
                self.translator = pipeline("translation", model=model_name)
                self.glossary = glossary or {}
            
            def preprocess(self, text):
                for source, target in self.glossary.items():
                    text = text.replace(source, f"[TERM_{target}]")
                return text
            
            def postprocess(self, text):
                for source, target in self.glossary.items():
                    text = text.replace(f"[TERM_{target}]", target)
                return text
            
            def translate(self, text):
                preprocessed = self.preprocess(text)
                result = self.translator(preprocessed)[0]['translation_text']
                return self.postprocess(result)
        
        # ศัพท์เฉพาะทางการแพทย์
        medical_glossary = {
            "diagnosis": "การวินิจฉัย",
            "treatment": "การรักษา",
            "symptoms": "อาการ",
            "patient": "ผู้ป่วย",
            "doctor": "แพทย์"
        }
        
        print("กำลังโหลดโมเดลสำหรับโดเมนการแพทย์...")
        medical_translator = DomainTranslator(
            "Helsinki-NLP/opus-mt-en-th",
            medical_glossary
        )
        
        medical_texts = [
            "The doctor will provide a diagnosis after examining the patient.",
            "The treatment for these symptoms is very effective.",
            "The patient should follow the doctor's instructions carefully."
        ]
        
        print("ผลการแปลเฉพาะโดเมนการแพทย์:")
        for text in medical_texts:
            translation = medical_translator.translate(text)
            print(f"EN: {text}")
            print(f"TH: {translation}")
            print("-" * 50)
            
    except ImportError:
        print("Error: กรุณาติดตั้ง transformers library")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """ฟังก์ชันหลักสำหรับรันการ demo ทั้งหมด"""
    print("🌐 Machine Translation Demo")
    print("ตัวอย่างการใช้งาน Machine Translation ด้วย Python")
    print("=" * 60)
    
    demos = [
        ("การแปลภาษาพื้นฐาน", demo_basic_translation),
        ("การประมวลผลแบบ Batch", demo_batch_processing),
        ("การประเมินคุณภาพการแปล", demo_evaluation),
        ("การแปลเฉพาะโดเมน", demo_domain_specific)
    ]
    
    while True:
        print("\nเลือก Demo ที่ต้องการทดสอบ:")
        for i, (name, _) in enumerate(demos, 1):
            print(f"{i}. {name}")
        print("0. ออกจากโปรแกรม")
        
        try:
            choice = int(input("\nกรุณาเลือก (0-4): "))
            
            if choice == 0:
                print("ขอบคุณที่ใช้งาน!")
                break
            elif 1 <= choice <= len(demos):
                print(f"\nกำลังรัน: {demos[choice-1][0]}")
                demos[choice-1][1]()
                input("\nกด Enter เพื่อดำเนินการต่อ...")
            else:
                print("กรุณาเลือกตัวเลขที่ถูกต้อง")
                
        except ValueError:
            print("กรุณาป้อนตัวเลข")
        except KeyboardInterrupt:
            print("\nโปรแกรมถูกยกเลิก")
            break
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {str(e)}")

if __name__ == "__main__":
    main()

