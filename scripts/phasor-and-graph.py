import pygame
import math

# pygame setup
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Phasor and Graph")
font = pygame.font.SysFont('sans', 25)

CIRCLE_RADIUS = 150
CIRCLE_CENTER = (300, 360)
ORIGIN = (600, 360)
SCALE = 100
X_MAX = 2 * math.pi
DOT_RADIUS = 10
LINE_AMOUNT = 300
DOT_SPEED = 0.00025  # rad / ms
TEXT = font.render("Angle: ", True, (0, 0, 0))


def phasor_dot_coordinates(psi):
    return (
                CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(psi), 
                CIRCLE_CENTER[1] - CIRCLE_RADIUS * math.sin(psi)
    )


def sine_wave_dot_coordinates(psi):
    return (
                psi * SCALE + ORIGIN[0],
                -math.sin(psi) * SCALE + ORIGIN[1]
    )


def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    window.blit(text_obj, (x, y))

# main function
def main():
    running = True
    drag = False
    psi = 1
    dt = 60

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                dot_x, dot_y = phasor_dot_coordinates(psi)
                dist = math.sqrt((dot_x - mouse_x)**2 + (dot_y - mouse_y)**2)
                
                if dist < DOT_RADIUS * 1.5:
                    drag = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False

            if event.type == pygame.MOUSEMOTION and drag:
                mouse_x, mouse_y = event.pos
                psi = math.atan2(-(mouse_y - CIRCLE_CENTER[1]), mouse_x - CIRCLE_CENTER[0])
                if psi < 0:
                    psi += 2 * math.pi

            if event.type == pygame.QUIT:
                running = False

        if not drag:
            psi += 0.00025 * dt

        if psi > 2 * math.pi:
            psi -= 2 * math.pi

        window.fill("white")
        # phasor circle
        pygame.draw.circle(window, (0, 0, 0), CIRCLE_CENTER, CIRCLE_RADIUS + 2, 4)
        # axes
        pygame.draw.line(window, (0, 0, 0), (ORIGIN[0], ORIGIN[1] - SCALE), (ORIGIN[0], ORIGIN[1] + SCALE), 5)
        pygame.draw.line(window, (0, 0, 0), ORIGIN, (ORIGIN[0] + X_MAX * SCALE, ORIGIN[1]), 5)
        # phasor dot
        pygame.draw.circle(
            window, 
            (52, 200, 255), 
            phasor_dot_coordinates(psi), 
            DOT_RADIUS
        )
        # sine wave dot
        pygame.draw.circle(
            window, 
            (52, 200, 255), 
            sine_wave_dot_coordinates(psi), 
            DOT_RADIUS
        )
        # draw sine wave
        for i in range(LINE_AMOUNT):
            t1 = i / LINE_AMOUNT
            t2 = (i + 1) / LINE_AMOUNT
            t1 *= 2 * math.pi
            t2 *= 2 * math.pi
            pygame.draw.line(
                window, 
                (52, 200, 255), 
                sine_wave_dot_coordinates(t1),
                sine_wave_dot_coordinates(t2)
            )
        # angle text
        round_angle = round(psi, 2)
        draw_text(f"Angle: {round_angle} rad", font, (0, 0, 0), 200, 100)
        # coordinate text
        coordinate_x, coordinate_y = sine_wave_dot_coordinates(psi)
        round_coordinate_x = round(coordinate_x)
        round_coordinate_y = round(coordinate_y)
        draw_text(f"Coordinate: {round_coordinate_x}, {round_coordinate_y}", font, (0, 0, 0), 700, 100)
        # axes text
        draw_text("1 (240)", font, (0, 0, 0), 500, 240)
        draw_text("0 (345)", font, (0, 0, 0), 500, 345)
        draw_text("-1 (450)", font, (0, 0, 0), 490, 450)
        draw_text("2 * pi (1228)", font, (0, 0, 0), 1100, 300)

        pygame.display.flip()
        pygame.display.update()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()