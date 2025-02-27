from __future__ import annotations

from importlib.metadata import version
from pathlib import Path
from typing import cast

from rich import box
from rich.console import RenderableType
from rich.json import JSON
from rich.markdown import Markdown
from rich.markup import escape
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    RichLog,
    Static,
    Switch,
)

## Table
from_markup = Text.from_markup
example_table = Table(
    show_edge=False,
    show_header=True,
    expand=True,
    row_styles=["none", "dim"],
    box=box.SIMPLE,
)
example_table.add_column(from_markup("[green]Date"), style="green", no_wrap=True)
example_table.add_column(from_markup("[blue]Title"), style="blue")
example_table.add_column(
    from_markup("[magenta]Box Office"),
    style="magenta",
    justify="right",
    no_wrap=True,
)
example_table.add_row(
    "Dec 20, 2019",
    "Star Wars: The Rise of Skywalker",
    "$375,126,118",
)
example_table.add_row(
    "May 25, 2018",
    from_markup("[b]Solo[/]: A Star Wars Story"),
    "$393,151,347",
)
example_table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    from_markup("[bold]$1,332,539,889[/bold]"),
)
example_table.add_row(
    "May 19, 1999",
    from_markup("Star Wars Ep. [b]I[/b]: [i]The phantom Menace"),
    "$1,027,044,677",
)


## Markdown Stuff
WELCOME_MD = """

## Tash 〰️

**Welcome**! Textual is a framework for creating sophisticated applications with the terminal.
"""
RICH_MD = """

Textual is built on **Rich**, the popular Python library for advanced terminal output.

Add content to your Textual App with Rich *renderables* (this text is written in Markdown and formatted with Rich's Markdown class).

Here are some examples:
"""
CSS_MD = """

Textual uses Cascading Stylesheets (CSS) to create Rich interactive User Interfaces.

- **Easy to learn** - much simpler than browser CSS
- **Live editing** - see your changes without restarting the app!

Here's an example of some CSS used in this app:
"""
DATA = {
    "foo": [
        3.1427,
        (
            "Paul Atreides",
            "Vladimir Harkonnen",
            "Thufir Hawat",
            "Gurney Halleck",
            "Duncan Idaho",
        ),
    ],
}
WIDGETS_MD = """

Textual widgets are powerful interactive components.

Build your own or use the builtin widgets.

- **Input** Text / Password input.
- **Button** Clickable button with a number of styles.
- **Switch** A switch to toggle between states.
- **DataTable** A spreadsheet-like widget for navigating data. Cells may contain text or Rich renderables.
- **Tree** An generic tree with expandable nodes.
- **DirectoryTree** A tree of file and folders.
- *... many more planned ...*
"""
MESSAGE = """
We hope you enjoy using Textual.

Here are some links. You can click these!

[@click="app.open_link('https://textual.textualize.io')"]Textual Docs[/]

[@click="app.open_link('https://github.com/Textualize/textual')"]Textual GitHub Repository[/]

[@click="app.open_link('https://github.com/Textualize/rich')"]Rich GitHub Repository[/]


Built with ♥  by [@click="app.open_link('https://www.textualize.io')"]Textualize.io[/]
"""
JSON_EXAMPLE = """{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}   
"""

class Menu(Static):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Courses", id="courses")
        yield Button("Your Courses", id="your_courses")
        yield Button("Progress", id="progress")
        yield Button("Practice", id="practice")
        yield Button("Projects", id="projects")
        yield Button("Sandbox", id="sandbox")
        yield Button("Dashboard", id="dashboard")
        yield Button("Docs", id="docs")
        yield Button("AI Assistant", id="ai_assistant")
        yield Button("Resources", id="resources")


class Home(ScrollableContainer):
    pass

class Courses(ScrollableContainer):
    pass

class Dashboard(ScrollableContainer):
    pass

class Title(Static):
    pass


class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Switch(value=self.app.dark)
        yield Static("Dark mode toggle", classes="label")

    def on_mount(self) -> None:
        self.watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self) -> None:
        self.query_one(Switch).value = self.app.dark

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.app.dark = event.value


