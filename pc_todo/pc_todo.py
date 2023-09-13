""" Pynecone Todoapp"""
from pcconfig import config
import datetime
import uuid
import asyncio
import pynecone as pc


from . import style

# generate id
def generate_id():
    return str(uuid.uuid4())


# database model
class Task(pc.Model, table=True):
    uuid: str
    date: str
    task: str


class State(pc.State):
    task: str

    task_list: list[list]

    def update_task_field(self, task):
        self.task = task

    async def add_task(self):
        self.task_list += [
            [
                generate_id(),
                datetime.datetime.now().strftime("%B %d, %Y %H:%M"),
                self.task,
            ]
        ]

        self.task = ""


def display_task(task) -> pc.Component:
    return pc.container(
        pc.hstack(
            pc.container(
                pc.vstack(
                    pc.container(
                        pc.text(
                            task[1],
                            font_size="10px",
                            font_weight="light",
                            color="grey",
                        ),
                    ),
                    pc.container(
                        pc.text(
                            task[2],
                            font_size="14px",
                        ),
                    ),
                    spacing="1px",
                ),
                padding="0px",
            )
        ),
        border_bottom="1px solid dodgerblue",
        width="320px",
        height="60px",
        padding="0px",
        display="flex",
        # justify_content="center",
    )


def sidebar():
    return pc.box(
        pc.vstack(
            pc.image(src="/favicon.ico", margin="0 auto"),
            pc.heading(
                "Sidebar",
                text_align="center",
                margin_bottom="1em",
            ),
            pc.menu("..."),
            width="250px",
            padding_x="2em",
            padding_y="1em",
        ),
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        z_index="500",
    )


def navbar() -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.image(src="favicon.ico", background_color="white"),
            pc.box(
                pc.heading("My App", font_size="2em"),
                pc.box(
                    pc.menu(
                        pc.menu_button(
                            pc.icon(
                                tag="hamburger",
                                font_size="24px",
                            )
                        ),
                        pc.menu_list(
                            pc.menu_item('Home'),
                            pc.menu_item('Search'),
                            pc.menu_item('Logout'),
                            color="black"
                        ),
                        style=style.menu_style,
                    ),
                    width="auto"
                ),
                display="flex",
                align_items="center",
                justify_content="space-between",
                width="100%",
                padding="0px 10px"
            ),
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="5",
        background_color="black",
        color="white",
        padding="0px 10px"
    )


# text input field
def task_input_field() -> pc.Component:
    return pc.container(
        # pc.vstack(
        #     pc.container(
        #         pc.text(
        #             "PyneCone: To-Do App",
        #             font_size="24px",
        #             font_weight="900",
        #             text_align="center",
        #             color="#4e4095",
        #             style={
        #                 "background-clip": "text",
        #                 "background-image": "linear-gradient(to right, #4b79a1, #283e51, #4b79a1)",
        #                 "-webkit-background-clip": "text",
        #                 "-webkit-text-fill-color": "transparent",
        #             },
        #         ),
        #         display="flex",
        #         align_items="center",
        #         justify_content="center",
        #         center_content=True,
        #     ),
        #     pc.spacer(),
        pc.hstack(
            pc.input(
                value=State.task,
                padding="5px",
                width="300px",
                height="45px",
                border="1px solid dodgerblue",
                border_radius="10px",
                focus_border="transparent",
                on_change=lambda value: State.update_task_field(value),
            ),
            pc.button(
                pc.icon(
                    tag="add",
                    font_size="20px",
                ),
                color="#4b79a1",
                on_click=lambda: State.add_task(),
            ),
            spacing="8px",
        ),
    )
    # )


def index() -> pc.Component:
    return pc.box(
        navbar(),
        pc.vstack(
            pc.spacer(),
            pc.desktop_only(
                pc.box(
                pc.vstack(
                    pc.foreach(
                        State.task_list,
                        display_task,
                    ),
                    width="400px",
                    height="500px",
                    overflow="hidden",
                ),
                height="500px",
                overflow="hidden",
                border_radius="10px",
                padding_bottom="10px",
                box_shadow="7px -7px 14px #cccecf, -7px 7px 14px #ffffff",
                ),
                pc.container(task_input_field()),
            ),
            pc.mobile_and_tablet(
                pc.box(
                    pc.vstack(
                        pc.foreach(
                            State.task_list,
                            display_task,
                        ),
                        width="100%",
                        height="100%",
                        overflow="hidden",
                    ),
                    height="500px",
                    overflow="hidden",
                    border_radius="10px",
                    padding_bottom="10px",
                    box_shadow="7px -7px 14px #cccecf, -7px 7px 14px #ffffff",
                ),
                pc.box(task_input_field()),
            ),
        ),
        bg="#ebedee",
        height="100%",
        position="fixed",
        width="100%",
        # display="grid",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
