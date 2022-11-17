# eat2gether Trouble shooting
#노연수
로그인 구현할때 DB연동을 하면서 pymongo 에러 이슈가 있었습니다. 깃 merge이후, 트러블 슈팅이 발생하였습니다. 알고보니 다른 팀원들은 certifi를 사용하지 않아도 실행이 가능하였는데 제 서버에서만 실행이 되지 않았고 결국 원인은 mongo DB url 뒤에 tlsCAFile=ca를 붙이지 않아서 실행되지 않았다는 사실을 알게 되었습니다. 

# 각지 이름을 적어주시고, 트러블 슈팅 하신 내용을 추가해주세요
