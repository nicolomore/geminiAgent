from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, Collapsible, Pretty
from textual.containers import Horizontal, VerticalScroll
from textual import on, work
from agent import *
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
    
    def setAgent(self, agent: Agent):
        self.agent = agent

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
        risposta = await self.agent.answer(prompt)
        if(risposta.text):
            pannelloGem = Bubble(text=Markdown(risposta.text), role="ai")
            self.call_from_thread(chat.mount, pannelloGem)
            self.call_from_thread(chat.scroll_end)
    def onToolCall(self, toolName : str, params : tuple, kparams : dict[str, any], output : str):
        chat = self.query_one("#chat", VerticalScroll)
        data = {
            "Params": params,
            "KwParams": kparams,
            "Output": output
        }
        content = Pretty(data)
        chat.mount(Collapsible(content, title=toolName))
        chat.scroll_end()
        

if __name__ == "__main__":
    initGmail()
    agente = Agent()
    agente.start()
    app = GUI()
    app.setAgent(agente)
    app.run()
    app.query_one("#input", Input).focus()