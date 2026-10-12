"""Preview scenes. From the repo root:

manimgl components/showcase.py CardsShowcase -s -l --file_name cards -c "#171717"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manimlib import DOWN, LEFT, ORIGIN, RIGHT, Scene, UP, VGroup

from components import *  # noqa: F403


def _place(scene, mob):
    use_background(scene)
    fit(mob)
    mob.move_to(ORIGIN)
    scene.add(mob)


class CardsShowcase(Scene):
    def construct(self):
        group = vstack(
            hstack(
                TextCard("AUTH"),
                TextCard("SEARCH", state="ghost"),
                TextCard("YOU", state="outline"),
                StatusCard("worker", "BLOCKED"),
                FileCard("app.db", "53 51 4C 69 74 65", state="filled"),
                buff=0.25,
            ),
            hstack(
                Computer([["vCPU", "vRAM"], ["vDISK", "Kernel"]], accent="Kernel"),
                SpecCard(
                    "Deployment",
                    "/registry/deployments/web",
                    [("copies", "3"), ("image", "web:1.4"), ("port", "8080")],
                ),
                buff=0.4,
                aligned_edge=UP,
            ),
            hstack(
                QuestionCard(1, "How does it\nactually work?"),
                LayerStack(
                    [
                        ("FROM node:20-slim", "CACHED"),
                        ("RUN apt install wget", "REBUILD"),
                        ("COPY package.json .", "REBUILD"),
                    ],
                    width=5.4,
                ),
                buff=0.4,
                aligned_edge=UP,
            ),
            buff=0.35,
        )
        _place(self, group)


class ListsShowcase(Scene):
    def construct(self):
        group = hstack(
            Leaderboard(
                [
                    ("01", "shadowwolf", "9,842"),
                    ("02", "neon_blade", "9,610"),
                    ("03", "phoenix", "9,501"),
                    ("04", "kira_07", "9,354"),
                ],
                highlight=2,
                title="TOP 10",
                subtitle="ZREVRANGE 0 9",
                width=5.2,
            ),
            vstack(
                Checklist(
                    "VERIFYING",
                    "bank.com",
                    [
                        ("Certificate signed by intermediate", "VALID"),
                        ("Intermediate signed by trusted root", "PENDING"),
                        ("Domain matches bank.com", "PENDING"),
                    ],
                    width=7.2,
                ),
                hstack(
                    InstanceCard("web-1", "t3.micro", "10.0.1.24", "running"),
                    JobQueue(
                        ["resize photo", "for user 123", "upload done"],
                        highlight=0,
                        width=3.2,
                    ),
                    CounterStack([997, 998, 999], active=1),
                    buff=0.3,
                    aligned_edge=UP,
                ),
                buff=0.3,
                aligned_edge=LEFT,
            ),
            buff=0.4,
            aligned_edge=UP,
        )
        _place(self, group)


class ChartsShowcase(Scene):
    def construct(self):
        group = vstack(
            hstack(
                Meter(
                    1,
                    eyebrow="RAM EXHAUSTED",
                    value_text="10 GB",
                    color=ORANGE,
                    width=5.2,
                ),
                Meter(
                    0.5,
                    left_label="HALF WRITTEN",
                    right_label="COMPLETE",
                    color=RED,
                    width=4.2,
                    height=0.08,
                ),
                RangeBar("A few hundred", "instant", fill=0.7, width=2.4),
                buff=0.45,
                aligned_edge=DOWN,
            ),
            hstack(
                BarChart(
                    [1.2, 2.0, 2.1, 2.1],
                    labels=["", "", "S3", ""],
                    title="CAPACITY",
                    max_height=1.8,
                ),
                Timeline(
                    [(0.08, "CLIENT"), (0.48, "DISK · BACKEND"), (0.9, "NETWORK")],
                    title="ONE CONNECTION'S LIFETIME",
                    width=7.2,
                ),
                buff=0.4,
                aligned_edge=UP,
            ),
            hstack(
                Heatmap(
                    rows=4,
                    cols=10,
                    tint="gray",
                    cell=0.22,
                    pattern=lambda r, c: ((r * 3 + c * 5) % 7) / 6,
                ),
                TickLine(caption="NO HISTORY"),
                StatBlock("10,400,000", eyebrow="TRADITIONAL DATABASE"),
                FractionCallout(14, 20, "are enough"),
                buff=0.4,
            ),
            buff=0.35,
        )
        _place(self, group)


class DiagramsShowcase(Scene):
    def construct(self):
        tree = Tree(
            {
                "label": "milo",
                "state": "outline",
                "children": [
                    "finn",
                    {
                        "label": "sara",
                        "children": ["tara", {"label": "vera", "link": PURPLE}],
                    },
                ],
            },
            title="INDEX B-TREE",
        )
        group = hstack(
            vstack(
                tree,
                StackFlow(["SQL", "BYTECODE", "VDBE", "PAGER"], node_width=2.2),
                buff=0.3,
            ),
            vstack(
                Fanout(
                    "KAFKA",
                    ["PRODUCER A", "PRODUCER B", "PRODUCER C"],
                    incoming=True,
                    hub_state="filled",
                ),
                Flow(["BROWSER", "SERVER"], states=["outline", "idle"]),
                buff=0.3,
            ),
            vstack(
                HashRing(
                    ["S0", "S1", "S2", "S3", "S4"],
                    highlight=4,
                    center="SHARD 4",
                    caption="the 5th shard",
                    radius=1.45,
                ),
                HashAxis([("A", 0.15), ("B", 0.48), ("C", 0.8)], width=4.5),
                buff=0.35,
            ),
            buff=0.35,
            aligned_edge=UP,
        )
        _place(self, group)


class DataShowcase(Scene):
    def construct(self):
        middle = LabeledRow(
            "P1",
            ["", "1", "2", "3", ""],
            states=["ghost", "filled", "filled", "filled", "ghost"],
            size=0.48,
        )
        partitions = vstack(
            LabeledRow("P0", ["", "", "", "", ""], size=0.48),
            Surround(middle, state="outline", buff=0.1),
            LabeledRow("P2", ["", "", "", "", ""], size=0.48),
            buff=0.12,
        )
        group = hstack(
            vstack(
                LogRow(
                    ["0", "1", "2", "3", "4", "5", "6", "7"],
                    filled=[6],
                    active=7,
                    pointer="APPEND",
                ),
                partitions,
                ChipRow(["the", "QUICK", "and", "Foxes"], accent=[1, 3]),
                buff=0.35,
            ),
            vstack(
                GridTable(
                    ["TERM", "DOCS"],
                    [["fox", "1, 12"], ["brown", "1"], ["quick", "1"]],
                    highlight=0,
                ),
                DataPage(
                    [["1", "ada"], ["2", "grace"], ["3", "lin"]],
                    headers=["id", "name"],
                    cursor=1,
                ),
                CellGrid(
                    rows=3,
                    cols=8,
                    marks={(1, 2): "accent", (1, 3): "danger", (2, 6): "filled"},
                    caption="HYPERVISOR",
                ),
                buff=0.3,
            ),
            vstack(
                CodeBlock(
                    "SELECT name\nFROM users\nWHERE id = 1", language="sql", width=4.4
                ),
                Terminal("terraform plan", output=["No changes."]),
                CodeWindow(
                    'resource "aws_instance" "web" {\n  instance_type = "t3.micro"\n}',
                    language="hcl",
                    title="main.tf",
                    width=5.2,
                ),
                buff=0.25,
                aligned_edge=LEFT,
            ),
            buff=0.35,
            aligned_edge=UP,
        )
        _place(self, group)


class InfraShowcase(Scene):
    def construct(self):
        glyphs = VGroup(*[icon(name, height=0.38) for name in icon_names()])
        glyphs.arrange_in_grid(n_cols=8, buff=0.22)
        group = vstack(
            glyphs,
            hstack(
                ServiceLogo(
                    "RDS", icon_name="expand", subtitle="Relational Database Service"
                ),
                LogoLockup("ZTM", subtitle="LINK IN THE DESCRIPTION"),
                WorldMap(
                    [
                        ("Sydney", 151, -34),
                        ("Virginia", -77, 39),
                        ("Frankfurt", 8.7, 50),
                    ],
                    width=6.2,
                    height=2.6,
                ),
                buff=0.35,
                aligned_edge=UP,
            ),
            hstack(
                Zone(
                    "us-east-1",
                    InstanceCard("web", "t3.micro", footer="running"),
                    InstanceCard("api", "t3.small", footer="running"),
                ),
                PolicyLine("role/photo-app", "s3:PutObject"),
                ReplicaPair("primary down", "new primary"),
                AccessToken("eyJhbGci.payload.sig", expires="EXPIRES IN 00:42:17"),
                buff=0.3,
                aligned_edge=UP,
            ),
            hstack(
                Headline("git", font_size=54),
                Title("SAME PARTITION · ORDER PRESERVED"),
                Note("check the link in the description", highlight="link"),
                DiffStat(2, 1),
                PlanList(
                    [
                        ("+", "aws_instance.web"),
                        ("~", "aws_s3_bucket.logs"),
                        ("-", "aws_db.old"),
                    ]
                ),
                SplitPanel("PLAIN TEXT", "ENCRYPTED", right_state="filled"),
                Formula(["5^7 mod 23 = 17", "5^11 mod 23 = 22"], accent=1),
                TermWeight("data", "0.1"),
                buff=0.28,
            ),
            buff=0.28,
        )
        _place(self, group)
