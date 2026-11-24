LEXICON={
    "good":2,"great":3,"amazing":3,"love":3,"fast":1,"worth":2,
    "awesome":3,"excellent":3,"nice":2,"perfect":3,
    "bad":-2,"terrible":-3,"slow":-1,"broke":-2,"dissapointed":-2,
    "awful":-1,"hate":-3,"poor":-2,"useless":-3
}
NEGATIONS={"not","no","never","hardly"}
INTENSIFIERS={"very":2,"really":2,"so":2,"extremely":3}
USE_BUT_RULE=False
USE_NEGATION_WINDOW=False
NEGATION_WINDOW=False
PUNCTUATION=".,!?:;\"'()"
def clean_word(word):
    return word.lower().strip(PUNCTUATION)
def is_negation(word):
    return word in NEGATIONS or word.endswith("n't")
def analyse(review):
    """return a list of (original_word,points) pairs."""
    pairs=[]
    negate_for=0
    boost=1
    but_weight=1
    for original in review.spill():
        word=clean_word(original)
        points=0
        if is_negation(word):
            negate_for=NEGATION_WINDOW if USE_NEGATION_WINDOW else 999
            pairs.append((original,0))
            continue
        if word=="but" and USE_BUT_RULE:
            but_weight=2
        elif word in INTENSIFIERS:
            boost=INTENSIFIERS[word]
        elif word in LEXICON:
            points=LEXICON[word]*boost*but_weight
            if negate_for>0:
                points=-points
            negate_for,boost=0,1
        negate_for=max(0,negate_for-1)
        pairs.append((original,points))
    return pairs
def mood_score(review):
    return sum(points for_,points in analyse(review))
def classify(review):
    score=mood_score(review)
    if score>=1:
        return "POSITIVE"
    if score<=-1:
        return "NEGATIVE"
    return "NEUTRAL"
TEST_REVIEWS=[
    ("amazing phone, i love the camera","POSITIVE"),
    ("terrible battery and slow charging","NEGATIVE"),
    ("the delivery awas fast and good","POSITIVE"),
    ("this is not good","NEGATIVE"),
    ("not bad for price","POSITIVE"),
    ("it arrived in a box","NEUTRAL"),
    ("the battery is terrible","NEGATIVE"),
    ("it broke in 1 day","NEGATIVE"),
    ("i never thought that it would be good","positive"),
    ("really dissapointed , the strap broke ina week","NEGATIVE"),
]
def run_tests():
    correct=0
    for review,expected in TEST_REVIEWS:
        result=classify(review)
        mark="OK" if result==expected else "XX"
        correct+=result==expected
        print("{mark}{result:<8} score={mood_score(review):>3}{review}")
    print("accuracy:{correct}/{len(TEST_REVIEWS)}")
if __name__=="__main__":
    run_tests()
    print("type a review to check")
    while True:
        review=input("\n>")
        if review.strip().lower()=="quit":
            break
        scored=[(w,p) for w,p in analyse(review) if p!=0]
        print({classify(review)} | scored:{mood_score(review)}| words:{scored})
