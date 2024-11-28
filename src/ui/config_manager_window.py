import tkinter as tk
from tkinter import ttk, messagebox
from config.constants import config, FONT_SIZES
from config.config_manager import UCConfig

class ConfigManagerWindow:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("설정 관리")
        self.window.geometry("800x600")
        
        self._create_widgets()
        self._load_current_config()
        
    def _create_widgets(self):
        # UC 관리 프레임
        uc_frame = ttk.LabelFrame(self.window, text="UC 관리", padding="10")
        uc_frame.pack(fill="x", padx=10, pady=5)
        
        # UC 목록
        self.uc_listbox = tk.Listbox(uc_frame, height=10)
        self.uc_listbox.pack(side="left", fill="x", expand=True)
        self.uc_listbox.bind('<<ListboxSelect>>', self._on_uc_select)
        
        # UC 관리 버튼
        btn_frame = ttk.Frame(uc_frame)
        btn_frame.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="추가", command=self._add_uc).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="삭제", command=self._remove_uc).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="수정", command=self._edit_uc).pack(fill="x", pady=2)
        
        # UC 상세 정보 프레임
        details_frame = ttk.LabelFrame(self.window, text="UC 상세 정보", padding="10")
        details_frame.pack(fill="x", padx=10, pady=5)
        
        # ID 입력
        ttk.Label(details_frame, text="ID:").grid(row=0, column=0, sticky="e")
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(details_frame, textvariable=self.id_var)
        self.id_entry.grid(row=0, column=1, sticky="ew")
        
        # 이름 입력
        ttk.Label(details_frame, text="이름:").grid(row=1, column=0, sticky="e")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(details_frame, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=1, sticky="ew")
        
        # 바코드 프리픽스 입력
        ttk.Label(details_frame, text="바코드 프리픽스:").grid(row=2, column=0, sticky="e")
        self.prefix_var = tk.StringVar()
        self.prefix_entry = ttk.Entry(details_frame, textvariable=self.prefix_var)
        self.prefix_entry.grid(row=2, column=1, sticky="ew")
        
        # TRAY 매핑 프레임
        mapping_frame = ttk.LabelFrame(self.window, text="TRAY 매핑", padding="10")
        mapping_frame.pack(fill="x", padx=10, pady=5)
        
        self.tray_vars = {}
        for i, tray in enumerate(config.trays):
            self.tray_vars[tray.id] = tk.BooleanVar()
            ttk.Checkbutton(
                mapping_frame, 
                text=tray.name,
                variable=self.tray_vars[tray.id]
            ).grid(row=i//2, column=i%2, sticky="w")
            
        # 저장 버튼
        ttk.Button(
            self.window, 
            text="저장", 
            command=self._save_changes
        ).pack(pady=10)
        
    def _load_current_config(self):
        """현재 설정 로드"""
        self.uc_listbox.delete(0, tk.END)
        for uc in config.ucs:
            self.uc_listbox.insert(tk.END, f"{uc.id} - {uc.name}")
            
    def _on_uc_select(self, event):
        """UC 선택 시 상세 정보 표시"""
        if not self.uc_listbox.curselection():
            return
            
        selected_id = self.uc_listbox.get(self.uc_listbox.curselection()).split(" - ")[0]
        uc = next((uc for uc in config.ucs if uc.id == selected_id), None)
        
        if uc:
            self.id_var.set(uc.id)
            self.name_var.set(uc.name)
            self.prefix_var.set(uc.barcodePrefix)
            
            # TRAY 매핑 체크박스 업데이트
            for tray_id, var in self.tray_vars.items():
                tray = next((t for t in config.trays if t.id == tray_id), None)
                if tray:
                    var.set(uc.id in tray.allowedUCs)
                    
    def _add_uc(self):
        """새 UC 추가"""
        self._clear_form()
        self.id_entry.focus()
        
    def _remove_uc(self):
        """선택된 UC 삭제"""
        if not self.uc_listbox.curselection():
            messagebox.showwarning("경고", "삭제할 UC를 선택하세요.")
            return
            
        selected_id = self.uc_listbox.get(self.uc_listbox.curselection()).split(" - ")[0]
        if messagebox.askyesno("확인", f"{selected_id}를 삭제하시겠습니까?"):
            config.remove_uc(selected_id)
            self._load_current_config()
            self._clear_form()
            
    def _edit_uc(self):
        """선택된 UC 수정"""
        if not self.uc_listbox.curselection():
            messagebox.showwarning("경고", "수정할 UC를 선택하세요.")
            return
            
        self.id_entry.focus()
        
    def _save_changes(self):
        """변경사항 저장"""
        uc_id = self.id_var.get()
        name = self.name_var.get()
        prefix = self.prefix_var.get()
        
        if not all([uc_id, name, prefix]):
            messagebox.showwarning("경고", "모든 필드를 입력하세요.")
            return
            
        # UC 설정 업데이트
        new_uc = UCConfig(id=uc_id, name=name, barcodePrefix=prefix)
        
        # 기존 UC 삭제 후 새로 추가
        config.remove_uc(uc_id)
        config.add_uc(new_uc)
        
        # TRAY 매핑 업데이트
        for tray in config.trays:
            if self.tray_vars[tray.id].get():
                if uc_id not in tray.allowedUCs:
                    tray.allowedUCs.append(uc_id)
            else:
                if uc_id in tray.allowedUCs:
                    tray.allowedUCs.remove(uc_id)
                    
        config.save_config()
        self._load_current_config()
        messagebox.showinfo("알림", "설정이 저장되었습니다.")
        
    def _clear_form(self):
        """입력 폼 초기화"""
        self.id_var.set("")
        self.name_var.set("")
        self.prefix_var.set("")
        for var in self.tray_vars.values():
            var.set(False)
            
    def run(self):
        """창 실행"""
        self.window.mainloop() 