from pandas import DataFrame
from typing import Any, Generator
import flet as ft
import pyperclip
import utils


PROMPT_POSTFIX = "\nProvide a simple, precise, comprehensive, and concise rationale for the correct answer."
QUESTIONS: Generator[dict[str, Any], Any, None] | None = None
num_qtns: int = 0
qtns_left: int = 0
current_question: dict = {}
df: DataFrame | None = None
feedback: str = ""


def save_explanation(qtn: dict = {}) -> dict:
    global df, feedback

    if (index := qtn.get("i", None)) is not None:
        utils.set_explanation_detail(df, int(index), rationale_text.value)
        feedback = "Explanation Added!"
    else:
        feedback = "FAILED!"

    # print(feedback)


def save_document():
    global df
    utils.save_changes(df, set_file.value)
    # print("Success")


def set_explanation():
    rationale_text.value = pyperclip.paste()
    rationale_text.update()
    toggle_exp_btn_state()


def toggle_exp_btn_state():
    if rationale_text.value:
        explanation_btn.disabled = False
    else:
        explanation_btn.disabled = True
    explanation_btn.update()


def toggle_update_doc_btn_state():
    if set_file.value:
        update_doc_btn.disabled = False
    else:
        update_doc_btn.disabled = True
    update_doc_btn.update()


def toggle_nxt_qtn_btn_state():
    if input_text.value:
        nxt_qtn_btn.disabled = False
    else:
        nxt_qtn_btn.disabled = True

    nxt_qtn_btn.update()


def get_next_question():
    global current_question
    next_q = None
    if QUESTIONS:
        next_q = next(QUESTIONS, None)
        if isinstance(next_q, dict):
            current_question = next_q.copy()
            index = next_q.pop("i", None)

            next_q = utils.pretty_print_dict(next_q) + PROMPT_POSTFIX

    return next_q


def set_questions():
    global QUESTIONS, num_qtns, qtns_left, df
    try:
        df, target_qtnz = utils.extract_df(utils.FILES.get(set_file.value))
        QUESTIONS = utils.fetch_incomplete_MCQ(target_qtnz)
        num_qtns = sum(1 for _ in utils.fetch_incomplete_MCQ(target_qtnz))
        qtns_left = num_qtns + 1
    except ValueError:
        ...
    finally:
        set_prompt()
        toggle_nxt_qtn_btn_state()
        toggle_update_doc_btn_state()


def set_prompt():
    global qtns_left, num_qtns
    rationale_text.value = ""
    rationale_text.update()
    toggle_exp_btn_state()

    input_text.value = get_next_question()
    input_text.update()

    qtns_left = qtns_left - 1 if qtns_left > 0 else 0
    counter.text = f"{qtns_left}/{num_qtns}"
    counter.update()

    if qtns_left == 0 or num_qtns == 0:
        nxt_qtn_btn.disabled = True
        nxt_qtn_btn.update()


nxt_qtn_btn = ft.OutlinedButton(
    "Next Question",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
    ),
    disabled=True,
    on_click=lambda e: set_prompt(),
)

explanation_btn = ft.OutlinedButton(
    "Add Explanation",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
    ),
    disabled=True,
)

update_doc_btn = ft.FilledButton(
    "Update Document",
    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    disabled=True,
)

input_text = ft.TextField(
    value=get_next_question(),
    label="Prompt",
    label_style=ft.TextStyle(
        size=16,
        weight="bold",
        color=ft.colors.AMBER_900,
    ),
    min_lines=6,
    max_lines=8,
    multiline=True,
    read_only=True,
    text_size=11,
    border_width=0,
)

rationale_text = ft.TextField(
    hint_text="Paste Explanation here",
    min_lines=8,
    max_lines=8,
    multiline=True,
    text_size=12,
    border_width=0,
    on_change=lambda e: toggle_exp_btn_state(),
)

prompt_field = ft.Stack(
    [
        ft.Container(content=ft.Card(content=input_text), padding=15),
        ft.Container(
            content=ft.Icon(
                name=ft.icons.COPY_OUTLINED,
                size=35,
                opacity=0.3,
                color="grey",
            ),
            on_click=lambda e: pyperclip.copy(input_text.value),
            alignment=ft.alignment.top_right,
            # width=35,
        ),
    ]
)

rationale_field = ft.Stack(
    [
        ft.Container(content=ft.Card(content=rationale_text), padding=15),
        ft.Container(
            content=ft.Icon(
                name=ft.icons.PASTE_OUTLINED,
                size=35,
                opacity=0.3,
                color="grey",
            ),
            on_click=lambda e: set_explanation(),
            alignment=ft.alignment.top_right,
            # width=35,
        ),
    ]
)

set_file = ft.Dropdown(
    label="Choose File To Use",
    width=280,
    options=[ft.dropdown.Option(filename) for filename in utils.FILES],
    on_change=lambda e: set_questions(),
)

counter = ft.TextButton(text=f"{qtns_left}/{num_qtns}", disabled=True)


def main(page: ft.Page):
    page.scroll = "hidden"
    page.window_width = 600
    page.window_height = 900
    page.window_opacity = 0.98
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    explanation_btn.on_click = lambda e: save_action("Explanation Added")
    update_doc_btn.on_click = lambda e: save_action("File Updated")

    page.add(
        ft.AppBar(
            title=ft.Text(value="Utility App", style="bold"),
            actions=[
                ft.Container(
                    content=ft.Icon(
                        ft.icons.REFRESH_OUTLINED,
                        size=35,
                        color=ft.colors.AMBER_ACCENT_100,
                    ),
                    margin=10,
                    padding=5,
                    visible=False
                    # on_click=lambda e: page.update(),
                )
            ],
        ),
        ft.Divider(opacity=0.5),
        set_file,
        ft.Divider(opacity=0.5),
        ft.Container(
            content=ft.Column(
                [
                    prompt_field,
                    ft.Row(
                        [counter, nxt_qtn_btn],
                        spacing=35,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                horizontal_alignment="center",
            ),
            padding=5,
        ),
        ft.Divider(opacity=0.5),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Explanation",
                        text_align="center",
                        size=20,
                        color=ft.colors.BLUE_300,
                        weight="bold",
                    ),
                    rationale_field,
                    ft.Row(
                        [explanation_btn],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                horizontal_alignment="center",
            ),
            padding=5,
        ),
        ft.Divider(height=15, thickness=3),
        ft.Container(content=update_doc_btn),
    )

    page.update()

    def save_action(msg: str):
        if msg.startswith("File"):
            save_document()
            set_questions()
        else:
            save_explanation(current_question)

        page.show_snack_bar(
            ft.SnackBar(
                ft.Text(
                    f"{msg} Successfully!",
                    weight="bold",
                    size=20,
                    text_align="center",
                    color="#02fea6",
                ),
                open=True,
                duration=1500,
                bgcolor="#484848",
            )
        )


ft.app(target=main)
