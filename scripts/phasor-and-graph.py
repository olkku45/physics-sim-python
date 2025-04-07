import pygame
import math

# pygame setup
pygame.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
CIRCLE_RADIUS = 150
CIRCLE_CENTER = (300, 360)
ORIGIN = (600, 360)
SCALE = 100
X_MAX = 2 * math.pi
DOT_RADIUS = 10
LINE_AMOUNT = 300
DOT_SPEED = 0.00025  # rad / ms


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

        pygame.display.flip()
        pygame.display.update()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


# idea olisi tehdä vaiheenosoitin, jota manuaalisesti
# pyörittämällä saataisiin tehtyä sinimuotoinen graafi