from fastapi import HTTPException

class ErrorHandler:
    @staticmethod
    def raise_not_found_error(detail="블로그 아이디를 찾을 수 없습니다."):
        raise HTTPException(status_code=404, detail=detail)

    @staticmethod
    def raise_bad_request_error(detail="잘못된 요청입니다."):
        raise HTTPException(status_code=400, detail=detail)

    @staticmethod
    def raise_internal_server_error(detail="서버 내부 오류가 발생했습니다."):
        raise HTTPException(status_code=500, detail=detail)

    @staticmethod
    def handle_transport_error(error):
        print(f"전송 오류: {str(error)}")
        return None

    @staticmethod
    def handle_generic_error(error):
        print(f"예상치 못한 오류가 발생했습니다: {str(error)}")
        return None

    @staticmethod
    def handle_requests_http_error(error, detail="서버에서 설정을 가져오는데 실패했습니다."):
        print(f"HTTP 오류가 발생했습니다: {str(error)}")
        raise HTTPException(status_code=400, detail=detail)

    @staticmethod
    def handle_requests_exception(error, detail="설정을 가져오는 동안 오류가 발생했습니다."):
        print(f"요청 오류가 발생했습니다: {str(error)}")
        raise HTTPException(status_code=500, detail=detail)

    @staticmethod
    def handle_unexpected_error(error, detail="설정을 가져오는 동안 예상치 못한 오류가 발생했습니다."):
        print(f"예상치 못한 오류가 발생했습니다: {str(error)}")
        raise HTTPException(status_code=500, detail=detail)
    
    @staticmethod
    def handle_key_error(error, detail="잘못된 설정 데이터입니다."):
        print(f"키 오류가 발생했습니다: {str(error)}")
        raise HTTPException(status_code=400, detail=detail)