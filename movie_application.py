import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('영화 분석 및 퀴즈')
        self.configure(background='#c5d6eb')  # 배경색 변경

        # 프레임 생성
        self.frame_title = tk.Frame(self, bg='#c5d6eb')
        self.frame_options = tk.Frame(self, bg='#c5d6eb')
        self.frame_content = tk.Frame(self, bg='#c5d6eb')

        # 제목 라벨 생성
        self.label_title = ttk.Label(self.frame_title, text=self.title(), font=('한컴 말랑말랑 Regular', 18, "bold"), background='#c5d6eb')
        self.label_title.pack(pady=10)

        # 옵션 리스트
        self.options = ['영화 히스토리 퀴즈', '트렌드 분석', '텔레그램 봇']

        # 현재 선택된 라벨을 추적하는 변수
        self.selected_label = None

        # 라벨 생성
        self.labels = []
        for i, option in enumerate(self.options):
            label = ttk.Label(self.frame_options, text=option, background='white', borderwidth=2, relief="groove", font=('한컴 말랑말랑 Regular', 12))
            label.bind("<Button-1>", self.label_click)
            label.grid(row=0, column=i, sticky='E', padx = 5)  # 가로 정렬
            self.labels.append(label)

        # 출력 칸
        self.content = tk.Text(self.frame_content)
        self.content.pack(fill="both", expand=True)

        # 프레임 배치
        self.frame_title.pack(side="top", fill="x")
        self.frame_options.pack(side="top", fill="x")
        self.frame_content.pack(side="bottom", fill="both", expand=True)

    def label_click(self, event):
        clicked_label = event.widget

        # 이전에 선택된 라벨이 있으면 그 라벨의 색상을 원래대로 되돌립니다.
        if self.selected_label:
            self.selected_label.config(foreground='black')

        # 클릭된 라벨의 텍스트 색상을 변경하고, 이 라벨을 현재 선택된 라벨로 설정합니다.
        clicked_label.config(foreground='blue')
        self.selected_label = clicked_label

        print(f'{clicked_label.cget("text")} 라벨이 클릭되었습니다.')

if __name__ == "__main__":
    app = App()
    app.mainloop()
