# 전남광주 수학과외

광주·전남 지역 1:1 맞춤 과외 웹사이트입니다.

## 로컬 확인

`index.html`을 브라우저에서 열면 됩니다. 별도 빌드 과정은 없습니다.

## 지역 페이지 수정

27개 지역 페이지(`gwangju-*.html`, `*-si.html`, `*-gun.html`)와 `sitemap.xml`은 `tools/build_region_pages.py`로 생성합니다. 지역 페이지를 직접 고치지 말고, 스크립트의 지역 정보나 문구를 수정한 뒤 다시 생성하세요.

```
python tools/build_region_pages.py
```

## 배포

GitHub Pages 저장소의 루트에 업로드하면 `CNAME` 설정을 통해 `tutorlink.kr` 도메인을 사용할 수 있습니다. 가비아 DNS에는 GitHub Pages용 A 레코드와 `www` CNAME 레코드를 별도로 등록해야 합니다.

## 운영 전 확인

- 상담을 받을 전화번호 또는 카카오톡 채널 연결
- 상담 폼 전송을 처리할 이메일/폼 서비스 연결
- 실제 사업자 정보 및 개인정보처리방침 입력