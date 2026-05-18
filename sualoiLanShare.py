import json
import tkinter as giao_dien_do_hoa
from tkinter import messagebox as hop_thoai_thong_bao
import subprocess as tien_trinh_con
import ctypes as thu_vien_c_co_ban
import sys as he_thong_may_tinh
import os as he_dieu_hanh
import urllib.request # Thư viện gọi API/Link Web
import urllib.error
import ssl

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

def doc_du_lieu_tu_json():
    url_github = "https://raw.githubusercontent.com/tuantran19912512/Lanprint/refs/heads/main/ma_loi_chia_se_lan_v2.json"
    file_cuc_bo = "ma_loi_chia_se_lan_v2.json"
    
    # BỎ QUA KIỂM TRA CHỨNG CHỈ SSL ĐỂ TRÁNH LỖI TRÊN WINDOWS
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 1. Thử tải dữ liệu từ GitHub
    try:
        yeu_cau = urllib.request.Request(url_github, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(yeu_cau, timeout=10, context=ctx) as phan_hoi:
            du_lieu_raw = phan_hoi.read().decode('utf-8')
            du_lieu = json.loads(du_lieu_raw)
            # hop_thoai_thong_bao.showinfo("Thành công", "Đã tải dữ liệu mới nhất từ GitHub!")
            return du_lieu.get("danh_sach_ma_loi", [])
            
    except urllib.error.HTTPError as e:
        loi = f"Lỗi HTTP {e.code}: "
        if e.code == 404:
            loi += "Không tìm thấy file (Vui lòng kiểm tra lại link hoặc chuyển Repo GitHub sang PUBLIC)."
        hop_thoai_thong_bao.showwarning("Lỗi kéo dữ liệu từ GitHub", loi + f"\n\nĐang chuyển sang đọc file Offline ở máy...")
        
    except Exception as e:
        hop_thoai_thong_bao.showwarning("Lỗi mạng", f"Lỗi: {e}\n\nĐang chuyển sang đọc file Offline ở máy...")

    # 2. Đọc dự phòng từ file Offline nếu GitHub lỗi
    if he_dieu_hanh.path.exists(file_cuc_bo):
        try:
            with open(file_cuc_bo, "r", encoding="utf-8") as f:
                du_lieu = json.load(f)
                return du_lieu.get("danh_sach_ma_loi", [])
        except Exception:
            pass
            
    hop_thoai_thong_bao.showerror("Lỗi Dữ Liệu", "Không thể tải từ GitHub và cũng không tìm thấy file dự phòng trên máy!")
    return []

def khoi_dong_giao_dien():
    danh_sach_loi_json = doc_du_lieu_tu_json()
    if not danh_sach_loi_json:
        he_thong_may_tinh.exit()

    # Bảng màu Dark Mode
    mau_nen_chinh = "#1E1E1E"
    mau_nen_phu = "#252526"
    mau_chu_tieu_de = "#FFFFFF"
    mau_chu_thuong = "#CCCCCC"
    mau_chu_log = "#4CAF50" 
    mau_nut_xanh = "#0E639C"
    mau_nut_do = "#C74C3C"
    mau_hover = "#3E3E42"

    cua_so_chinh = giao_dien_do_hoa.Tk()
    cua_so_chinh.title("VietToolbox - Modul Sửa Lỗi Mạng LAN")
    cua_so_chinh.geometry("700x700")
    cua_so_chinh.resizable(False, False)
    cua_so_chinh.configure(bg=mau_nen_chinh)

    nhan_tieu_de = giao_dien_do_hoa.Label(cua_so_chinh, text="CÔNG CỤ KHẮC PHỤC SỰ CỐ CHIA SẺ FILE & MÁY IN", 
                                          font=("Segoe UI", 14, "bold"), bg=mau_nen_chinh, fg=mau_chu_tieu_de, pady=15)
    nhan_tieu_de.pack()

    # KHUNG CHỨA CHECKBOX CÓ THANH CUỘN (SCROLLBAR)
    khung_danh_sach_bao_ngoai = giao_dien_do_hoa.Frame(cua_so_chinh, bg=mau_nen_phu, bd=0, highlightthickness=1, highlightbackground="#333333")
    khung_danh_sach_bao_ngoai.pack(fill="x", padx=25, pady=5)
    
    # Thêm Canvas để có thể cuộn danh sách lỗi nếu sau này JSON quá dài
    canvas_danh_sach = giao_dien_do_hoa.Canvas(khung_danh_sach_bao_ngoai, bg=mau_nen_phu, highlightthickness=0, height=250)
    scrollbar_danh_sach = giao_dien_do_hoa.Scrollbar(khung_danh_sach_bao_ngoai, orient="vertical", command=canvas_danh_sach.yview)
    khung_chua_check = giao_dien_do_hoa.Frame(canvas_danh_sach, bg=mau_nen_phu)
    
    khung_chua_check.bind(
        "<Configure>",
        lambda e: canvas_danh_sach.configure(scrollregion=canvas_danh_sach.bbox("all"))
    )
    canvas_danh_sach.create_window((0, 0), window=khung_chua_check, anchor="nw", width=630)
    canvas_danh_sach.configure(yscrollcommand=scrollbar_danh_sach.set)
    
    canvas_danh_sach.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scrollbar_danh_sach.pack(side="right", fill="y")

    cac_bien_tich_chon = {}

    for item in danh_sach_loi_json:
        ma_loi = item.get("ma_loi")
        ten_loi = item.get("ten_loi")
        chuoi_hien_thi = f" {ma_loi} - {ten_loi}"
        
        bien_trang_thai = giao_dien_do_hoa.BooleanVar()
        nut_tich = giao_dien_do_hoa.Checkbutton(
            khung_chua_check, text=chuoi_hien_thi, variable=bien_trang_thai,
            font=("Segoe UI", 10), bg=mau_nen_phu, fg=mau_chu_thuong,
            selectcolor=mau_nen_chinh, activebackground=mau_hover, activeforeground=mau_chu_tieu_de,
            anchor="w", relief="flat", bd=0, pady=3
        )
        nut_tich.pack(fill="x", padx=10, pady=2)
        cac_bien_tich_chon[ma_loi] = {"trang_thai": bien_trang_thai, "du_lieu": item}

    # KHUNG HIỂN THỊ LOG
    khung_log = giao_dien_do_hoa.Frame(cua_so_chinh, bg=mau_nen_chinh)
    khung_log.pack(fill="both", expand=True, padx=25, pady=10)
    
    nhan_log = giao_dien_do_hoa.Label(khung_log, text="NHẬT KÝ THỰC THI (LOG):", font=("Segoe UI", 10, "bold"), bg=mau_nen_chinh, fg=mau_chu_tieu_de, anchor="w")
    nhan_log.pack(fill="x")

    thanh_cuon_log = giao_dien_do_hoa.Scrollbar(khung_log)
    thanh_cuon_log.pack(side="right", fill="y")

    hop_log = giao_dien_do_hoa.Text(khung_log, height=10, bg="#000000", fg=mau_chu_log, font=("Consolas", 10), 
                                    yscrollcommand=thanh_cuon_log.set, relief="flat", padx=10, pady=10)
    hop_log.pack(side="left", fill="both", expand=True)
    thanh_cuon_log.config(command=hop_log.yview)
    
    hop_log.config(state="disabled")

    def ghi_log(noi_dung):
        hop_log.config(state="normal")
        hop_log.insert(giao_dien_do_hoa.END, noi_dung + "\n")
        hop_log.see(giao_dien_do_hoa.END) 
        hop_log.config(state="disabled")
        cua_so_chinh.update() 

    def thuc_thi_sua_loi():
        co_loi_duoc_chon = False
        
        hop_log.config(state="normal")
        hop_log.delete(1.0, giao_dien_do_hoa.END)
        hop_log.config(state="disabled")

        ghi_log("[*] Đang nạp lệnh từ GitHub/JSON Local...")
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