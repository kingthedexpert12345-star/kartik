SPAM_WORDS={
    "free":2,"winner":3,"won":3,"prize":3,"lottery":3,
    "urgent":2,"click":2,"claim":2,"cash":2,"verify":2,
    "congratulations":2,"offer":1,"limited":1,"now":1,"account":1,
}
THRESHOLD=4
USE_LEET=False
LEET = str.maketrans("13450@$", "ieasoas")
PUNCTUATION=".,!?:;\"'()"
def clean_word(word):
    word=word.lower()
    if USE_LEET:
        word=word.translate(LEET)
    return word.strip(PUNCTUATION)
def tokenize(message):
    words=[]
    for word in message.split():
        cleaned=clean_word(word)
        if cleaned:
            words.append(cleaned)
    return words
def spam_score(message):
    score=0
    for word in tokenize(message):
        score +=SPAM_WORDS.get(word,0)
    return score
def classify(messgae):
    if spam_score(messgae)>=THRESHOLD:
        return "SPAM"
    return "SAFE"
def explain(message):
    return [word for word in tokenize(message) if word in SPAM_WORDS]
TEST_MESSAGES=[
    ("congratulations! you won a free iphone. click now to claim","SPAM"),
    ("urgent verify or your account will get blocked","SPAM"),
    ("claim your cash prize","SPAM"),
    ("hey , are we still meeting at 5?","SAFE"),
    ("your free coding class starts in 1 hour","SAFE"),
    ("dinner is ready","SAFE"),
    ("click here for a prize","SPAM"),
    ("free cash for new users","SPAM"),
    ("click here for a new quiz","SAFE"),
    ("your bank account statement is ready","SAFE")
]
def run_test():
    correct=false_positives=false_negatives=0
    for message,expected in TEST_MESSAGES:
        result=classify(message)
        if result==expected:
            correct+=1
            mark="OK"
        elif result=="SPAM":
            false_positives+=1
            mark="FP"
        else:
            false_negatives+=1
            mark="FN"
        print("{mark} {result} score={spam_score(message):>2} {message}")
    print("accuracy: {correct}/{len(TEST_MESSAGES)}")
    print("false positives (safe messages blocked): {false_positives}")
    print("false negatives (spam that got through):{false_negatives}")
if __name__ =="__main__":
    run_test()
    print("type a messgae to check ot quit to stop")
    while True:
        message=input("\n>")
        if message.strip().lower()=="quit":
            break
        print("{classify(message)}| score:{spam_score(message)} | flagged:{explain(message)}")