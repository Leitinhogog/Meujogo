"""
Joguinho de teste em Kivy - esqueleto base
Um quadrado que você controla tocando na tela pra desviar de obstáculos.
Substitua a lógica conforme o jogo for crescendo.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random


class Jogador(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (60, 60)
        self.pos = (Window.width / 2 - 30, 50)
        with self.canvas:
            Color(0.2, 0.8, 0.3, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def mover_para(self, x):
        novo_x = max(0, min(x - self.width / 2, Window.width - self.width))
        self.pos = (novo_x, self.pos[1])
        self.rect.pos = self.pos


class Obstaculo(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (40, 40)
        self.pos = (random.randint(0, Window.width - 40), Window.height)
        with self.canvas:
            Color(0.9, 0.2, 0.2, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def cair(self, velocidade):
        x, y = self.pos
        self.pos = (x, y - velocidade)
        self.rect.pos = self.pos


class JogoWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jogador = Jogador()
        self.add_widget(self.jogador)
        self.obstaculos = []
        self.pontos = 0
        self.game_over = False

        Clock.schedule_interval(self.atualizar, 1 / 60)
        Clock.schedule_interval(self.spawn_obstaculo, 1.2)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.jogador.mover_para(touch.x)

    def on_touch_down(self, touch):
        if not self.game_over:
            self.jogador.mover_para(touch.x)

    def spawn_obstaculo(self, dt):
        if not self.game_over:
            obs = Obstaculo()
            self.obstaculos.append(obs)
            self.add_widget(obs)

    def atualizar(self, dt):
        if self.game_over:
            return

        for obs in self.obstaculos[:]:
            obs.cair(4)

            if obs.pos[1] < -obs.height:
                self.obstaculos.remove(obs)
                self.remove_widget(obs)
                self.pontos += 1

            elif self.jogador.rect.pos[0] < obs.rect.pos[0] + obs.width and \
                 self.jogador.rect.pos[0] + self.jogador.width > obs.rect.pos[0] and \
                 self.jogador.rect.pos[1] < obs.rect.pos[1] + obs.height and \
                 self.jogador.rect.pos[1] + self.jogador.height > obs.rect.pos[1]:
                self.game_over = True
                print(f"GAME OVER - Pontos: {self.pontos}")


class MeuJogoApp(App):
    def build(self):
        return JogoWidget()


if __name__ == "__main__":
    MeuJogoApp().run()
