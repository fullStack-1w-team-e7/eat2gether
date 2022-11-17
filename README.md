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