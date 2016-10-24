# Pokedex 포켓몬 도감

포켓몬 도감을 만듭니다.

- 백엔드 : Flask (Python 3.5+)
- 프론트엔드 : ES6 + Stylus + Webpack
- 디비 : 빠른 개발을 위한 SQLite3

- 데이터 소스 : [영어](http://www.pokemon.com/us/pokedex/), [한국어 및 국가별 포켓몬 이름](http://ko.pokemon.wikia.com/wiki/%EA%B5%AD%EA%B0%80%EB%B3%84_%ED%8F%AC%EC%BC%93%EB%AA%AC_%EC%9D%B4%EB%A6%84_%EB%AA%A9%EB%A1%9D)


## 기능

- 한국어 및 영어 지원
- 번호나 이름으로 포켓몬 검색
- 처음 검색하는 포켓몬일시 크롤링 후 DB에 저장
- 이미 검색해본 포켓몬일시 DB에 있는 정보 불러옴

## 데이터베이스 스키마

다른 언어군 간에 중복되는 정보가 거의 전무하므로 언어 정보만 담고 있는 Locale
테이블과 실제 엔트리가 들어있는 Pokemon 테이블을 분리해 1:n relation으로 관리.

### Locale

- 로케일 PK

### Pokemon

- 포켓몬 번호 PK
- 포켓몬 이름
- 설명
- 타입
- 분류
- 이미지 URL
- 성별
