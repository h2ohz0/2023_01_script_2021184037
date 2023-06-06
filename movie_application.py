import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import trend_analysis
import year_month_movielist


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('영화 탐색 및 퀴즈')

        # 창 크기 및 위치 설정
        window_width = 800
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - window_width) // 2)
        y = int((screen_height - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # PIL 라이브러리를 이용해 이미지 파일 열기
        image = Image.open('background.png')

        # 이미지 크기 조정
        new_size = (window_width, window_height)
        image = image.resize(new_size)

        self.bg_image = ImageTk.PhotoImage(image)

        # 배경 이미지를 포함한 Canvas 생성
        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # 프레임 생성 (canvas 위에)
        self.frame_title = tk.Frame(self.canvas)
        self.frame_options = tk.Frame(self.canvas)
        self.frame_content = tk.Frame(self.canvas)

        # 제목 라벨 생성
        self.label_title = ttk.Label(self.frame_title, text=self.title(), font=('한컴 말랑말랑 Regular', 24, "bold"))
        self.label_title.pack(pady=10)

        # 옵션 리스트
        self.options = ['영화 히스토리 퀴즈', '영화 탐색', '텔레그램 봇']

        # 현재 선택된 버튼을 추적하는 변수
        self.selected_button = None

        # 스타일 생성
        self.button_style = ttk.Style()
        self.button_style.configure('TButton', font=('한컴 말랑말랑 Regular', 18), foreground='black')
        self.button_style.configure('Clicked.TButton', font=('한컴 말랑말랑 Regular', 18), foreground='purple')
        self.button_style.map('TButton',
                              foreground=[('active', 'purple')],
                              background=[('active', 'white')])

        # 버튼 생성
        self.buttons = []
        self.sub_buttons = []  # Add this line: new button list for sub menu
        for i, option in enumerate(self.options):
            button = ttk.Button(self.frame_options, text=option, command=lambda o=option: self.button_click(o))
            button.grid(row=0, column=i, sticky='E', padx=5)  # 가로 정렬
            self.buttons.append(button)

        # 출력 칸
        self.content = tk.Text(self.frame_content)
        self.content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 프레임 배치
        self.frame_title.pack(side="top", fill="x")
        self.frame_options.pack(side="top", fill="x")
        self.frame_content.pack(side="bottom", fill="both", expand=True)
        # Create a frame for sub menu
        self.frame_sub_menu = tk.Frame(self.frame_content)

    def button_click(self, option):
        # Set all buttons to the normal style
        for button in self.buttons:
            button.configure(style='TButton')

        # Find the clicked button and set it to the clicked style
        for button in self.buttons:
            if button['text'] == option:
                button.configure(style='Clicked.TButton')
                break

        print(f'{option} 버튼이 클릭되었습니다.')

        if option == '영화 히스토리 퀴즈':
            self.show_quiz()
        elif option == '영화 탐색':
            # Remove the following line to prevent the sub menu from appearing
            self.create_sub_menu()
            self.content.delete('1.0', tk.END)  # Clean the previous content
        elif option == '텔레그램 봇':
            self.show_bot()
            self.content.delete('1.0', tk.END)  # Clean the previous content
        else:
            self.content.delete('1.0', tk.END)
            self.content.insert(tk.END, '올바르지 않은 옵션입니다.')

    def create_sub_menu(self):
        # Clear the frame before creating a new sub menu
        for widget in self.frame_sub_menu.winfo_children():
            widget.destroy()

        # 버튼 생성
        self.sub_buttons = []  # Make sure to clear any previous buttons
        options = ['개봉 연월 통계', '개봉연월 영화목록']
        for i, option in enumerate(options):
            button = ttk.Button(self.frame_sub_menu, text=option, command=lambda o=option: self.sub_button_click(o))
            button.pack(side="top", fill="x")  # 세로 배치
            self.sub_buttons.append(button)

        self.frame_sub_menu.pack(side="bottom", fill="both", expand=True)

    def sub_button_click(self, option):
        print(f'{option} 버튼이 클릭되었습니다.')
        if option == '개봉 연월 통계':
            self.show_trend()
        elif option == '개봉연월 영화목록':
            self.show_movielist()

    def show_quiz(self):
        self.content.delete('1.0', tk.END)  # Clean the previous content

    def show_movielist(self):
        self.content.delete('1.0', tk.END)  # Clean the previous content

        toplevel = tk.Toplevel()
        toplevel.configure(bg='#c5d6eb')  # Set the background color here

        year_month_movielist.create_gui(toplevel)
        self.content.insert(tk.END, '개봉 연월별 영화 목록입니다.\n')

    def show_trend(self):
        self.content.delete('1.0', tk.END)  # Clean the previous content
        trend_analysis.create_gui()

    def show_bot(self):
        self.content.delete('1.0', tk.END)  # Clean the previous content


if __name__ == "__main__":
    app = App()
    app.mainloop()