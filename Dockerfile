# 도커 허브에서 이미지를 가져와서 이미지를 작업한다
FROM python:3.11.7

# 타임존 설정 (설정을 하지 않으면 시간 저장시 다른 시간대로 저장됨)
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezone

# 컨테이너 내 작업 경로
# WORKDIR (경로)
WORKDIR /app

# 파일 복사
COPY . .

# 파이썬 라이브러리 설치
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 서버 실행
CMD python main.py