import tkinter as tk
from tkinter import ttk
import pygame
import math

def ejecutar():
    seleccion = tipo_simulacion.get()

    if seleccion == "Maquina de Atwood":
        iniciar_simulacion()
    elif seleccion == "Bloque con rozamiento":
        simulacion_friccion()

def cambiar_inputs(event):
    seleccion = tipo_simulacion.get()

    label_m1.place_forget()
    entry_m1.place_forget()

    label_m2.place_forget()
    entry_m2.place_forget()

    label_m.place_forget()
    entry_m.place_forget()

    label_f.place_forget()
    entry_f.place_forget()

    label_mu.place_forget()
    entry_mu.place_forget()

    if seleccion == "Maquina de Atwood":
        label_m1.place(x=150, y=80)
        entry_m1.place(x=245, y=80)

        label_m2.place(x=150, y=120)
        entry_m2.place(x=245, y=120)

    elif seleccion == "Bloque con rozamiento":
        label_m.place(x=100, y=80)
        entry_m.place(x=245, y=80)

        label_f.place(x=100, y=120)
        entry_f.place(x=245, y=120)

        label_mu.place(x=100, y=160)
        entry_mu.place(x=245, y=160)


def iniciar_simulacion():

    m1 = float(entry_m1.get())
    m2 = float(entry_m2.get())

    g = 9.81
    a = abs((m2*g - m1*g)/ (m1 + m2))

    direction = 1

    if m1 > m2:
        direction = -1

    if direction == 1:
        T = m1*a + m1*9.81
    elif direction == -1:
        T = m2*a + m2*9.81

    pygame.init()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pulley_x = 450
    pulley_y = 180
    pulley_radius = 60

    left_y = 350
    right_y = 350

    mass_w = 60
    mass_h = 60

    velocity = 0
    dt = 1/60

    PIXELS_PER_METER = 40
    a_pixels = a * PIXELS_PER_METER

    running = True
    simulation_running = True
    font = pygame.font.SysFont("Arial", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if simulation_running:
            velocity += a_pixels * dt
            if direction == -1:
                left_y += velocity * dt
                right_y -= velocity * dt
            else:
                left_y -= velocity * dt
                right_y += velocity * dt
            if left_y <= 120 or right_y <= 120:
                simulation_running = False
            if left_y >= 520 or right_y >= 520:
                simulation_running = False
        screen.fill((25,25,30))

        pygame.draw.circle(
            screen,
            (220,220,220),
            (pulley_x,pulley_y),
            pulley_radius,
            5
        )

        pygame.draw.line(
            screen,
            (255,255,255),
            (pulley_x-pulley_radius, pulley_y),
            (pulley_x-pulley_radius, left_y),
            3
        )

        pygame.draw.line(
            screen,
            (255,255,255),
            (pulley_x+pulley_radius, pulley_y),
            (pulley_x+pulley_radius, right_y),
            3
        )

        pygame.draw.arc(
            screen,
            (255,255,255),
            (
                pulley_x-pulley_radius,
                pulley_y-pulley_radius,
                pulley_radius*2,
                pulley_radius*2
            ),
            math.pi,
            2*math.pi,
            3
        )

        pygame.draw.rect(
            screen,
            (220,80,80),
            (
                pulley_x-pulley_radius-mass_w//2,
                left_y,
                mass_w,
                mass_h
            )
        )

        pygame.draw.rect(
            screen,
            (80,120,255),
            (
                pulley_x+pulley_radius-mass_w//2,
                right_y,
                mass_w,
                mass_h
            )
        )

        label1 = font.render("m1", True, (255,255,255))
        label2 = font.render("m2", True, (255,255,255))

        screen.blit(
            label1,
            (
                pulley_x-pulley_radius-15,
                left_y+15
            )
        )

        screen.blit(
            label2,
            (
                pulley_x+pulley_radius-15,
                right_y+15
            )
        )

        text1 = font.render(
            f"Aceleracion = {a:.2f} m/s²",
            True,
            (255,255,255)
        )

        text2 = font.render(
            f"Tension = {T:.2f} N",
            True,
            (255,255,255)
        )

        screen.blit(text1, (20,20))
        screen.blit(text2, (20,50))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def simulacion_friccion():
    m = float(entry_m.get())
    F = float(entry_f.get())
    mu = float(entry_mu.get())

    g = 9.81
    Fr = mu * m * g
    a = (F-Fr) / m

    pygame.init()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    x = 100
    y = 400

    velocity = 0
    dt = 1/60

    PIXELS_PER_METER = 40
    a_pixels = a * PIXELS_PER_METER

    running = True
    simulation_running = True

    font = pygame.font.SysFont("Arial", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if simulation_running:
            velocity += a_pixels * dt
            x += velocity * dt
            if x >= 700:
                simulation_running = False
        screen.fill((25,25,30))

        pygame.draw.line(
            screen,
            (255,255,255),
            (50,460),
            (850,460),
            5
        )

        pygame.draw.rect(
            screen,
            (220,80,80),
            (x,y,100,60)
        )

        pygame.draw.line(
            screen,
            (80,120,255),
            (x+100,y+30),
            (x+180,y+30),
            5
        )

        pygame.draw.polygon(
            screen,
            (80,120,255),
            [
                (x+180,y+30),
                (x+160,y+20),
                (x+160,y+40)
            ]
        )

        text1 = font.render(
            f"Aceleracion = {a:.2f} m/s²",
            True,
            (255,255,255)
        )

        text2 = font.render(
            f"Friccion = {Fr:.2f} N",
            True,
            (255,255,255)
        )

        screen.blit(text1, (20,20))
        screen.blit(text2, (20,50))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


root = tk.Tk()
root.title("Máquina de Atwood")
root.geometry("600x500")

tipo_simulacion = tk.StringVar()

combo = ttk.Combobox(
    root,
    textvariable=tipo_simulacion,
    state="readonly"
)
combo["values"] = (
    "Maquina de Atwood",
    "Bloque con rozamiento"
)

combo.current(0)
combo.place(x=230,y=20)
combo.bind(
    "<<ComboboxSelected>>",
    cambiar_inputs
)

label_m1 = tk.Label(root, text="Masa m1 (kg)")
entry_m1 = tk.Entry(root)
entry_m1.insert(0, "")

label_m2 = tk.Label(root, text="Masa m2 (kg)")
entry_m2 = tk.Entry(root)
entry_m2.insert(0, "")

label_m = tk.Label(root, text="Masa (kg)")
entry_m = tk.Entry(root)

label_f = tk.Label(root, text="Fuerza (N)")
entry_f = tk.Entry(root)

label_mu = tk.Label(root, text="Coeficiente μ")
entry_mu = tk.Entry(root)

label_m1.place(x=150, y=80)
entry_m1.place(x=245, y=80)

label_m2.place(x=150, y=120)
entry_m2.place(x=245, y=120)

btn1 = tk.Button(
    root,
    text="Correr Simulacion",
    command=ejecutar
)
btn1.place(x=245,y=200)

btn2 = tk.Button(
    root,
    text="Cerrar",
    command=root.destroy
)
btn2.place(x=10,y=470)

root.mainloop()