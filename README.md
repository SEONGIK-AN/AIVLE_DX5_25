## 빅데이터 분석을 통한 해양생태 예측 관리 플랫폼, IM OCEAN
|주관|소속|프로젝트 기간|
|:---:|:---:|:---:|
|[KT 에이블스쿨](https://aivle.kt.co.kr/home/main/indexMain)|KT 에이블스쿨 5기 대구/경북 8반 25조|2024-06-17~2024-07-29|

### 프로젝트 요약(가상 사업)
![사업요약](./src/img/사업요약.png)

### 서비스 시나리오
![서비스 시나리오](./src/img/서비스시나리오.png)

### 사용 데이터 및 출처
- 본 저작물은 기상청 기후정보포털에서 공공누리 제1유형으로 개방한 국가 기후변화 표준 시나리오를 이용하였으며, 해당 저작물은 [기상청 기후정보포털](http://www.climate.go.kr/home/bbs/view.php?code=11&bname=notice&vcode=6925&cpage=1&vNum=Notice&skind=&sword=&category1=&category2=)을 참고하여 API 신청을 통해 무료로 이용할 수 있습니다.

#### 국내 해양 생태구 해역 구분(출처: [국가법령정보센터](https://www.law.go.kr/flDownload.do?flSeq=14495017&flNm=%5B%EB%B3%84%ED%91%9C%5D+%EC%83%9D%ED%83%9C%EA%B5%AC%EB%B3%84+%ED%95%B4%EC%97%AD+%EA%B5%AC%EB%B6%84%ED%91%9C))
![생태구 구분](./src/img/해역.png)

#### 수질/수온 예측 데이터
> [**기상청 기후정보포털**](http://www.climate.go.kr/home/bbs/view.php?code=11&bname=notice&vcode=6925&cpage=1&vNum=Notice&skind=&sword=&category1=&category2=)
> 1. AR6_SSP585_ENSMN_korea_SALNT_gridraw_monthly_2021_2040.nc(표층염도 예측 데이터 2021~2040)
> 2. AR6_SSP585_ENSMN_korea_SALNT_gridraw_monthly_2041_2060.nc(표층염도 예측 데이터 2041~2060)
> 3. AR6_SSP585_ENSMN_korea_SST_gridraw_monthly_2021_2040.nc(표층수온 예측 데이터 2021~2040)
> 4. AR6_SSP585_ENSMN_korea_SST_gridraw_monthly_2041_2060.nc(표층수온 예측 데이터 2041~2060)
#### 어업 관련 데이터
> **[광주과학기술원](https://www.bigdata-sea.kr/)**
> 1. 어업별 어구부이
> 2. 어업별 어선조업
> 3. 어업별 어획량
> 4. 어업별 조업 정보
> ### 사용 라이브러리
1. `pandas==2.2.2`
2. `scikit-learn=1.4.2`
3. `folium==0.14.0`
4. `streamlit==1.36.0`
5. `streamlit-extras==0.4.0`
6. `streamlit_folium==0.21.0`
7. `altair==5.0.1`