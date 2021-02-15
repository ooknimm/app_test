# app_test

# 과제 1

<br> 

## step 1

+ app.py에 로직들이 담겨 있습니다.
+ pymysql을 사용하여 mysql과 연결하였고 connection.py에 연결객체가 담겨 있습니다.
+ validator.py의 함수들로 유효성 검사를 하였습니다.

<br>

### dir
+ apptest_v1

### 실행파일 
+ apptest_v1/run.py (포트 번호 5000)

<br>

### API 목록

+ 회원가입
+ 로그인
+ 유저 목록 조회
+ 유저 상세 조회
+ 회원 정보 수정
+ 회원 탈퇴

<br>

### API 문서
링크 : https://documenter.getpostman.com/view/13473885/TWDRszPd

<br>

### 개선이 필요한 점

+ 하나의 파일에 모든 로직이 담겨 있어 굉장히 가독성이 떨어지고 유지보수가 힘들어 보입니다.
+ 유효성 검사로 인해 로직이 길어지고 복잡해졌습니다. 검사 또한 불완전합니다.
+ 확장성을 생각해서 어드민까지 추가해서 로직을 구현한다면 더 좋을 것 같습니다.
+ 함수형 뷰보단 클래스형 뷰가 더 깔끔할 것 같습니다.
+ 유저 목록 조회는 페이지네이션이 구현되면 더 좋을 것 같습니다.


<br>
<br>

## step 2

+ step 1을 개선하였습니다.
+ 레이어드 아키텍처 패턴을 사용하였습니다. view, service, model로 계층을 나누었습니다.
+ utils 안에 있는 error_handler.py와 custom_exeptions.py로 에러 핸들링을 하였습니다.
+ pymysql로 mysql과 연결하였고 connection.py에 연결 객체가 담겨 있습니다.
+ flask-request-validator 라이브러리를 사용하여 유효성 검사를 하였습니다.
+ rules.py에서 flask-request-validator가 사용하는 rules를 커스텀하였습니다.
+ 클래스 기반 뷰를 사용했습니다. view/\__init\__.py에서 url을 지정하였습니다.
+ 어드민을 구현하였습니다. 유저 목록 조회는 어드민만 사용 가능합니다.
+ 목록 조회는 페이지네이션을 구현하였습니다.

<br>

### dir
+ apptest_v2

### 실행파일 
+ apptest_v2/run.py (포트 번호 6000)


<br>

### API 목록

+ 회원가입
  + 유저 회원가입
  + 어드민 회원가입
  
+ 로그인 (유저, 어드민)
+ 유저 목록 조회 (어드민)
+ 유저 상세 조회(유저, 어드민)
+ 유저 정보 수정(유저, 어드민)
+ 유저 탈퇴(유저, 어드민)


<br>


### API 문서
링크 : https://documenter.getpostman.com/view/13473885/TWDRszPi#f18a5e37-15d8-4b3b-947b-a9b1a92fe938


<br>
<br>

# 과제 2

### dir
+ wep-scraping

<br>

## step 1

- nodejs의 puppeteer를 사용하여 자동화
- 첫 화면에서 상단 메뉴(Product, Pricing, Documents, FAQ&Blog, Contact)를 차례대로 클릭해서 해당 화면으로 이동
- 이동이 완료되면, Contact 화면에서, "Get In Touch With Us" 부분의 각 항목에 임의의 값을 입력한 후 "SEND" 버튼을 클릭

### 실행 파일 

+ wep-scraping/wepScraper_v1.js

<br>
<br>

## step 2
- nodejs의 puppeteer를 사용하여 자동화
- https://apptest.ai 사이트의 첫 화면에서 Click 가능한 모든 요소(element)를 추출한다.
- 추출된 각 요소에 대한 정보를 JSON 파일의 형태로 저장한다.
- JSON 파일을 읽어서, JSON 파일에 있는 element들을 순서대로 Click한다.
- 각 element들이 클릭될 때마다, 클릭된 결과 화면에 대하여 스크린샷 이미지를 저장한다.

### 실행 파일 

+ wep-scraping/wepScraper_v2.js

### 기타 파일 및 디렉토리


+ 클릭된 결과 화면 스크린샷 저장소 : wep-scraping/screenshots/

+ 클릭 가능한 요소 추출 파일 : wep-scraping/scrapingJson.json
