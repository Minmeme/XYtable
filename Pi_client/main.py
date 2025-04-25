import csv
from flask import Flask, render_template, Response
from multiprocessing import Process

app = Flask(__name__)


@app.route('/')
def index():
    # อ่านข้อมูลจากไฟล์ color_totals.csv
    csv_file = '/home/meme/Documents/cata/camtest/csv/color_totals.csv'
    last_row = None
    while True:
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = list(csv.reader(file))
                if len(reader) > 1:
                    last_row = reader[-1]  # แถวล่าสุด (ID, Timestamp, Yellow, Blue, Pink, White)
        except FileNotFoundError:
            last_row = None

        return render_template('index.html', totals=last_row)


if __name__ == "__main__":
    app.run(host='10.10.199.124', port=5050, threaded=True, debug=False)
