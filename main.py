import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Добавляем поддержку PIL для работы с изображениями

class ZooQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор эффективности очереди зоомагазина")
        self.root.geometry("600x400")
        self.root.resizable(False, False)  # Запрещаем изменение размера окна
        self.root.configure(bg='#E6F3FF')  # Устанавливаем голубой фон
        
        # Устанавливаем иконку окна
        try:
            # Конвертируем JPG в ICO
            img = Image.open('icon2.jpg')
            img.save('temp_icon.ico', format='ICO', sizes=[(32, 32)])
            self.root.iconbitmap('temp_icon.ico')
        except Exception as e:
            print(f"Ошибка загрузки иконки окна: {e}")
        
        # Основной контейнер
        main_frame = tk.Frame(root, bg='#E6F3FF')
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Создаем верхний контейнер для логотипа и заголовка
        top_frame = tk.Frame(main_frame, bg='#E6F3FF')
        top_frame.pack(fill="x", anchor="w")
        
        # Добавляем логотип
        try:
            original_image = Image.open("icon2.jpg")
            size = 32  # Уменьшаем размер логотипа
            original_image.thumbnail((size, size), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(original_image)
            logo_label = tk.Label(top_frame, image=self.logo_image, bg='#E6F3FF')
            logo_label.pack(side="left", padx=(0, 10))
            
            # Заголовок рядом с логотипом
            tk.Label(top_frame, 
                    text="Калькулятор эффективности\nочереди зоомагазина",
                    font=("Arial", 12), 
                    bg='#E6F3FF',
                    justify="left").pack(side="left", pady=5)
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            
        # Создаем контейнер для полей ввода
        input_frame = tk.Frame(main_frame, bg='#E6F3FF')
        input_frame.pack(fill="both", expand=True, pady=20)
        
        # Поля ввода
        tk.Label(input_frame, text="Интенсивность поступления клиентов (λ, клиентов/час):", 
                anchor="w", bg='#E6F3FF').pack(fill="x")
        self.lambda_entry = tk.Entry(input_frame)
        self.lambda_entry.pack(fill="x", pady=5)
        
        tk.Label(input_frame, text="Интенсивность обслуживания (μ, клиентов/час):", 
                anchor="w", bg='#E6F3FF').pack(fill="x")
        self.mu_entry = tk.Entry(input_frame)
        self.mu_entry.pack(fill="x", pady=5)
        
        # Кнопка расчета
        tk.Button(input_frame, text="Рассчитать показатели", 
                command=self.calculate_metrics).pack(pady=15)
        
        # Область для результатов
        self.result_label = tk.Label(input_frame, text="", wraplength=550, 
                                   justify="left", bg='#E6F3FF')
        self.result_label.pack(pady=10)
    
    def calculate_metrics(self):
        try:
            # Получение входных данных
            lambda_val = float(self.lambda_entry.get())
            mu_val = float(self.mu_entry.get())
            
            # Валидация
            if lambda_val <= 0 or mu_val <= 0:
                messagebox.showerror("Ошибка", "Интенсивности должны быть положительными числами.")
                return
            if lambda_val >= mu_val:
                messagebox.showerror("Ошибка", 
                    "Интенсивность поступления (λ) должна быть меньше интенсивности обслуживания (μ), "
                    "иначе очередь будет расти бесконечно.")
                return
            
            # Расчеты для M/M/1
            ro = lambda_val / mu_val  # Коэффициент загрузки
            p_refusal = (1 - ro) * ro  # Вероятность отказа с учетом загрузки
            relative_throughput = 1 - p_refusal  # Относительная пропускная способность
            absolute_throughput = lambda_val * relative_throughput  # Абсолютная пропускная способность
            
            # Форматирование результатов с округлением до тысячных
            result_text = (
                f"Результаты расчета:\n"
                f"Вероятность отказа (P_ref): {p_refusal:.3f}\n"
                f"Относительная пропускная способность (Q): {relative_throughput:.3f}\n"
                f"Абсолютная пропускная способность (A): {absolute_throughput:.3f} клиентов/час"
            )
            self.result_label.config(text=result_text)
            
            # Не очищаем поля ввода после расчета, чтобы можно было экспериментировать
            # self.lambda_entry.delete(0, tk.END)
            # self.mu_entry.delete(0, tk.END)
        
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для λ и μ.")
            self.lambda_entry.delete(0, tk.END)
            self.mu_entry.delete(0, tk.END)
            self.result_label.config(text="")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")
            self.lambda_entry.delete(0, tk.END)
            self.mu_entry.delete(0, tk.END)
            self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZooQueueApp(root)
    root.mainloop()