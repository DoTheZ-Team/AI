from models import mongodb
from datetime import datetime
from Hashtag import Hashtag
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
            
class Controller:

    async def test(self):
        return "test 성공"
    
    # 해시태그 추가
    async def update_hashtag(self, member_id, content):
        member_id = int(member_id)
        # 디비에서 유저가 작성한 해시태그가 있는지 조회
        hashtag = await mongodb.engine.find_one(Hashtag, Hashtag.member_id == member_id)
        
        # 해시태그 존재시 업데이트 진행
        if hashtag:
            hashtag.content = hashtag.content + ' ' + content
            hashtag.updated_at = datetime.now()
            await mongodb.engine.save(hashtag)
            print(f"{hashtag.content} 해시태그가 생성되었습니다.")
            
        # 해시태그 미존재시 생성 진행
        else:
            hashtag = Hashtag(member_id=member_id, content=content)
            await mongodb.engine.save(hashtag)
            print(f"{content} 해시태그가 생성되었습니다.")
            
        return hashtag
    
    
    
    async def recommend_user(self, member_id:int):
        hashtag = await mongodb.engine.find_one(Hashtag, Hashtag.member_id == member_id)
        
        if hashtag:
            # 해시태그 다가져옴
            all_hashtags = await mongodb.engine.find(Hashtag)

            # 사용자들의 해시태그와 아이디 리스트로 저장
            contents = [hashtag.content for hashtag in all_hashtags]
            member_ids = [hashtag.member_id for hashtag in all_hashtags]
            
            user_index, similarities = self.compute_recommendations(contents, member_ids, member_id)
            
            # 당자자의 인덱스를 제외한 가장 유사한 30명의 인덱스를 가져옴
            similar_users_indices = similarities.argsort()[-(30 + 1):-1][::-1]
            similar_users = [member_ids[i] for i in similar_users_indices]
            
            return {"member_id": member_id, "similar_users": similar_users}
        
        else:
            return [] # 작성 해시태그 없을 시 빈 리스트 반환 추후 변경 필요(인기 유저 또는 랜덤 유저 추천)


    # 추천 알고리즘 부분! TF-IDF를 사용하여 단어의 중요도를 계산하고
    # 이후로 코사인 유사도를 사용하여 유사도를 계산하는 알고리즘임
    def compute_recommendations(self, contents, member_ids, target_member_id):
        
        # 이부분이 TF-IDF를 사용하여 단어의 중요도를 계산하는 부분
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(contents)

        # 이건 타겟 유저의 TF-IDF 벡터를 가져오는 부분
        # -> 이후로 cosine 유사도를 계산할 때 타깃으로 사용하기 위함
        target_index = member_ids.index(target_member_id)
        target_vector = tfidf_matrix[target_index]

        # 이제 진짜 사용자의 TF-IDF 벡터를 통해 다른 사용자들과의 코사인 유사도를 구함
        target_similarities = cosine_similarity(target_vector, tfidf_matrix).flatten()

        # 사용자의 유사도를 기반으로 가장 유사한 사용자를 찾아내고 그 결과를 리턴
        return target_index, target_similarities