import flet as ft
import pyperclip, sample_questions


FILES = ("home.txt", "boys.txt", "axe.xlsx", "names.xlsx")
QUESTIONS = (qtn for qtn in sample_questions.QUESTIONS)
num_qtns = sum(1 for _ in sample_questions.QUESTIONS)
qtns_left = num_qtns


def save_explanation(exp: str, qtn: dict = {}) -> dict:
    qtn.update({"Explanation": exp})
    # do other stuff with the updated question
    # print(f"Explanation added successfully\n{qtn}")


def save_document():
    print("Save document with explanations")


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


def get_next_question():
    return next(QUESTIONS, "NO MORE QUESTIONS")


def set_questions():
    print(f"Set QUESTIONS from {set_file.value}")
    # to be accomplished by script


def set_prompt():
    global qtns_left
    rationale_text.value = ""
    rationale_text.update()
    toggle_exp_btn_state()

    input_text.value = get_next_question()
    input_text.update()

    qtns_left = qtns_left - 1 if qtns_left > 0 else 0
    counter.text = f"{qtns_left}/{num_qtns}"
    counter.update()

    if not qtns_left:
        nxt_qtn_btn.disabled = True
        nxt_qtn_btn.update()


nxt_qtn_btn = ft.OutlinedButton(
    "Next Question",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
    ),
    on_click=lambda e: set_prompt(),
)

explanation_btn = ft.OutlinedButton(
    "Add Explanation",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
    ),
    disabled=True,
    on_click=lambda e: save_explanation(rationale_text.value),
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
    label="Choose file to use",
    width=280,
    options=[ft.dropdown.Option(file) for file in FILES],
    value=FILES[0] if FILES else "---No Files Specified---",
    on_change=lambda e: set_questions(),
)

counter = ft.TextButton(text=f"{qtns_left}/{num_qtns}", disabled=True)


def main(page: ft.Page):
    page.window_width = 600
    page.window_height = 900
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.AppBar(title=ft.Text(value="Utility App", style="bold")),
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
        ft.Container(
            content=ft.FilledButton(
                "Update Document",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                on_click=lambda e: save_document(),
            )
        ),
    )
    page.update()


ft.app(target=main)
