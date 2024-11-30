from ui.main_window import MainWindow
from services.update_service import UpdateService

def main():
    """메인 프로그램 실행"""
    # 업데이트 확인
    update_service = UpdateService()
    if update_service.check_for_updates():
        print("새로운 버전이 있습니다. 업데이트를 시작합니다...")
        if update_service.download_and_install_update():
            return  # 업데이트 성공 시 현재 프로그램 종료
        else:
            print("업데이트 실패. 현재 버전으로 계속합니다.")
    
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main() 