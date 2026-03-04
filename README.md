# DuongThuyTram-24521802-ExtSort
# 🗂️ Ứng dụng minh hoạ Sắp xếp Ngoại (External Merge Sort)

> Xây dựng ứng dụng cho phép người dùng chọn lựa tập tin dữ liệu nguồn và sắp xếp dữ liệu trong tập tin này tăng dần. 

Tập tin lưu dữ liệu là các số thực (8bytes) ở dạng tập tin nhị phân

Chương trình cần minh họa quá trình sắp xếp với các tập tin có kích thước nhỏ.

---

## 📌 Table of Contents
- [Introduction](#introduction)
- [Database](#database)
- [Base-lined knowledge](#base-lined-knowledge) 
- [Features](#features)
  - [Major Features](#major-features)
  - [Minor Features](#minor-features)
- [How to run](#how-to-run)
- [Author](#author)

---

## Introduction
Em tên: **<Dương Thùy Trâm>** , MSSV **<24521802>**, lớp **<CS523.Q21>**.

Sau đây là bảng mô tả cách xây dựng ứng dụng minh hoạ sắp xếp ngoại
- Input: tệp `.bin` chứa các số thực `double` (8 bytes) dạng nhị phân
- Output: tệp `.bin` đã được sắp xếp tăng dần
- Minh hoạ: tạo các run nhỏ (sort trong RAM) và trộn nhiều lượt (pass merge)

---

## Database
Phần database (ERD) dùng để mô tả các “thành phần” trong quá trình sắp xếp ngoại và mối quan hệ giữa chúng, ví dụ: một phiên sắp xếp sẽ tạo ra nhiều run, mỗi lượt trộn sẽ ghép các run lại, cuối cùng sinh ra tệp kết quả đã sắp xếp.

![ERD](database/database.png)

---
## Base-lined knowledge

### 1) Kiến thức về dữ liệu & file nhị phân
- **Tệp nhị phân (.bin)**: dữ liệu được lưu dưới dạng byte (không phải text)
- **Double (8 bytes)**: mỗi số thực `double` chiếm đúng 8 byte; khi đọc/ghi cần đọc theo bội số của 8
- **File I/O**: thao tác đọc/ghi file nhị phân (binary read/write), đọc theo khối (block) thay vì đọc từng byte

### 2) Kiến thức thuật toán sắp xếp
- **Sắp xếp trong bộ nhớ **
- **External Merge Sort (sắp xếp ngoại)**

### 3) Kiến thức về SQL
- ERD : hiểu khái niệm thực thể, thuộc tính và mối quan hệ (1–n, n–n)
- **Khoá chính (Primary Key) & Khoá ngoại (Foreign Key)**: dùng để liên kết các bảng và thể hiện quan hệ giữa thực thể
- SQL cơ bản

> Chú thích: ERD trong đồ án dùng để mô tả hướng thiết kế và xử lý của chương trình (Tệp → PhiênSắpXếp → Run → LượtTrộn → KếtQuả)
---

## Features

### Major Features
1. Chọn file input `.bin` (double 8 bytes) nếu có sẵn
2. Chỉnh sửa cấu hình tham số với  `KichThuocRun` và `KichThuocBoDem`
3. Dùng thuật toán sắp xếp ngoại (External Merge Sort) để sắp xếp
4. Hiển thị log minh hoạ: tạo run + merge pass
5. Hiển thị kết quả: `sorted.bin` và `ketqua_sorted.txt`

### Minor Features
1. Cho phép người dùng tạo demo input nhanh (random doubles) nếu không có dữ liệu sẵn 
2. Hiển thị kết quả đã sắp xếp trên giao diện

---

## How to run
1. Có hai cách để đưa dữ liệu vào :
- Chọn file có sẵn nếu có
- Có thể demo input nhanh

![ERD](photo/1.1.jpg)

2. Chọn nơi lưu output

![ERD](photo/1.2.jpg)\

3.Bấm SORT

![ERD](photo/1.3.jpg)

4. Hiển thị kết quả

![ERD](photo/1.4.jpg)

5 Xuất kết quả ra file txt để xem hết

![ERD](photo/1.5.jpg)
![ERD](photo/1.6.jpg)

---

## Installation
Yêu cầu:
- Python 3.9+ (hoặc 3.10+)
- Tkinter (Windows thường có sẵn)

Cài đặt (nếu cần):
```bash
python --version
