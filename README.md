# full_reference
필요할 때 사용할 참고용 레포
내가 알고있는 대부분이 다 들어간 레포

# 1. ModelViewSet
- 메서드 별 각기 다른 인증 모듈 적용
- 메서드별 각기 다른 시리얼라이저 적용
- decorator를 활용한 소유자 전용 퍼미션 부여

# 2. Middleware
- HTTP Header에 인증키 (SHA256) 체크하여 API 접속 보안을 강화한 middleware 작성

# 3. Auth
- JWT 커스터마이즈
- Login 방식 커스터마이즈
- 퍼미션 커스터마이즈

# 4. Response
- 에러 응답 유틸화
- 정상 응답 유틸화

# 5. URI
- DefaultRouter 로 ModelViewSet uri 관리 


# 6. Docker & docker-compose
- django 도커라이징

# 7. .env
- python-dotenv 패키지로 환경파일 관리

# 8. swagger
- drf-yasg 패키지로 API 문서화
- api 파라미터 유틸라이즈

## 추후 더 좋은 버전으로 업그레이드 될 예정
