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


def link(a: VGroup, b: VGroup, label: str, color=INK, arc: float = 0.0) -> VGroup:
    """Arrow from a's edge to b's edge, on the sides facing each other. Manim has no layout engine:
    use this instead of center-to-center arrows, which cross boxes and land on corners."""
    (ax, ay, _), (bx, by, _) = a[0].get_center(), b[0].get_center()
    if abs(bx - ax) >= abs(by - ay):
        start, end = (a[0].get_right(), b[0].get_left()) if bx > ax else (a[0].get_left(), b[0].get_right())
    else:
        start, end = (a[0].get_bottom(), b[0].get_top()) if by < ay else (a[0].get_top(), b[0].get_bottom())
    arrow = Arrow(start, end, color=color, buff=0.06, stroke_width=4, path_arc=arc,
                  max_tip_length_to_length_ratio=0.2)
    tag = Text(label, font_size=26, color=ACCENT)
    return VGroup(arrow, tag.next_to(arrow.point_from_proportion(0.4), RIGHT if abs(bx - ax) < abs(by - ay) else UP, buff=0.08))


def fit(*parts: VGroup) -> VGroup:
    """Scale the whole picture to the frame, so nothing runs off the edge."""
    return VGroup(*parts).scale_to_fit_width(config.frame_width - 0.8).move_to([0, -0.15, 0])


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
        fit(you, prog, shelf)  # before anything is shown, so nothing jumps
        self.play(FadeIn(you), run_time=self.say(
            "First, you. You type commands into the terminal, a window where you give the computer instructions by typing."))
        self.play(FadeIn(prog), run_time=self.say(
            "Next, the Notes program. It is a C L I, which stands for Command Line Interface: "
            "a program you use by typing. Think of it as a librarian."))
        self.play(FadeIn(shelf), run_time=self.say(
            "Last, the notes folder, where each note is saved as a file. That is the library shelf."))

        # 3. Walk the numbered steps
        l1, l2 = link(you, prog, "1"), link(prog, shelf, "2")
        self.play(GrowArrow(l1[0]), Write(l1[1]), run_time=self.say(
            "Step one. You type notes show todo. The program first checks the name is safe, "
            "like a librarian making sure you asked for a book and not the office keys."))
        dot = Dot(color=ACCENT).move_to(l2[0].get_start())
        self.play(GrowArrow(l2[0]), Write(l2[1]), run_time=self.say(
            "Step two. The program reads the file called todo from the folder. The librarian takes the book off the shelf."))
        self.play(FadeIn(dot), MoveAlongPath(dot, l2[0]), run_time=1)
        self.play(MoveAlongPath(dot, Arrow(shelf[0].get_left(), prog[0].get_right())), run_time=1)
        # a return trip: bottom edge to bottom edge, curved under the row so it crosses no box
        back = Arrow(prog[0].get_bottom(), you[0].get_bottom(), color=ACCENT, path_arc=-0.8, buff=0.06)
        n3 = Text("3", font_size=26, color=ACCENT).next_to(back, DOWN, buff=0.08)
        self.play(Create(back), Write(n3), MoveAlongPath(dot, back), run_time=self.say(
            "Step three. The program prints the note in your terminal. The librarian hands you the book."))

        # 4. Recap
        self.play(Indicate(prog), run_time=self.say(
            "In short: you ask, the program checks and fetches, and you get your note back."))
        self.wait(0.5)
