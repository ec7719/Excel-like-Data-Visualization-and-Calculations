import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to read different file types
def read_file(file):
    file_extension = file.name.split(".")[-1]
    if file_extension == "csv":
        data = pd.read_csv(file)
    elif file_extension == "xlsx":
        data = pd.read_excel(file, engine="openpyxl")
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return data

# Function to display the uploaded data
def display_data(data):
    st.write("### Data Preview")
    st.dataframe(data.head())

# Function to perform mathematical calculations and store results as separate columns
def perform_calculations(data):
    st.write("### Calculations")

    # Get column names
    columns = data.columns

    # Iterate over each column and perform calculations
    for column in columns:
        st.write("Calculations for column:", column)

        # Example calculations: sum, mean, median
        column_sum = data[column].sum()
        column_mean = data[column].mean()
        column_median = data[column].median()

        # Create new column names
        sum_column_name = f"{column}_sum"
        mean_column_name = f"{column}_mean"
        median_column_name = f"{column}_median"

        # Add the calculated values as new columns
        data[sum_column_name] = column_sum
        data[mean_column_name] = column_mean
        data[median_column_name] = column_median

        # Display the calculated values
        st.write("Sum:", column_sum)
        st.write("Mean:", column_mean)
        st.write("Median:", column_median)

    # Display the updated data with calculated columns
    st.write("### Updated Data")
    st.dataframe(data)

# Function to plot the graph
def plot_graph(data, graph_type, x_variables, y_variables):
    plt.figure(figsize=(8, 6))

    for x_var in x_variables:
        for y_var in y_variables:
            if graph_type == "Scatter":
                plt.scatter(data[x_var], data[y_var], label=f"{x_var} vs {y_var}")
            elif graph_type == "Line":
                plt.plot(data[x_var], data[y_var], label=f"{x_var} vs {y_var}")
            elif graph_type == "Bar":
                x = range(len(data))
                plt.bar(x, data[y_var], label=y_var)

    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    plt.title(f"{graph_type} Plot")
    plt.legend()

    st.pyplot()

# Streamlit web app
def main():
    st.title("Excel-like Data Visualization and Calculations")
    st.write("Upload a CSV or Excel file and visualize the data")

    file = st.file_uploader("Upload file", type=["csv", "xlsx"])

    if file is not None:
        data = read_file(file)
        if data is not None:
            display_data(data)
            perform_calculations(data)

            st.write("### Graph Visualizer")
            st.write("Select variables for visualization:")

            graph_type = st.selectbox("Graph Type", options=["Scatter", "Line", "Bar"])
            x_variables = st.multiselect("X Variables", options=data.columns)
            y_variables = st.multiselect("Y Variables", options=data.columns)

            if st.button("Plot"):
                plot_graph(data, graph_type, x_variables, y_variables)

if __name__ == "__main__":
    main()
