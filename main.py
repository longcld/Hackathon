from flask import Flask

app = Flask(__name__)

list = ["1", "2", '3']
@app.route("/")
def begin():
    return '''<!DOCTYPE html>
<html>
<body>
<input type='file' />
<img id="myImg" src="#" alt="your image" />

<button type="button" >Detect</button><br>
<br>
<br>

Họ tên:<input type="text" name="name:"><br>
Mã SV:<input type="text" name="Id:"><br>
Ngày sinh:<input type="text" name="birthday:"><br>
Khóa:<input type="text" name=""><br>
</body>
</html>
'''


if __name__ == "__main__":
    app.run()
