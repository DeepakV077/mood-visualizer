try:
    import pygame
    _PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    _PYGAME_AVAILABLE = False

MOOD_COLORS = {
    "CALM": (100, 200, 255),
    "FOCUS": (255, 200, 100),
    "STRESS": (255, 50, 50),
    "UNKNOWN": (200, 200, 200)
}

# --- Pygame Visualizer ---
class Visualizer:
    def __init__(self, width=400, height=400):
        if not _PYGAME_AVAILABLE:
            raise RuntimeError("Pygame not available")
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mood Visualizer")
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)

    def update(self, mood, features=None, dt=None):
        color = MOOD_COLORS.get(mood, (200, 200, 200))
        self.screen.fill((0, 0, 0))
        # features: optional (alpha, beta, gamma) in 0..1 to drive visuals
        if features is None:
            a = 0.33
        else:
            try:
                a, b, g = features
            except Exception:
                a = 0.33
        # orb radius influenced by alpha
        orb_radius = int(40 + 140 * float(a))
        pygame.draw.circle(self.screen, color, (self.width//2, self.height//2), max(8, orb_radius))

        # Display feature values and dt
        if features is not None and dt is not None:
            a, b, g = features
            text = f"Mood: {mood} | Alpha:{a:.2f} Beta:{b:.2f} Gamma:{g:.2f} | dt:{dt:.2f}s"
        else:
            text = f"Mood: {mood}"

        img = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        self.clock.tick(30)

    def close(self):
        pygame.quit()


# --- Console fallback Visualizer ---
class _ConsoleVisualizer:
    def __init__(self, width=700, height=500, fps=60):
        import time
        self.time = time
        self.width = width
        self.height = height
        self.target_fps = fps
        self.mood = 'UNKNOWN'
        self.feature_vals = (0.33, 0.33, 0.33)
        self._last_print = self.time.time()

    def update(self, mood, features=None, dt=None):
        self.mood = mood
        if features is None:
            a = b = g = 0.0
        else:
            a, b, g = features
            self.feature_vals = features
        if self.time.time() - self._last_print > 0.5:
            print(f"[console] Mood={mood} alpha={a:.2f} beta={b:.2f} gamma={g:.2f}")
            self._last_print = self.time.time()

    def close(self):
        print('Console visualizer closed')


if not _PYGAME_AVAILABLE:
    Visualizer = _ConsoleVisualizer
