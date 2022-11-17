# eat2gether Trouble shooting


# 각지 이름을 적어주시고, 트러블 슈팅 하신 내용을 추가해주세요

# 송지수

상세 페이지 기능 구현중 ajax통신이 비동기 방식으로 동작해 
원해는 기능이 구현되지 않았다<br>
검색 중 fetch api와 async, await 키워드를 찾고<br>

    async function add() {
              const response = await fetch('/api/validate', {method: 'GET'});
              const validateToken = await response.json();

              {# 토큰이 존재할 경우 #}
              if(validateToken['result'] === 'success') {

                  const response = await fetch('/api/add/{{ page.post_id }}', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({'give_user': validateToken['id'] })
                  });

                  const result = await response.json();

                  {# 토큰이 존재하고 예약에 성공한 경우 #}
                  if(result['result'] === 'success') {
                      alert(result['msg']);

                  {# 토큰은 존재하지만 정원초과인 경우우 #}
                 } else {
                      alert(result['msg']);
                  }

              {# 토큰이 없는경우(유효기간 만료 or 로그인X) #}
              } else {
                  alert(validateToken['msg']);
              }

              window.location.reload();
        }

문제를 해결 할 수 있었다 


# 강동규(7조 Node)
### 오타 에러
* 코드 작성 후 파일을 실행해 보면 나는 경우의 80프로 이상이 괄호 등을 빼먹거나 철자를 잘못 입력해서 생겨나는 오류들이었다. 오타라면 진절머리가 날 정도였다. 나만 이렇게 오타의 늪에서 헤어나오지 못하는 건지 의구심이 들었다. 예를 들면 -로 작성해야 할 것을 _으로 작성하거나 주석처리를 잘못하여 이상한 # 기호가 굴러다니거나 하는 식이다. 하지만 이를  찾는 것은 너무나 짜증나고 오랜 시간이 걸리는 일이다. 
#### 해결 방법을 고민하다
* 계속 오타의 늪에서 허우적대고 싶지 않았다. 그래서 어떻게든 대책을 세워야 했다. 나의 해결 방법은 다음과 같다.
     - 작업 단위를 쪼개서 그때그때 실행하여 에러가 발생하지 않는지 확인한다.
        - 코드를 타이핑한 양이 많아질 수록 그 안에서 발생한 오류를 찾아내기 어렵다. 그래서 나는 작업양이 많아지기 전에 코드를 실행하여 이상이 없으면 다음 작업을 하는 방법을 쓰게 되었다. 
     - 기본 구조는 직접 타이핑 한다
        - 이게 무슨 해결방법이냐고 하실 수도 있다. 하지만 역설적으로 자주 직접 코드를 외워서 써 보는 것이 오타 에러를 줄이는 가장 좋은 방법 중의 하나가 된다. 코드를 복붙하지 않고 직접 손으로 적거나 타이핑 하면 그 과정에서 코드의 구조를 머릿 속에 더 잘 새겨넣게 된다. 그래서 나중에 오류가 생겼을 때 잘못된 부분이 어디인지 찾아내는 눈이 생겨난다. 
        
        
#노연수
### 로그인 구현할때 DB연동을 하면서 pymongo 에러 이슈가 있었습니다. 깃 merge이후, 트러블 슈팅이 발생하였습니다. 알고보니 다른 팀원들은 certifi를 사용하지 않아도 실행이 가능하였는데 제 서버에서만 실행이 되지 않았고 결국 원인은 mongo DB url 뒤에 tlsCAFile=ca를 붙이지 않아서 실행되지 않았다는 사실을 알게 되었습니다. 


#최예나(팀장)
### 지난 4일간의 기록을 블로그에 남겼다.
### 블로그에는 없지만, 깃을 사용해 푸쉬, 풀, 풀 리퀘스트, 머지 등... 많은 에러를 만났다. 대부분의 개발 시간에는 깃을 통해 파일을 머지하고, 머지 컨플릭트를 해결하는 데에 사용했다.
https://dev-jn.tistory.com/85
https://dev-jn.tistory.com/86
https://dev-jn.tistory.com/87
https://dev-jn.tistory.com/88
