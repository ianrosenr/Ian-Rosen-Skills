"""EXAMPLE architecture video: replace the narration and parts with this app's.
Rules: page instructions, "Video". Each self.say(...) returns its length in seconds;
give animations that run time so picture and voice stay in sync."""
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, FadeOut, GrowArrow, Indicate,
                   MoveAlongPath, RoundedRectangle, Text, VGroup, Write, config)

from narrate import Narrated

config.background_color = "#0f172a"
INK, ACCENT, DIM = "#f1f5f9", "#60a5fa", "#64748b"


def part(name: str, tech: str, x: float) -> VGroup:
    box = RoundedRectangle(width=3.2, height=1.7, corner_radius=0.2, color=ACCENT).shift(RIGHT * x)
    label = VGroup(Text(name, font_size=30, color=INK), Text(tech, font_size=22, color=DIM)).arrange(DOWN, buff=0.15)
    return VGroup(box, label.move_to(box))


class Architecture(Narrated):
    def construct(self):
        # 1. What the app does
        title = Text("How Notes works", font_size=56, color=INK)
        self.play(Write(title), run_time=self.say("This is how the Notes app works, explained from the very beginning."))
        self.play(FadeOut(title), run_time=0.5)

        # 2. Build the diagram one part at a time, with the analogy
        you = part("You", "at the terminal", -5)
        prog = part("Notes program", "Python CLI", 0)
        shelf = part("Notes folder", "plain text files", 5)
        self.play(FadeIn(you), run_time=self.say(
            "First, you. You type commands into the terminal, a window where you give the computer instructions by typing."))
        self.play(FadeIn(prog), run_time=self.say(
            "Next, the Notes program. It is a C L I, which stands for Command Line Interface: "
            "a program you use by typing. Think of it as a librarian."))
        self.play(FadeIn(shelf), run_time=self.say(
            "Last, the notes folder, where each note is saved as a file. That is the library shelf."))

        # 3. Walk the numbered steps
        a1 = Arrow(you[0].get_right(), prog[0].get_left(), color=INK)
        a2 = Arrow(prog[0].get_right(), shelf[0].get_left(), color=INK)
        n1 = Text("1", font_size=28, color=ACCENT).next_to(a1, UP)
        n2 = Text("2", font_size=28, color=ACCENT).next_to(a2, UP)
        self.play(GrowArrow(a1), Write(n1), run_time=self.say(
            "Step one. You type notes show todo. The program first checks the name is safe, "
            "like a librarian making sure you asked for a book and not the office keys."))
        dot = Dot(color=ACCENT).move_to(prog[0].get_right())
        self.play(GrowArrow(a2), Write(n2), run_time=self.say(
            "Step two. The program reads the file called todo from the folder. The librarian takes the book off the shelf."))
        self.play(FadeIn(dot), MoveAlongPath(dot, Arrow(prog[0].get_right(), shelf[0].get_left())), run_time=1)
        back = Arrow(prog[0].get_bottom(), you[0].get_bottom(), color=ACCENT, path_arc=-0.8)
        self.play(MoveAlongPath(dot, Arrow(shelf[0].get_left(), prog[0].get_right())), run_time=1)
        n3 = Text("3", font_size=28, color=ACCENT).next_to(back, DOWN)
        self.play(Create(back), Write(n3), MoveAlongPath(dot, back), run_time=self.say(
            "Step three. The program prints the note in your terminal. The librarian hands you the book."))

        # 4. Recap
        self.play(Indicate(prog), run_time=self.say(
            "In short: you ask, the program checks and fetches, and you get your note back."))
        self.wait(0.5)
