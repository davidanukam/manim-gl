from manimlib import *
from components import *


class Test(Scene):
    def construct(self):
        c1 = Checklist(
            "VERIFYING",
            "bank.com",
            [
                ("Certificate signed by intermediate", "VALID"),
                ("Intermediate signed by trusted root", "PENDING"),
                ("Domain matches bank.com", "PENDING"),
            ],
            width=7.2,
        )
        self.play(Write(c1))
        self.play(c1.animate.add(("This list works", "VALID")))
        self.play(c1.animate.set_status(0, "FAIL"))
        self.play(c1.animate.pop(1))

        q = JobQueue(
            ["resize photo", "for user 123", "upload done"],
            highlight=0,
            width=3.2,
        ).shift(DOWN * 2)

        self.play(Write(q))
        self.play(q.animate.add("compile"))
        self.play(q.animate.pop(0))
        self.play(q.animate.pop(0))
        self.play(q.animate.pop(0))
        self.play(q.animate.pop(0))
        self.play(FadeOut(q))

        self.embed()
