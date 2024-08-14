import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.title("Data Processing with Streamlit")

# Đọc dữ liệu từ file data.csv
data_csv = pd.read_csv('data.csv')
st.write("Data loaded successfully. Here is the complete dataset:")
st.dataframe(data_csv, width=800)  # Tăng chiều cao của bảng hiển thị

# Chuyển đổi các cột có thể thành số
for col in data_csv.columns:
    data_csv[col] = pd.to_numeric(data_csv[col], errors='ignore')

st.write("Data after converting columns to numeric where possible:")
st.write(data_csv.dtypes)

# Kiểm tra giá trị thiếu trước khi điền
missing_values = data_csv.isnull().sum()
st.write("Missing values before filling:")
st.write(missing_values)

# Điền giá trị thiếu bằng giá trị trung bình cho các cột số
for col in data_csv.select_dtypes(include=['float64', 'int64']).columns:
    data_csv[col].fillna(data_csv[col].mean(), inplace=True)

missing_values_after_filling = data_csv.isnull().sum()
st.write("Missing values after filling numeric columns with mean:")
st.write(missing_values_after_filling)

# Kiểm tra và xử lý ngoại lai cho các cột số
for col in data_csv.select_dtypes(include=['float64', 'int64']).columns:
    Q1 = data_csv[col].quantile(0.25)
    Q3 = data_csv[col].quantile(0.75)
    IQR = Q3 - Q1
    data_csv = data_csv[~((data_csv[col] < (Q1 - 1.5 * IQR)) | (data_csv[col] > (Q3 + 1.5 * IQR)))]

st.write("Data after removing outliers:")
st.write(data_csv.describe())

# Chuyển đổi dữ liệu về định dạng phù hợp (nếu cần thiết)
for col in data_csv.select_dtypes(include=['object']).columns:
    if data_csv[col].str.isnumeric().all():
        data_csv[col] = data_csv[col].astype(int)

st.write("Data after converting applicable object columns to int:")
st.write(data_csv.dtypes)

# Tính toán thống kê cơ bản
st.write("Basic statistics:")
st.write(data_csv.describe())

# Chuyển đổi cột 'Stars' thành số (nếu cần thiết)
if 'Stars' in data_csv.columns:
    data_csv['Stars'] = pd.to_numeric(data_csv['Stars'], errors='coerce')

# Lưu kết quả phân tích
buffer = io.StringIO()
data_csv.to_csv(buffer, index=False)
csv_data = buffer.getvalue()

st.download_button(
    label="Download Data as CSV",
    data=csv_data,
    file_name='analysis_results.csv',
    mime='text/csv'
)

# Vẽ các loại biểu đồ cho cột Stars
if 'Stars' in data_csv.columns:
    st.write("Histogram of Stars:")
    fig = px.histogram(data_csv, x='Stars', title='Histogram of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Boxplot of Stars:")
    fig = px.box(data_csv, y='Stars', title='Boxplot of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Bar plot of Stars:")
    stars_count = data_csv['Stars'].value_counts().reset_index()
    stars_count.columns = ['Stars', 'count']
    fig = px.bar(stars_count, x='Stars', y='count', title='Bar plot of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Line plot of Stars:")
    fig = px.line(data_csv, y='Stars', title='Line plot of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    # Tính toán số lượng giá trị trong từng hạng mục 'Stars'
    stars_count = data_csv['Stars'].value_counts().reset_index()
    stars_count.columns = ['Stars', 'count']

# Định nghĩa ngưỡng giá trị nhỏ
    threshold = 5  # Bạn có thể điều chỉnh ngưỡng này

# Nhóm các giá trị nhỏ hơn ngưỡng thành 'Others'
    stars_count['Stars'] = stars_count['Stars'].apply(lambda x: x if stars_count[stars_count['Stars'] == x]['count'].values[0] >= threshold else 'Others')

# Gộp nhóm 'Others'
    stars_count = stars_count.groupby('Stars').sum().reset_index()
    st.write("Pie chart of Stars:")
    fig = px.pie(stars_count, names='Stars', values='count', title='Pie chart of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Heatmap of Stars (correlation with other columns):")
    numeric_cols = data_csv.select_dtypes(include=['float64', 'int64'])
    if not numeric_cols.empty:
        fig = px.imshow(numeric_cols.corr(), text_auto=True, title='Heatmap of Stars', width=1000, height=600)
        st.plotly_chart(fig)
    else:
        st.write("No numeric columns to display heatmap.")

    st.write("Violin plot of Stars:")
    fig = px.violin(data_csv, y='Stars', title='Violin plot of Stars', width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Scatter plot of Stars:")
    fig = px.scatter(data_csv, x=data_csv.index, y='Stars', title='Scatter plot of Stars', labels={'index': 'Index'}, width=1000, height=600)
    st.plotly_chart(fig)

    st.write("Pair plot of Stars with other numeric columns:")
    if len(numeric_cols.columns) > 1:
        fig = px.scatter_matrix(data_csv, dimensions=numeric_cols.columns.tolist(), title='Pair plot of Stars', width=1000, height=600)
        st.plotly_chart(fig)
else:
    st.write("Column 'Stars' not found in the dataset.")
