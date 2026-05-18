import json
import tkinter as giao_dien_do_hoa
from tkinter import messagebox as hop_thoai_thong_bao
import subprocess as tien_trinh_con
import ctypes as thu_vien_c_co_ban
import sys as he_thong_may_tinh
import os as he_dieu_hanh

def chay_lenh_cmd(cau_lenh):
    try:
        tien_trinh_con.run(cau_lenh, shell=True, check=True, stdout=tien_trinh_con.PIPE, stderr=tien_trinh_con.PIPE)
        return True
    except tien_trinh_con.CalledProcessError:
        return False

def kiem_tra_quyen_quan_tri_vien():
    try:
        return thu_vien_c_co_ban.windll.shell32.IsUserAnAdmin()
    except:
        return False

def doc_du_lieu_tu_json(ten_file="ma_loi_chia_se_lan_v2.json"):
    if not he_dieu_hanh.path.exists(ten_file):
        hop_thoai_thong_bao.showerror("Thiếu dữ liệu", f"Không tìm thấy file '{ten_file}' ở thư mục hiện tại!")
        return []
    with open(ten_file, "r", encoding="utf-8") as f:
        du_lieu = json.load(f)
        return du_lieu.get("danh_sach_ma_loi", [])

def khoi_dong_giao_dien():
    danh_sach_loi_json = doc_du_lieu_tu_json()
    if not danh_sach_loi_json:
        he_thong_may_tinh.exit()

    # Bảng màu Dark Mode
    mau_nen_chinh = "#1E1E1E"
    mau_nen_phu = "#252526"
    mau_chu_tieu_de = "#FFFFFF"
    mau_chu_thuong = "#CCCCCC"
    mau_chu_log = "#4CAF50" # Xanh lá cho log thành công
    mau_nut_xanh = "#0E639C"
    mau_nut_do = "#C74C3C"
    mau_hover = "#3E3E42"

    cua_so_chinh = giao_dien_do_hoa.Tk()
    cua_so_chinh.title("VietToolbox - Modul Sửa Lỗi Mạng LAN")
    # Tăng chiều cao cửa sổ để chứa khung log
    cua_so_chinh.geometry("700x700")
    cua_so_chinh.resizable(False, False)
    cua_so_chinh.configure(bg=mau_nen_chinh)

    nhan_tieu_de = giao_dien_do_hoa.Label(cua_so_chinh, text="CÔNG CỤ KHẮC PHỤC SỰ CỐ CHIA SẺ FILE & MÁY IN", 
                                          font=("Segoe UI", 14, "bold"), bg=mau_nen_chinh, fg=mau_chu_tieu_de, pady=15)
    nhan_tieu_de.pack()

    # KHUNG CHỨA CHECKBOX
    khung_danh_sach = giao_dien_do_hoa.Frame(cua_so_chinh, bg=mau_nen_phu, bd=0, highlightthickness=1, highlightbackground="#333333")
    khung_danh_sach.pack(fill="x", padx=25, pady=5)

    cac_bien_tich_chon = {}

    for item in danh_sach_loi_json:
        ma_loi = item.get("ma_loi")
        ten_loi = item.get("ten_loi")
        chuoi_hien_thi = f" {ma_loi} - {ten_loi}"
        
        bien_trang_thai = giao_dien_do_hoa.BooleanVar()
        nut_tich = giao_dien_do_hoa.Checkbutton(
            khung_danh_sach, text=chuoi_hien_thi, variable=bien_trang_thai,
            font=("Segoe UI", 10), bg=mau_nen_phu, fg=mau_chu_thuong,
            selectcolor=mau_nen_chinh, activebackground=mau_hover, activeforeground=mau_chu_tieu_de,
            anchor="w", relief="flat", bd=0, pady=3
        )
        nut_tich.pack(fill="x", padx=15, pady=2)
        cac_bien_tich_chon[ma_loi] = {"trang_thai": bien_trang_thai, "du_lieu": item}

    # KHUNG HIỂN THỊ LOG
    khung_log = giao_dien_do_hoa.Frame(cua_so_chinh, bg=mau_nen_chinh)
    khung_log.pack(fill="both", expand=True, padx=25, pady=10)
    
    nhan_log = giao_dien_do_hoa.Label(khung_log, text="NHẬT KÝ THỰC THI (LOG):", font=("Segoe UI", 10, "bold"), bg=mau_nen_chinh, fg=mau_chu_tieu_de, anchor="w")
    nhan_log.pack(fill="x")

    thanh_cuon = giao_dien_do_hoa.Scrollbar(khung_log)
    thanh_cuon.pack(side="right", fill="y")

    hop_log = giao_dien_do_hoa.Text(khung_log, height=10, bg="#000000", fg=mau_chu_log, font=("Consolas", 10), 
                                    yscrollcommand=thanh_cuon.set, relief="flat", padx=10, pady=10)
    hop_log.pack(side="left", fill="both", expand=True)
    thanh_cuon.config(command=hop_log.yview)
    
    # Chế độ chỉ đọc cho Log
    hop_log.config(state="disabled")

    def ghi_log(noi_dung):
        """Hàm phụ trợ để viết text vào khung Log theo thời gian thực"""
        hop_log.config(state="normal")
        hop_log.insert(giao_dien_do_hoa.END, noi_dung + "\n")
        hop_log.see(giao_dien_do_hoa.END) # Tự động cuộn xuống dòng mới nhất
        hop_log.config(state="disabled")
        cua_so_chinh.update() # Cập nhật giao diện ngay lập tức

    def thuc_thi_sua_loi():
        co_loi_duoc_chon = False
        
        # Xóa log cũ trước khi chạy mới
        hop_log.config(state="normal")
        hop_log.delete(1.0, giao_dien_do_hoa.END)
        hop_log.config(state="disabled")

        ghi_log("[*] Bắt đầu tiến trình khắc phục sự cố...")
        ghi_log("-" * 50)

        for ma_loi, thong_tin in cac_bien_tich_chon.items():
            if thong_tin["trang_thai"].get():
                co_loi_duoc_chon = True
                danh_sach_lenh = thong_tin["du_lieu"].get("lenh_thuc_thi", [])
                
                ghi_log(f"> Đang xử lý: {ma_loi} - {thong_tin['du_lieu'].get('ten_loi')}")
                
                if not danh_sach_lenh:
                    ghi_log(f"  [!] Cảnh báo: Không có lệnh thực thi nào được tìm thấy trong JSON.\n")
                    continue
                
                so_lenh_thanh_cong = 0
                for index, lenh in enumerate(danh_sach_lenh, 1):
                    ghi_log(f"  - Đang chạy lệnh {index}/{len(danh_sach_lenh)}: {lenh[:40]}...")
                    if chay_lenh_cmd(lenh):
                        so_lenh_thanh_cong += 1
                
                ghi_log(f"  [+] Hoàn tất: Chạy thành công {so_lenh_thanh_cong}/{len(danh_sach_lenh)} lệnh.\n")

        if not co_loi_duoc_chon:
            ghi_log("[!] LỖI: Bạn chưa chọn mã lỗi nào để thực thi.")
            return

        ghi_log("-" * 50)
        ghi_log("[*] TOÀN BỘ TIẾN TRÌNH ĐÃ HOÀN TẤT!")

    # KHUNG NÚT BẤM
    khung_nut_bam = giao_dien_do_hoa.Frame(cua_so_chinh, bg=mau_nen_chinh)
    khung_nut_bam.pack(pady=15)

    nut_thuc_thi = giao_dien_do_hoa.Button(
        khung_nut_bam, text="Thực thi sửa lỗi", font=("Segoe UI", 11, "bold"), 
        bg=mau_nut_xanh, fg="#FFFFFF", activebackground="#1177BB", activeforeground="#FFFFFF",
        relief="flat", bd=0, padx=25, pady=8, cursor="hand2", command=thuc_thi_sua_loi
    )
    nut_thuc_thi.pack(side="left", padx=15)

    nut_thoat = giao_dien_do_hoa.Button(
        khung_nut_bam, text="Thoát công cụ", font=("Segoe UI", 11), 
        bg=mau_nut_do, fg="#FFFFFF", activebackground="#E74C3C", activeforeground="#FFFFFF",
        relief="flat", bd=0, padx=25, pady=8, cursor="hand2", command=cua_so_chinh.destroy
    )
    nut_thoat.pack(side="right", padx=15)

    cua_so_chinh.mainloop()

if __name__ == "__main__":
    if kiem_tra_quyen_quan_tri_vien():
        khoi_dong_giao_dien()
    else:
        thu_vien_c_co_ban.windll.shell32.ShellExecuteW(None, "runas", he_thong_may_tinh.executable, " ".join(he_thong_may_tinh.argv), None, 1)