import pandas as pd

# โหลดไฟล์ CSV
df = pd.read_csv('/home/meme/Documents/cata/camtest/csv/color_counts.csv')


# บวกค่าทั้งหมดในแต่ละคอลัมน์
sum_by_color = df[['Yellow', 'Blue', 'Pink', 'White']].sum()

# แสดงผลลัพธ์
print(sum_by_color)

