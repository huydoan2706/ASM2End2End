import requests
from bs4 import BeautifulSoup

# 1. Gửi yêu cầu đến trang web
urls = ['https://vnu.edu.vn/dao-tao/gioi-thieu-chung',
        'https://vnu.edu.vn/gioi-thieu/tong-quan/lich-su',
        'https://vnu.edu.vn/gioi-thieu/tong-quan/su-mang-tam-nhin',
        'https://vnu.edu.vn/khoa-hoc-cong-nghe/gioi-thieu-chung',
        'https://vnu.edu.vn/khoa-hoc-cong-nghe/chien-luoc-khcndmst-20212030',
        'https://uet.vnu.edu.vn/gioi-thieu/',
        'https://vnu.edu.vn/hop-tac-phat-trien/gioi-thieu-chung/loi-gioi-thieu',
        'https://vnu.edu.vn/sinh-vien/gioi-thieu-chung',
        'https://vnu.edu.vn/can-bo/gioi-thieu-chung',
        'https://uet.vnu.edu.vn/dao-tao/',
        'https://uet.vnu.edu.vn/tuyen-sinh/',
        'https://uet.vnu.edu.vn/nghien-cuu-doi-moi/'
        ]

i = 0

for url in urls:
    response = requests.get(url)

    # Kiểm tra xem yêu cầu có thành công không (mã 200 là thành công)
    if response.status_code == 200:
        # 2. Phân tích mã nguồn HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lấy tất cả các thẻ <p>
        paragraphs = soup.find_all('p')
        # paragraphs = soup.find_all()

        # In ra văn bản của từng thẻ
        for p in paragraphs:
            # Lệnh .text giúp loại bỏ các mã HTML, chỉ giữ lại phần chữ
            print(p.text.strip())

        with open(f'raw_data/document_{i}.txt', 'w', encoding='utf-8') as f:
            for p in paragraphs:
                text = p.get_text().strip()
                if text:  # Chỉ ghi nếu đoạn văn không rỗng
                    f.write(text + '\n')  # Thêm dấu xuống dòng sau mỗi đoạn
                    # f.write('-' * 20 + '\n')  # (Tùy chọn) Thêm đường kẻ phân cách

        print("Đã lưu file thành công!")
    else:
        print("Không thể truy cập trang web.")

    i = i + 1