import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List

DOUBLE_SIZE = 8
DOUBLE_FMT = "<d"  # little-endian double


def read_doubles(fin, n: int) -> List[float]:
    data = fin.read(n * DOUBLE_SIZE)
    if not data:
        return []
    m = len(data) // DOUBLE_SIZE
    if m <= 0:
        return []
    return list(struct.unpack("<" + "d" * m, data[: m * DOUBLE_SIZE]))


def write_doubles(fout, arr: List[float]) -> None:
    if not arr:
        return
    fout.write(struct.pack("<" + "d" * len(arr), *arr))


class BufReader:
    def __init__(self, path: str, cap: int):
        self.f = open(path, "rb")
        self.cap = cap
        self.buf: List[float] = []
        self.pos = 0
        self.done = False
        self._refill()

    def _refill(self):
        self.buf = read_doubles(self.f, self.cap)
        self.pos = 0
        if not self.buf:
            self.done = True

    def has(self) -> bool:
        return not self.done

    def peek(self) -> float:
        return self.buf[self.pos]

    def pop(self):
        self.pos += 1
        if self.pos >= len(self.buf):
            self._refill()

    def close(self):
        self.f.close()


def merge_two_files(a: str, b: str, out_path: str, buf_cap: int):
    ra = BufReader(a, buf_cap)
    rb = BufReader(b, buf_cap)

    out_buf: List[float] = []
    with open(out_path, "wb") as fout:

        def flush():
            nonlocal out_buf
            write_doubles(fout, out_buf)
            out_buf = []

        while ra.has() and rb.has():
            if ra.peek() <= rb.peek():
                out_buf.append(ra.peek())
                ra.pop()
            else:
                out_buf.append(rb.peek())
                rb.pop()
            if len(out_buf) >= buf_cap:
                flush()

        while ra.has():
            out_buf.append(ra.peek())
            ra.pop()
            if len(out_buf) >= buf_cap:
                flush()

        while rb.has():
            out_buf.append(rb.peek())
            rb.pop()
            if len(out_buf) >= buf_cap:
                flush()

        flush()

    ra.close()
    rb.close()


def preview_list(arr: List[float], k: int = 20) -> str:
    if len(arr) <= k:
        return ", ".join(str(x) for x in arr)
    return ", ".join(str(x) for x in arr[:k]) + f" ... ({len(arr)} so)"


class ExternalSortGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minh hoa Sap xep Ngoai (External Merge Sort) - double 8 bytes")
        self.geometry("980x620")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value="sorted.bin")
        self.run_size = tk.StringVar(value="10")
        self.buf_size = tk.StringVar(value="8")

        # ---- Top: file pickers ----
        frm_top = tk.Frame(self)
        frm_top.pack(fill="x", padx=10, pady=8)

        tk.Label(frm_top, text="Input .bin:").grid(row=0, column=0, sticky="w")
        tk.Entry(frm_top, textvariable=self.input_path, width=80).grid(row=0, column=1, padx=6)
        tk.Button(frm_top, text="Browse...", command=self.browse_input).grid(row=0, column=2)

        tk.Label(frm_top, text="Output .bin:").grid(row=1, column=0, sticky="w", pady=6)
        tk.Entry(frm_top, textvariable=self.output_path, width=80).grid(row=1, column=1, padx=6)
        tk.Button(frm_top, text="Save as...", command=self.browse_output).grid(row=1, column=2)

        # ---- Params ----
        frm_params = tk.Frame(self)
        frm_params.pack(fill="x", padx=10)

        tk.Label(frm_params, text="KichThuocRun (so double/run):").grid(row=0, column=0, sticky="w")
        tk.Entry(frm_params, textvariable=self.run_size, width=10).grid(row=0, column=1, padx=6)

        tk.Label(frm_params, text="KichThuocBoDem (so double/buffer):").grid(row=0, column=2, sticky="w")
        tk.Entry(frm_params, textvariable=self.buf_size, width=10).grid(row=0, column=3, padx=6)

        tk.Button(frm_params, text="Tao demo input", command=self.make_demo).grid(row=0, column=4, padx=12)
        tk.Button(frm_params, text="SORT", command=self.sort_clicked, bg="#2ecc71").grid(row=0, column=5, padx=6)

        # ---- Middle: log + result ----
        frm_mid = tk.Frame(self)
        frm_mid.pack(fill="both", expand=True, padx=10, pady=8)

        frm_log = tk.LabelFrame(frm_mid, text="Log minh hoa (Run / Pass merge)")
        frm_log.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.txt_log = tk.Text(frm_log, wrap="word")
        self.txt_log.pack(fill="both", expand=True)
        self.txt_log.insert("end", "San sang.\n")

        frm_res = tk.LabelFrame(frm_mid, text="Ket qua da sap xep (preview)")
        frm_res.pack(side="right", fill="both", expand=False)

        self.lst_res = tk.Listbox(frm_res, width=40, height=25)
        self.lst_res.pack(padx=8, pady=8, fill="both", expand=True)

        frm_res_btn = tk.Frame(frm_res)
        frm_res_btn.pack(fill="x", padx=8, pady=(0, 8))

        tk.Button(frm_res_btn, text="Xuat ketqua_sorted.txt", command=self.export_txt).pack(side="left")
        tk.Button(frm_res_btn, text="Clear", command=lambda: self.lst_res.delete(0, "end")).pack(side="right")

        self.sorted_values_cache: List[float] = []

    # ---------- UI helpers ----------
    def log(self, s: str):
        self.txt_log.insert("end", s + "\n")
        self.txt_log.see("end")
        self.update_idletasks()

    def browse_input(self):
        p = filedialog.askopenfilename(
            title="Chon file input .bin",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if p:
            self.input_path.set(p)

    def browse_output(self):
        p = filedialog.asksaveasfilename(
            title="Chon noi luu output .bin",
            defaultextension=".bin",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if p:
            self.output_path.set(p)

    def make_demo(self):
        p = filedialog.asksaveasfilename(
            title="Luu demo input .bin",
            defaultextension=".bin",
            initialfile="input_demo.bin",
            filetypes=[("Binary files", "*.bin")]
        )
        if not p:
            return

        import random
        random.seed(42)
        arr = [random.uniform(-100, 100) for _ in range(60)]
        with open(p, "wb") as f:
            write_doubles(f, arr)

        self.input_path.set(p)
        self.log(f"[INFO] Da tao demo: {p} (60 doubles)")
        self.log(f"[INFO] Preview input: {preview_list(arr, 20)}")

    # ---------- Core sort ----------
    def create_runs(self, inp: str, run_size: int, run_dir: str) -> List[str]:
        os.makedirs(run_dir, exist_ok=True)
        runs = []
        with open(inp, "rb") as fin:
            idx = 0
            while True:
                chunk = read_doubles(fin, run_size)
                if not chunk:
                    break
                chunk.sort()

                run_path = os.path.join(run_dir, f"run_{idx:03d}.bin")
                with open(run_path, "wb") as fout:
                    write_doubles(fout, chunk)

                runs.append(run_path)
                self.log(f"[INFO] Tao Run #{idx+1}: {run_path} | count={len(chunk)} | {preview_list(chunk, 20)}")
                idx += 1

        self.log(f"[INFO] Phase 1 xong: Tong so Run = {len(runs)}")
        return runs

    def merge_passes(self, runs: List[str], buf_size: int, temp_dir: str) -> str:
        os.makedirs(temp_dir, exist_ok=True)
        pass_no = 1
        while len(runs) > 1:
            new_runs = []
            out_idx = 0
            i = 0
            while i < len(runs):
                if i + 1 >= len(runs):
                    new_runs.append(runs[i])
                    i += 1
                    continue

                out_path = os.path.join(temp_dir, f"pass_{pass_no}_{out_idx:03d}.bin")
                self.log(f"[INFO] Pass {pass_no}: merge")
                self.log(f"       A={runs[i]}")
                self.log(f"       B={runs[i+1]}")
                self.log(f"       -> {out_path}")

                merge_two_files(runs[i], runs[i + 1], out_path, buf_size)
                new_runs.append(out_path)

                i += 2
                out_idx += 1

            runs = new_runs
            self.log(f"[INFO] Pass {pass_no} xong: con {len(runs)} file")
            pass_no += 1

        return runs[0]

    def load_sorted_preview(self, path: str, preview_n: int = 200) -> List[float]:
        vals = []
        with open(path, "rb") as f:
            while len(vals) < preview_n:
                chunk = read_doubles(f, 1024)
                if not chunk:
                    break
                vals.extend(chunk)
        return vals[:preview_n]

    def load_all_sorted(self, path: str) -> List[float]:
        vals = []
        with open(path, "rb") as f:
            while True:
                chunk = read_doubles(f, 1024)
                if not chunk:
                    break
                vals.extend(chunk)
        return vals

    def sort_clicked(self):
        inp = self.input_path.get().strip()
        outp = self.output_path.get().strip()
        if not inp:
            messagebox.showerror("Loi", "Ban chua chon Input .bin!")
            return
        if not os.path.exists(inp):
            messagebox.showerror("Loi", "Input file khong ton tai!")
            return
        if not inp.lower().endswith(".bin"):
            messagebox.showerror("Loi", "Input phai la file .bin!")
            return
        if not outp:
            messagebox.showerror("Loi", "Ban chua chon Output .bin!")
            return

        try:
            run_size = int(self.run_size.get())
            buf_size = int(self.buf_size.get())
            if run_size <= 0 or buf_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Loi", "KichThuocRun va KichThuocBoDem phai la so nguyen duong!")
            return

        # Clear UI
        self.txt_log.delete("1.0", "end")
        self.lst_res.delete(0, "end")
        self.sorted_values_cache = []

        self.log("[INFO] ===== BAT DAU SAP XEP NGOAI =====")
        self.log(f"[INFO] Input: {inp} | soLuongSo={os.path.getsize(inp)//DOUBLE_SIZE}")
        self.log(f"[INFO] Output: {outp}")
        self.log(f"[INFO] KichThuocRun={run_size} | KichThuocBoDem={buf_size}")

        # Run dirs
        run_dir = "runs"
        temp_dir = "temp"

        # (optional) clean old dirs for clear demo
        for d in (run_dir, temp_dir):
            if os.path.isdir(d):
                for name in os.listdir(d):
                    try:
                        os.remove(os.path.join(d, name))
                    except OSError:
                        pass

        # Phase 1 + Phase 2
        runs = self.create_runs(inp, run_size, run_dir)
        if not runs:
            self.log("[ERROR] Khong co du lieu de sap xep!")
            return

        final_sorted = self.merge_passes(runs, buf_size, temp_dir)

        # Copy final -> output
        with open(final_sorted, "rb") as fin, open(outp, "wb") as fout:
            while True:
                block = fin.read(1024 * DOUBLE_SIZE)
                if not block:
                    break
                fout.write(block)

        self.log("[INFO] ===== HOAN TAT =====")

        # Load preview to show on UI listbox
        preview = self.load_sorted_preview(outp, preview_n=200)
        self.sorted_values_cache = self.load_all_sorted(outp)  # for export txt

        self.log(f"[INFO] Preview {len(preview)} so dau (da tang dan):")
        self.log("       " + preview_list(preview, 30))

        for v in preview:
            self.lst_res.insert("end", v)

        if len(self.sorted_values_cache) > 200:
            self.log(f"[INFO] File lon ({len(self.sorted_values_cache)} so). List chi hien 200 so dau.")
        else:
            self.log(f"[INFO] Da hien toan bo {len(self.sorted_values_cache)} so trong list.")

    def export_txt(self):
        if not self.sorted_values_cache:
            messagebox.showinfo("Thong bao", "Chua co ket qua de xuat.")
            return

        p = filedialog.asksaveasfilename(
            title="Luu ketqua_sorted.txt",
            defaultextension=".txt",
            initialfile="ketqua_sorted.txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not p:
            return

        with open(p, "w", encoding="utf-8") as f:
            for i, v in enumerate(self.sorted_values_cache, 1):
                f.write(f"{i}\t{v}\n")

        messagebox.showinfo("OK", f"Da xuat: {p}")


if __name__ == "__main__":
    app = ExternalSortGUI()
    app.mainloop()