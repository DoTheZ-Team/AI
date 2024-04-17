from app.database import mongodb
from datetime import datetime
from app.models.hashtag import Hashtag
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
            
class Controller:

    async def test(self):
        return "test 성공"
    
    async def update_hashtag(self, member_id, content):
        member_id = int(member_id)
        hashtag = await mongodb.engine.find_one(Hashtag, Hashtag.member_id == member_id)
        
        if hashtag:
            hashtag.content = hashtag.content + ' ' + content
            hashtag.updated_at = datetime.now()
            await mongodb.engine.save(hashtag)
            print(f"{hashtag.content} 해시태그가 생성되었습니다.")
            
        else:
            hashtag = Hashtag(member_id=member_id, content=content)
            await mongodb.engine.save(hashtag)
            print(f"{content} 해시태그가 생성되었습니다.")
            
        return hashtag
    
    async def recommend_user(self, member_id:int):
        hashtag = await mongodb.engine.find_one(Hashtag, Hashtag.member_id == member_id)
        
        if hashtag:
            all_hashtags = await mongodb.engine.find(Hashtag)
            contents = [hashtag.content for hashtag in all_hashtags]
            member_ids = [hashtag.member_id for hashtag in all_hashtags]
            
            user_index, similarities = self.compute_recommendations(contents, member_ids, member_id)
            
            similar_users_indices = similarities.argsort()[-(30 + 1):-1][::-1]
            similar_users = [member_ids[i] for i in similar_users_indices]
            
            return {"member_id": member_id, "similar_users": similar_users}
        
        else:
            return []

    def compute_recommendations(self, contents, member_ids, target_member_id):
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(contents)
        target_index = member_ids.index(target_member_id)
        target_vector = tfidf_matrix[target_index]
        target_similarities = cosine_similarity(target_vector, tfidf_matrix).flatten()
        return target_index, target_similarities
