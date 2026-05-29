from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import glob
import fitz

# KHÁC BIỆT Ở ĐÂY: Thay đổi tên mô hình thành BAAI/bge-m3
# Mô hình này hỗ trợ tốt cả tiếng Anh và tiếng Việt
model = SentenceTransformer('BAAI/bge-m3')

# 1. Khởi tạo một mảng (list) rỗng để chứa tất cả các đoạn văn
documents = []

# 2. Tìm tất cả các file có đuôi .txt trong thư mục hiện tại
cac_file_txt = glob.glob("raw_data/*.txt")
cac_file_pdf = glob.glob("raw_data/*.pdf")

print(f"Tìm thấy {len(cac_file_txt)} file .txt và {len(cac_file_pdf)} file .pdf. Đang tiến hành đọc dữ liệu...\n")

# 3. Duyệt qua từng file để đọc nội dung
for ten_file in cac_file_txt:
    # Mở file ở chế độ 'r' (read - đọc)
    with open(ten_file, 'r', encoding='utf-8') as f:
        # Đọc tất cả các dòng trong file
        lines = f.readlines()

        for line in lines:
            text = line.strip()  # Cắt bỏ khoảng trắng và dấu xuống dòng thừa

            # Chỉ đưa vào mảng nếu dòng đó có chữ (không rỗng)
            # VÀ không phải là dòng kẻ phân cách (ví dụ: '---') mà chúng ta có thể đã tạo trước đó
            if text and not text.startswith('---'):
                documents.append(text)

for file_pdf in cac_file_pdf:
    with fitz.open(file_pdf) as pdf:
        for trang in pdf:
            cac_doan = trang.get_text().split('\n')
            for doan in cac_doan:
                chu_sach = doan.strip()
                if chu_sach:
                    documents.append(chu_sach)

# 4. Kiểm tra kết quả
print(f"Tổng số đoạn văn đã gom được vào mảng: {len(documents)}")

# In thử 3 đoạn văn đầu tiên trong mảng để kiểm tra
print("\n--- 3 phần tử đầu tiên trong mảng ---")
for i in range(min(3, len(documents))):
    print(f"Phần tử {i}: {documents[i]}")

# Mã hóa tài liệu thành vectors
doc_embeddings = model.encode(documents, convert_to_tensor=True)

# Tạo chỉ mục FAISS để tìm kiếm
# Lưu ý: shape[1] sẽ tự động lấy kích thước vector của mô hình BGE (1024 chiều thay vì 384 chiều như MiniLM)
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings.cpu().detach().numpy())

print("Đã tạo chỉ mục FAISS thành công với mô hình BAAI/bge-m3!")

questions = ["Đại học Quốc gia Hà Nội có tên giao dịch quốc tế là gì?",
             "Sứ mệnh của Đại học Quốc gia Hà Nội là gì?",
             "Giá trị cốt lõi của Trường Đại học Công nghệ là gì?",
             "When was Rafael Nadal born?",
             "How many titles have Novak Djokovic won so far?",
             "¿Cuántos goles ha marcado Cristiano Ronaldo?"
             ]

questions_embeddings = model.encode(questions, convert_to_tensor=True)

i = 0
for q_embed in questions_embeddings:
    D, I = index.search(q_embed.cpu().detach().numpy().reshape(1, -1), k=1)
    answer = documents[I[0][0]]
    print(f"\nCâu trả lời cho câu hỏi số {i + 1} là: \n {answer} \n")
    i = i + 1
