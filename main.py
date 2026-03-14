from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input, Button, Static
from textual.containers import Horizontal, VerticalScroll
from textual import on, work
from answer import *
import manager

class Bubble(Horizontal):
    def __init__(self, text : str, role : str):
        super().__init__()
        self.text = text
        self.role = role
        self.add_class(role)

    def compose(self) -> ComposeResult:
        yield Static(content=self.text, classes="contenuto")

class GUI(App):
    CSS_PATH = "/home/batman/progetti/agenteV2/style.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager.instance = self
    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        with Horizontal(id="inputBar"):
            yield Button(label="+", id="allega")
            yield Input(placeholder="prompt", id="input")
            yield Button(label=">", id="invia")
        
    @on(Button.Pressed, "#invia")
    @on(Input.Submitted, "#input")
    @work(exclusive=True, thread=True)
    async def rispondi(self):
        input = self.query_one("#input", Input)
        chat = self.query_one("#chat", VerticalScroll)
        prompt = input.value
        input.value = ""
        pannelloTu = Bubble(text=prompt, role="user")
        self.call_from_thread(chat.mount, pannelloTu)
        self.call_from_thread(chat.scroll_end)
        self.call_from_thread(input.focus)
        risposta = await answer(prompt)
        if(risposta.text):
            pannelloGem = Bubble(text=Markdown(risposta.text), role="ai")
            self.call_from_thread(chat.mount, pannelloGem)
            self.call_from_thread(chat.scroll_end)
    def onToolCall(self, tool : str):
        chat = self.query_one("#chat", VerticalScroll)
        chat.mount(Bubble(text=tool, role="ai"))
        chat.scroll_end()
        

if __name__ == "__main__":
    initGmail()
    app = GUI()
    app.run()