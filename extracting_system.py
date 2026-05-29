from retrieving_system import documents
from transformers import pipeline

questions = ["Đại học Quốc gia Hà Nội có tên giao dịch quốc tế là gì?",
             "Sứ mệnh của Đại học Quốc gia Hà Nội là gì?",
             "Giá trị cốt lõi của Trường Đại học Công nghệ là gì?",
             "When was Rafael Nadal born?",
             "How many titles have Novak Djokovic won so far?",
             "¿Cuántos goles ha marcado Cristiano Ronaldo?"
             ]

documents = documents

qa_pipeline = pipeline("question-answering", 'deepset/xlm-roberta-base-squad2')

for question in questions:
    print(question)
    result = qa_pipeline(question, documents)
    print(result)
    print("\n")
