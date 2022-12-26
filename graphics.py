import tkinter as tk


def draw(canvas, width, height):


window = tk.Tk()
canvas = tk.Canvas(window, width=400, height=300)
canvas.pack()



# frame_a = tk.Frame()
# frame_b = tk.Frame()


# greetin = tk.Label(
#     text="I'm in frame A",
#     fg="#FF5733",
#     bg="#34A2FE",
#     width=30,
#     height=10,
#     master = frame_a)

# button = tk.Button(
#     text="I'm in frame b!",
#     width=25,
#     height=5,
#     bg="#000000",
#     fg="#FFFFFF",
#     master = frame_b
# )

# entry = tk.Entry(width=50)

# greetin.pack()
# button.pack()
# frame_a.pack()
# frame_b.pack()
# entry.pack()


window.mainloop()
x = 1