# DuongThuyTram-24521802-ExtSort
# 🗂️ Ứng dụng minh hoạ Sắp xếp Ngoại (External Merge Sort)

> Xây dựng ứng dụng cho phép người dùng chọn lựa tập tin dữ liệu nguồn và sắp xếp dữ liệu trong tập tin này tăng dần. 

Tập tin lưu dữ liệu là các số thực (8bytes) ở dạng tập tin nhị phân

Chương trình cần minh họa quá trình sắp xếp với các tập tin có kích thước nhỏ.

---

## 📌 Table of Contents
- [Introduction](#introduction)
- [Database](#database)
- [Features](#features)
  - [Major Features](#major-features)
  - [Minor Features](#minor-features)
- [How it works](#how-it-works)
- [How to run](#how-to-run)
- [Author](#author)

---

## Introduction
Chào các bạn, mình là **<Tên bạn>**, MSSV **<MSSV>**, lớp **<Lớp>**.

Đồ án này xây dựng ứng dụng minh hoạ **sắp xếp ngoại tối hạn**:
- Input: tệp `.bin` chứa các số thực `double` (8 bytes) dạng nhị phân
- Output: tệp `.bin` đã được sắp xếp tăng dần
- Minh hoạ: tạo các run nhỏ (sort trong RAM) và trộn nhiều lượt (pass merge)

---

## Database
Phần database (ERD) dùng để mô tả **hướng thiết kế** các thực thể trong quá trình sắp xếp.

> ✅ Chèn ảnh ERD tại đây:

![ERD](photo/Screenshot 2026-03-03 234012.png)

---

## Features

### Major Features
1. Chọn file input `.bin` (double 8 bytes)
2. Thiết lập `KichThuocRun` và `KichThuocBoDem`
3. Sắp xếp ngoại tăng dần (External Merge Sort)
4. Hiển thị log minh hoạ: tạo run + merge pass
5. Xuất kết quả: `sorted.bin` và `ketqua_sorted.txt`

### Minor Features
1. Tạo demo input nhanh (random doubles)
2. Preview kết quả đã sắp xếp trên giao diện
3. Tự tạo thư mục `runs/` và `temp/` để minh hoạ

---

## How it works
### Phase 1 — Create Runs
- Đọc lần lượt `KichThuocRun` số từ input
- Sort trong RAM
- Ghi ra file `runs/run_###.bin`

### Phase 2 — Merge Passes
- Trộn từng cặp run (2-way merge) bằng buffer nhỏ
- Mỗi pass tạo ra các file `temp/pass_i_###.bin`
- Lặp cho đến khi còn 1 file cuối → ghi ra output `sorted.bin`

---

## Installation
Yêu cầu:
- Python 3.9+ (hoặc 3.10+)
- Tkinter (Windows thường có sẵn)

Cài đặt (nếu cần):
```bash
python --version
