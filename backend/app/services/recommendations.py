from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def recommend_events(interests:str,skills:str,events:list,limit=5):
    if not events:return[]
    profile=f"{interests} {skills}".strip() or "general campus"
    corpus=[profile]+[f"{e.title} {e.description} {e.category} {e.skills}" for e in events]
    matrix=TfidfVectorizer(stop_words="english").fit_transform(corpus);scores=cosine_similarity(matrix[0:1],matrix[1:]).flatten()
    ranked=sorted(zip(events,scores),key=lambda x:x[1],reverse=True)[:limit]
    return [{"event_id":e.id,"title":e.title,"score":round(float(s),3),"reason":f"Matches your interests in {e.category}" if s>0 else "Broad campus relevance"} for e,s in ranked]
