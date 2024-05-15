'''
자동 업데이트 방식으로 하려고 처음에 작성했던 코드
이부분 고민중임.
'''

# import schedule
# import time
# from tf_idf_service import TF_IDF, index_creation, prepare_documents, indexing

# # 주기적으로 tf-idf작업 수행하는 함수
# def periodic_job():
#     # Run TF_IDF and related functions
#     tfidf_matrix, data = TF_IDF()
#     es_client = index_creation(tfidf_matrix)
#     docs = prepare_documents(tfidf_matrix)
#     indexing(docs, es_client)
#     print("TF-IDF updated at:", time.strftime("%Y-%m-%d %H:%M:%S"))

# # Schedule the periodic job to run every hour (adjust interval as needed)
# schedule.every(6).hour.do(periodic_job)

# # Run the scheduler loop
# while True:
#     schedule.run_pending()
#     time.sleep(1)