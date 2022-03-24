import tkinter as tk
import pyperclip
from txtcli.model import ErrMsg

from txtcli.util import send_msg


def create_window_center(title: str) -> tk.Tk:
    window = tk.Tk()
    window.title(title)
    window.rowconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=500, weight=1)

    window_width = 500
    window_height = 250
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    return window


def get_text(form_input: tk.Entry | tk.Text) -> str:
    if type(form_input) is tk.Entry:
        return form_input.get().strip()
    elif type(form_input) is tk.Text:
        return form_input.get("1.0", tk.END).strip()
    else:
        return ""


def tk_send_msg() -> ErrMsg:
    window = create_window_center("Send - txt")

    label = tk.Label(text="txt", pady=5)
    label.pack()

    frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1, padx=5, pady=5)
    frame.pack()

    form_input = tk.Text(master=frame, width=60, height=10, pady=5)
    form_input.pack()

    def btn_click():
        msg = get_text(form_input)
        window.quit()
        return send_msg(msg)

    post_btn = tk.Button(master=frame, text="Send", command=btn_click)
    post_btn.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=5)

    cancel_btn = tk.Button(master=frame, text="Cancel", command=window.quit)
    cancel_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    form_input.focus()
    try:
        msg = pyperclip.paste()
        form_input.insert(tk.END, msg)
    except Exception:
        pass

    window.mainloop()
