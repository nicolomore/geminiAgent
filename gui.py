from textual.widgets import Input, Button, Collapsible, Pretty, Markdown
from textual.containers import Horizontal, VerticalScroll
from plugins.telegramPlugin import telegramPlugin
from textual.app import App, ComposeResult
from textual import on, work
import manager
import agent

class Bubble(Horizontal):
    def __init__(self, text : str, role : str):
        super().__init__()
        self.text = text
        self.role = role
        self.add_class(role)

    
    def compose(self) -> ComposeResult:
        yield Markdown(markdown=self.text, classes="contenuto")

class GUI(App):
    CSS_PATH = "/home/batman/progetti/agenteV2/style.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager.instance = self

    def _on_mount(self, event):
        self.query_one("#input", Input).focus()


    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        with Horizontal(id="inputBar"):
            yield Button(label="+", id="allega")
            yield Input(placeholder="prompt", id="input")
            yield Button(label=">", id="invia")
    
    def setAgent(self, agent: agent.Agent):
        self.agent = agent

   
    @work(exclusive=True)
    async def rispondi(self, prompt : str):
        chat = self.query_one("#chat", VerticalScroll)
        risposta = await self.agent.answer(prompt)
        if(risposta.text):
            pannelloGem = Bubble(text=risposta.text, role="ai")
            chat.mount(pannelloGem)
            chat.scroll_end()
    
    @on(Button.Pressed, "#invia")
    @on(Input.Submitted, "#input")
    async def printMessage(self):
        input = self.query_one("#input", Input)
        chat = self.query_one("#chat", VerticalScroll)
        prompt = input.value
        input.value = ""
        pannelloTu = Bubble(text=prompt, role="user")
        await chat.mount(pannelloTu)
        chat.scroll_end()
        input.focus()
        self.rispondi(prompt)
    
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
    manager.initGmail()
    agente = agent.Agent()
    agente.setSystemPrompt("""
        Sei un assistente AI avanzato e un agente di sistema locale. Interagisci con l'utente tramite un'interfaccia a riga di comando (TUI) avanzata.

        Hai a disposizione un vasto arsenale di strumenti per interagire con il sistema operativo (Linux), esplorare e modificare file, testare codice Python, inviare email, scaricare media, cercare sul web e gestire una memoria a lungo termine. Usa questi strumenti in modo proattivo e autonomo per completare le richieste dell'utente.

        STILE E COMPORTAMENTO:
        - Comportati come un sysadmin o un "copilota" per programmatori: sii conciso, tecnico, preciso e vai dritto al punto. Evita convenevoli inutili.
        - Se l'utente ti chiede di fare qualcosa sul sistema (es. "creami questo file", "cerca questo errore", "aggiorna la task"), USA I TOOL prima di rispondere e poi conferma all'utente l'esito dell'operazione, mostrando eventuali output rilevanti.
        """)
    agente.addTools([telegramPlugin.sendFileTool])
    agente.start()
    app = GUI()
    app.setAgent(agente)
    app.run()