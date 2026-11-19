import gradio as gr
from spam_shield import THRESHOLD,classify,explain,spam_score
def check(message):
    flagged=", ".join(explain(message))
    return classify(message,spam_score(message),flagged)
demo=gr.Interface(
    fn=check,
    inputs=gr.Textbox(lines=3,label="paste a message"),
    outputs=[
        gr.Textbox(label="verdict"),
        gr.Number(label="spam score"),
        gr.Textbox(label="words that raised the score"),    
    ],
    title="spam shield",
    description="every spam word adds points. a score of %d or more means SPAM"%
THRESHOLD,
    examples=[
        ["congratulations you won a free iphone"],
        ["hey are we still meeting at 5?"],
        ["click the link for free quiz now"],
    ],
) 
if __name__=="__main__":
    demo.launch()