class Welcome(Container):
    ALLOW_MAXIMIZE = True

    def compose(self) -> ComposeResult:
        yield Static(Markdown(WELCOME_MD))
        yield Button("Start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast(TashApp, self.app)
        app.add_note("[b magenta]Start!")
        app.query_one(".location-first").scroll_visible(duration=0.5, top=True)


class OptionGroup(Container):
    pass


class SectionTitle(Static):
    pass


class Message(Static):
    pass


class Version(Static):
    def render(self) -> RenderableType:
        return f"[b]v{version('textual')}"


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("Textual Demo")
        yield OptionGroup(Message(MESSAGE), Version())
        yield DarkSwitch()


class AboveFold(Container):
    pass


class Section(Container):
    pass


class Column(Container):
    pass


class TextContent(Static):
    pass


class QuickAccess(Container):
    pass


class LocationLink(Static):
    def __init__(self, label: str, reveal: str) -> None:
        super().__init__(label)
        self.reveal = reveal

    def on_click(self) -> None:
        app = cast(TashApp, self.app)
        app.query_one(self.reveal).scroll_visible(top=True, duration=0.5)
        app.add_note(f"Scrolling to [b]{self.reveal}[/b]")


class LoginForm(Container):
    ALLOW_MAXIMIZE = True

    def compose(self) -> ComposeResult:
        yield Static("Username", classes="label")
        yield Input(placeholder="Username")
        yield Static("Password", classes="label")
        yield Input(placeholder="Password", password=True)
        yield Static()
        yield Button("Login", variant="primary")


class Window(Container):
    pass


class SubTitle(Static):
    pass


class TashApp(App[None]):
    CSS_PATH = "demo.tcss"
    TITLE = "Tash by Savant"
    BINDINGS = [
        ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f1", "app.toggle_class('RichLog', '-hidden')", "Notes"),
        Binding("ctrl+q", "app.quit", "Quit", show=True),
    ]

    show_sidebar = reactive(False)

    def add_note(self, renderable: RenderableType) -> None:
        self.query_one(RichLog).write(renderable)


    def compose(self) -> ComposeResult:
        example_css = Path(self.css_path[0]).read_text()
        yield Header(show_clock=True)
        with Container(id="menu"):
            yield Button("Home", id="btn_view1")
            yield Button("Explore", id="btn_view2")
            yield Button("Your Courses", id="btn_view3")
            yield Button("Progress", id="btn_view4")
            yield Button("Training", id="btn_view5")
            yield Button("Projects", id="btn_view6")
            yield Button("Assistant", id="btn_view7")
        
        with ScrollableContainer(id="content"):
            with Container(id="view1", classes="view active"):
                # example_css = Path(self.css_path[0]).read_text()
                # RichLog(classes="-hidden", wrap=False, highlight=True, markup=True)
                yield ScrollableContainer(
                Column(
                    Section(
                        SectionTitle("Rich"),
                        TextContent(Markdown(RICH_MD)),
                        SubTitle("Pretty Printed data (try resizing the terminal)"),
                        Static(Pretty(DATA, indent_guides=True), classes="pretty pad"),
                        SubTitle("JSON"),
                        Window(Static(JSON(JSON_EXAMPLE), expand=True), classes="pad"),
                        SubTitle("Tables"),
                        Static(example_table, classes="table pad"),
                    ),
                    classes="location-rich",
                ),
                )
            with ScrollableContainer(id="view2", classes="view"):
                yield Static("This is View 2 content")
            with ScrollableContainer(id="view3", classes="view"):
                yield Static("This is View 1 content")
            with ScrollableContainer(id="view4", classes="view"):
                yield Static("This is View 2 content")
            with ScrollableContainer(id="view5", classes="view"):
                yield Static("This is View 1 content")
            with ScrollableContainer(id="view6", classes="view"):
                yield Static("This is View 2 content")
            with ScrollableContainer(id="view7", classes="view"):
                yield Static("This is View 2 content")
            
            yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_view1":
            self.activate_view("view1")
        elif event.button.id == "btn_view2":
            self.activate_view("view2")
        elif event.button.id == "btn_view3":
            self.activate_view("view3")
        elif event.button.id == "btn_view4":
            self.activate_view("view4")
        elif event.button.id == "btn_view5":
            self.activate_view("view5")
        elif event.button.id == "btn_view6":
            self.activate_view("view6")
        elif event.button.id == "btn_view7":
            self.activate_view("view7")

    def activate_view(self, view_id: str) -> None:
        for view in self.query(".view"):
            view.remove_class("active")
        self.query_one(f"#{view_id}").add_class("active")
    
    


    # def compose(self) -> ComposeResult:
    #     example_css = Path(self.css_path[0]).read_text()
    #     yield Container(
    #         Sidebar(classes="-hidden"),
    #         Header(show_clock=True),
    #         RichLog(classes="-hidden", wrap=False, highlight=True, markup=True),
    #         Home(
    #             QuickAccess(
    #                 Dashboard("Dashboard", ".dashboard"),
    #                 Courses("Courses", ".location-widgets"),
    #                 LocationLink("Rich content", ".location-rich"),
    #                 LocationLink("CSS", ".location-css"),
    #             ),
    #             AboveFold(Welcome(), classes="location-top"),
    #             Column(
    #                 Section(
    #                     SectionTitle("Widgets"),
    #                     TextContent(Markdown(WIDGETS_MD)),
    #                     LoginForm(),
    #                     DataTable(),
    #                 ),
    #                 classes="location-widgets location-first",
    #             ),
    #             Column(
    #                 Section(
    #                     SectionTitle("Rich"),
    #                     TextContent(Markdown(RICH_MD)),
    #                     SubTitle("Pretty Printed data (try resizing the terminal)"),
    #                     Static(Pretty(DATA, indent_guides=True), classes="pretty pad"),
    #                     SubTitle("JSON"),
    #                     Window(Static(JSON(JSON_EXAMPLE), expand=True), classes="pad"),
    #                     SubTitle("Tables"),
    #                     Static(example_table, classes="table pad"),
    #                 ),
    #                 classes="location-rich",
    #             ),
    #             Column(
    #                 Section(
    #                     SectionTitle("CSS"),
    #                     TextContent(Markdown(CSS_MD)),
    #                     Window(
    #                         Static(
    #                             Syntax(
    #                                 example_css,
    #                                 "css",
    #                                 theme="material",
    #                                 line_numbers=True,
    #                             ),
    #                             expand=True,
    #                         )
    #                     ),
    #                 ),
    #                 classes="location-css",
    #             ),
    #         ),
    #         Dashboard(
    #             Column(
    #                 Section(
    #                     SectionTitle("Rich"),
    #                     TextContent(Markdown(RICH_MD)),
    #                     SubTitle("Pretty Printed data (try resizing the terminal)"),
    #                     Static(Pretty(DATA, indent_guides=True), classes="pretty pad"),
    #                     SubTitle("JSON"),
    #                     Window(Static(JSON(JSON_EXAMPLE), expand=True), classes="pad"),
    #                     SubTitle("Tables"),
    #                     Static(example_table, classes="table pad"),
    #                 ),
    #                 classes="location-rich",
    #             ), classes="dashboard",
    #         ),
    #     )
    #     # yield Container(
    #     #     Sidebar(classes="-hidden"),
    #     #     Header(show_clock=True),
    #     #     RichLog(classes="-hidden", wrap=False, highlight=True, markup=True),

    #     # )
        

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser

        webbrowser.open(link)

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

    # def on_mount(self) -> None:
    #     self.add_note("Textual Demo app is running")
    #     table = self.query_one(DataTable)
    #     table.add_column("Foo", width=20)
    #     table.add_column("Bar", width=20)
    #     table.add_column("Baz", width=20)
    #     table.add_column("Foo", width=20)
    #     table.add_column("Bar", width=20)
    #     table.add_column("Baz", width=20)
    #     table.zebra_stripes = True
    #     for n in range(20):
    #         table.add_row(*[f"Cell ([b]{n}[/b], {col})" for col in range(6)])
    #     self.query_one("Welcome Button", Button).focus()

    def action_screenshot(self, filename: str | None = None, path: str = "./") -> None:
        """Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.

        Args:
            filename: Filename of screenshot, or None to auto-generate.
            path: Path to directory.
        """
        self.bell()
        path = self.save_screenshot(filename, path)
        message = f"Screenshot saved to [bold green]'{escape(str(path))}'[/]"
        self.add_note(Text.from_markup(message))
        self.notify(message)


# app = TashApp()
if __name__ == "__main__":
    TashApp().run()