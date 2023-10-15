import bs4
import requests
import pandas as pd

def scrap_fbref(table_id):
    # Tìm bảng với ID tương ứng 
    table_overall = soup.find(id=table_id)
    headers_table_overall = []
    # Lấy tiêu đề của các cột từ thẻ <thead>
    for i in table_overall.select("thead tr:not(.over_header) th"):
        title = i.text
        headers_table_overall.append(title)

    # Tạo DataFrame để lưu dữ liệu
    df_table_overall = pd.DataFrame(columns=headers_table_overall)
    
    # Lặp qua từng hàng dữ liệu (tr) trong bảng
    for j in table_overall.select("tbody tr"):
        # Tìm tất cả thẻ <th> và <td> trong hàng
        row_rank = j.find_all("th")
        row_data = j.find_all("td")
        
        # Tạo danh sách dữ liệu cho hàng này bằng cách lấy nội dung từ thẻ <th> và <td>
        row = [i.text for i in row_rank + row_data]
        
        # Thêm hàng dữ liệu này vào DataFrame
        df_table_overall.loc[len(df_table_overall)] = row

    # Lưu dữ liệu vào tệp CSV với tên dựa trên ID bảng
    csv_file_name = table_id + ".csv"
    df_table_overall.to_csv(csv_file_name)

# URL của trang web chứa dữ liệu
EPL_DATA = "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"
# Gửi yêu cầu HTTP để tải trang web
response = requests.get(EPL_DATA)
# Phân tích HTML bằng BeautifulSoup
soup = bs4.BeautifulSoup(response.text, 'html.parser')

# Danh sách các ID bảng bạn muốn crawl dữ liệu
table_ids = ["results2022-202391_overall", "results2022-202391_home_away"]

# Lặp qua danh sách ID bảng và gọi hàm để crawl và lưu dữ liệu vào tệp CSV
for table_id in table_ids:
    scrap_fbref(table_id)
