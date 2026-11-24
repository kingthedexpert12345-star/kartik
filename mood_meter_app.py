import gradio as gr
from mood_meter import analyse,classify,mood_score
COLORS={"positive":"lightgreen","negative":"salmon"}
def check(review):
    pieces=[]
    for word,points in analyse(review):
        if points>0:
            label="positive"
        elif points<0:
            label="negative"
        else:
            label=None
        pieces.append((word+" ",label))
        return classify(review),mood_score(review),pieces
demo=gr.Interface(
    fn=check,
    inputs=gr.Textbox(lines=3,label="padte a review"),
    outputs=[
        gr.Texbox(label="Mood"),
        gr.Number(label="mood score"),
        gr.HighlightedText(label="which words decided it ?",color_map=COLORS),
    ],
    title="review mood meter",
    description="green words add points and red cuts points",
    examples=[
        ["amazing phone , i love the camera"],
        ["this is not good at all"],
        ["the screen is great but battery is terrible"],
    ],
)
if __name__=="__main__":
    demo.launch()
