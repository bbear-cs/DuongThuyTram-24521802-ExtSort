# DuongThuyTram-24521802-ExtSort
# 🗂️ Ứng dụng minh hoạ Sắp xếp Ngoại (External Merge Sort)

> Ứng dụng cho phép người dùng chọn tệp dữ liệu nhị phân chứa **số thực double (8 bytes)** và thực hiện **sắp xếp ngoại tăng dần** theo thuật toán **External Merge Sort**, đồng thời minh hoạ quá trình tạo run và trộn nhiều pass.

---

## 📌 Table of Contents
- [Introduction](#introduction)
- [Database](#database)
- [Features](#features)
  - [Major Features](#major-features)
  - [Minor Features](#minor-features)
- [How it works](#how-it-works)
- [Installation](#installation)
- [How to run](#how-to-run)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
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

![ERD](photo/database.png)

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
