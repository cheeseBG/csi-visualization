from moviepy.editor import *
# 파일명을 넣어서 쉽게 읽어들일 수 있다.
# speedx 등의 함수를 이용해 속도나 화면 로테이션 등을 쉽게 할 수 있다.
clip = (VideoFileClip("../asset/sample.mp4").speedx(2))

# write_gif 함수를 이용해 바로 gif로 만들 수 있다.
clip.write_gif("sample.gif")