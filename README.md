# Pokedex 포켓몬 도감

![포켓몬 도감](pokedex.jpeg)

포켓몬 도감입니다. 사용한 주요 기술은 다음과 같습니다.

- 언어 : Python(3.5+), node(6.0+)
- 백엔드 : [Flask](http://flask.pocoo.org/docs/0.11) + [requests](http://docs.python-requests.org/en/master/)
- 프론트엔드 : ES6 + [Stylus](http://stylus-lang.com/) + [babel](https://babeljs.io/) + [Webpack](https://webpack.github.io/) + [milligram](https://milligram.github.io/) + [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- 디비 : 빠른 개발을 위한 SQLite3

영어 포켓몬 데이터는 [공식 포켓몬 도감](http://www.pokemon.com/us/pokedex/), 국가별 포켓몬 이름은 [포켓몬 위키](http://ko.pokemon.wikia.com/wiki/%EA%B5%AD%EA%B0%80%EB%B3%84_%ED%8F%AC%EC%BC%93%EB%AA%AC_%EC%9D%B4%EB%A6%84_%EB%AA%A9%EB%A1%9D)에서 가져왔습니다.

## 실행

```bash
# 파이썬 가상 환경 진입
pip install -r requirements.txt # 파이썬 종속성 설치
npm install # npm 종속성 설치
npm run build # 스태틱 에셋 빌드
python run.py # localhost:5000 에서 서버 시작
```

## 피쳐 요약

- 영어 지원 - 후에 언어별로 확장 가능하게 설계
- 번호나 이름으로 포켓몬 검색
- 처음 검색하는 포켓몬일시 크롤링 후 DB에 저장
- 이미 검색해본 포켓몬일시 DB에 있는 정보 사용
- 검색 과정에서 이름 자동완성 제공
- 진화 사슬 정보 제공
- 모바일/웹에 알맞게 대응하는 반응형 디자인

## 데이터베이스 스키마

다른 언어군 간에 중복되는 정보가 거의 전무하므로 언어 정보만 담고 있는 Locale 테이블과 실제 엔트리가 들어있는 Pokemon 테이블을 분리해 1:n relation으로 관리했습니다. 진화 정보는 의미 상으로는 Pokemon 테이블의 자기 자신과의 relation으로 짜는게 맞겠지만, ForeingKey를 갖지 않는 Evolution 테이블로 따로 뺐습니다. 처음 검색한 포켓몬에 대해 크롤링을 해 왔을 때 (추가적인 크롤링 없이) 그 페이지 안에 있는 정보만 가지고 진화 정보를 제공하기 위해 이렇게 구현했습니다. 나중에 한 페이지를 크롤링 해 올 때 진화 사슬 전체의 정보를 다 가져오게 변경할 경우 개선 가능한 부분입니다.

### Pokemon

- 포켓몬 번호 PK
- 이미지 URL
- 성별
- 타입
- 키
- 몸무게

### PokemonLocale

- 포켓몬 번호 PK
- 로케일 PK
- 포켓몬 이름
- 설명
- 분류
- Pokemon 아이디 FK


### Evolution

- ID PK
- 진화 전 포켓몬 번호
- 진화 후 포켓몬 번호


## 다국어 지원

시간 관계상 서비스의 영어 버전만을 구현했지만, 이후 다국어 지원을 고려한 지점이 몇 있습니다.

- 데이터베이스 스키마에서 language-agnostic한 Pokemon, Evolution 과 language-dependent한 PokemonLocale 구분
- 크롤링 해온 데이터 언어별(소스의 구조별)로 다르게 파싱해야 할 때 언어별 함수를 손쉽게 등록 가능하도록 설계

실제로 다국어 환경을 지원하기 위해선 다음과 같은 조치들이 필요할 것입니다.

- 서비스 최초 접속시 사용자에게 언어 설정을 물은 뒤 결과를 flask session에 저장.
- 현재는 LocaleType.EN 으로 하드코딩 되어 있는 언어 정보를 모두 세션에 있는 정보에 기반하여 사용
- templates 폴더 밑에 지원 언어별 서브디렉토리 및 템플릿 생성, render_template 에서 적절한 템플릿 렌더
- Pokemon 모델 내의 필드들의 각 언어별 매핑 (예를 들어, 타입에서의 Bug -> 벌레(한국어), Bug (영어) 등) 설정


## 가능한 개선 방안

### 모던 프론트엔드 라이브러리 도입

처음 프로젝트를 시작할 때, 상대적으로 간단한 프로젝트라 생각하여 굳이 SPA로 만들 필요가 없다고 생각했습니다. 실제로 꽤 간단하긴 했지만 막바지에 나름대로 구조가 복잡해지고 자동 완성 기능을 바닐라 JS로 구현하면서 애초에 리액트, 리덕스 정도를 사용해 SPA로 구현하는게 더 깔끔하고 (초기 보일러플레이트를 감안해도) 간단하게 구현할 수 있었을 수 있겠다고 느꼈습니다.

### 브라우저 서포트

시간 제한이 있는 프로젝트에서 짧은 시간 내에 괜찮은 룩앤필을 얻기 위해 milligram 이라는 Flexbox 에 기반한 프론트엔드 프레임워크를 사용했습니다. 그 외에 일부 직접 Flexbox를 사용한 부분도 있습니다. (fetch의 경우 깃헙의 폴리필을 사용했습니다) 때문에 IE 지원이 부실합니다. 만약 낡은 버전의 익스플로러 지원들이 꼭 필요한 서비스일 경우 해당 부분들을 Flexbox 대신 다른 기술을 이용해 구현해야 할 것입니다.

### 검색 실패 결과 개선

주요 기능 개발에 집중하느라 상대적으로 사용자 경험 고려가 부실한 상태입니다. 특히 정확히 매치되는 검색어가 아니면 유저는 무조건 에러창을 보게 되는데, 실제 서비스라 생각하면 이 부분이 많이 아쉽습니다. 현재 존재하는 검색어 추천 기능 이외에도 잘못된 검색어로 검색 했을 때 유저가 찾고자 했을 수 있는(검색어와 비슷한) 포켓몬을 몇 마리 보여주는 등의 디테일이 추가되면 좋을 것 같습니다.

