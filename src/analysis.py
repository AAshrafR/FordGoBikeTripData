import os
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns



from data_loading import load_data
from feature_engineering import add_features
from preprocessing import clean_data
from configration import FIGURES_PATH




def user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a count plot showing the distribution of user types in the

    dataset and displays the plot directly with an option to save it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the 'user_type'
          column.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5), dpi=200)

    sns.countplot(data=df, x="user_type")

    plt.xlabel("User distribution")
    plt.ylabel("Frequency")
    plt.title("Represent the user's distribution depending on user type")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()



def bike_share(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a count plot showing the distribution of bike share users across all trips,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the
          'bike_share_for_all_trip' column.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5), dpi=200)

    sns.countplot(data=df, x="bike_share_for_all_trip")

    plt.xlabel("User distribution")
    plt.ylabel("Frequency")
    plt.title("Represent the user's distribution depending on being a part of the Trips Program")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()



def user_age(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a histogram plot showing the distribution of users' ages,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the 'member_age'
          column.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5), dpi=200)

    plt.hist(df["member_age"], edgecolor="black")

    plt.xlabel("User distribution")
    plt.ylabel("Frequency")
    plt.title("Represent the user's distribution depending on their age")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()



def age_outliers(df: pd.DataFrame, save_path: Optional[str] = None) -> pd.DataFrame:
    """Detects and treats outliers in the 'member_age' column using the IQR

    clipping method, plots the boxplots before and after treatment, and returns
    the updated DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the 'member_age'
          column.
        save_path (Optional[str]): Optional file path to save the second plot
          (treated boxplot).

    Returns:
        pd.DataFrame: The DataFrame with 'member_age' outliers clipped within IQR
        fences.
    """
    # 1. Plot initial boxplot before treatment
    plt.figure(figsize=(8, 2))
    sns.boxplot(df["member_age"], orient="h")
    plt.title("Member Age Boxplot")
    plt.show()

    # 2. Outlier treatment using IQR clipping
    df["member_age"] = df["member_age"].astype("float64")
    Q1 = df["member_age"].quantile(0.25)
    Q3 = df["member_age"].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR

    df["member_age"] = df["member_age"].clip(
        lower=lower_fence, upper=upper_fence
    )

    # 3. Display summary statistics after treatment
    print(df["member_age"].describe())

    # 4. Plot boxplot after outlier treatment
    plt.figure(figsize=(8, 2))
    sns.boxplot(x=df["member_age"])
    plt.title("Users' Age After Outlier Treatment")
    plt.xlabel("Age")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()

    return df



def trip_duration_min(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a Kernel Density Estimate (KDE) plot showing the distribution

    of trip duration in minutes, displays the plot directly, and optionally
    saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the
          'trip_duration_min' column.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(20, 10))

    sns.kdeplot(df["trip_duration_min"])

    plt.title("trip duration in min kde plot")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()



def member_gender(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a donut chart showing the distribution of member genders using

    Plotly Express, displays the figure directly, and optionally saves it.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the 'member_gender'
          column.
        save_path (Optional[str]): Optional file path to save the generated plot
          (e.g., 'plot.html' or 'plot.png').

    Returns:
        None
    """
    fig = px.pie(
        df,
        names="member_gender",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4,
    )

    fig.update_layout(
        annotations=[
            dict(text="Gender", font_size=20, x=0.5, y=0.5, showarrow=False)
        ]
    )

    if save_path:
        if save_path.endswith(".html"):
            fig.write_html(save_path)
        else:
            fig.write_image(save_path)

    fig.show()




def trip_duration_hour(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a Kernel Density Estimate (KDE) plot showing the distribution

    of trip duration in hours, displays the plot directly, and optionally saves
    it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the
          'trip_duration_hour' column.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(20, 10))

    sns.kdeplot(df["trip_duration_hour"])

    plt.title("trip duration in hours kde plot")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()



def avg_duration_user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a bar plot showing the average trip duration in seconds

    for each user type category, displays the plot directly, and optionally saves
    it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'user_type' and
          'duration_sec' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    sns.barplot(data=df, x="user_type", y="duration_sec")

    plt.title("Duration distribution by User Type")
    plt.xlabel("User Type")
    plt.ylabel("Duration in sec")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def duration_by_gender(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a violin plot showing the distribution of trip duration in minutes

    across different member genders, displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'member_gender' and
          'trip_duration_min' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    sns.violinplot(data=df, x="member_gender", y="trip_duration_min")

    plt.title("Duration Distribution by Member Gender")
    plt.xlabel("Member Gender")
    plt.ylabel("Trip Duration (minutes)")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def duration_by_user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a bar plot showing the average trip duration in minutes for each user type,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'user_type' and
          'trip_duration_min' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    sns.barplot(data=df, x="user_type", y="trip_duration_min")

    plt.title("Trip Duration in Minutes by User Type")
    plt.xlabel("User Type")
    plt.ylabel("trip_duration_min")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def age_by_user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a box plot showing the age distribution across different user types,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'user_type' and
          'member_age' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    sns.boxplot(data=df, x="user_type", y="member_age")

    plt.title("Distribution of Age by User Type")
    plt.xlabel("User Type")
    plt.ylabel("Age")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def age_by_member_gender(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a dodged histogram showing the user age distribution grouped by member gender,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'member_age' and
          'member_gender' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(12, 6))

    sns.histplot(
        data=df,
        x="member_age",
        hue="member_gender",
        bins=20,
        multiple="dodge",
    )

    plt.title("User Distribution by Age and Member Gender")
    plt.xlabel("Age")
    plt.ylabel("Number of Users")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()





def duration_by_age_user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a scatter plot showing the relationship between age, trip duration in minutes,

    and user type with transparency, displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'member_age',
          'trip_duration_min', and 'user_type' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(12, 6))

    sns.scatterplot(
        data=df,
        x="member_age",
        y="trip_duration_min",
        hue="user_type",
        alpha=0.5,
    )

    plt.title("Trip Duration by Age and User Type")
    plt.xlabel("Age")
    plt.ylabel("Trip Duration (minutes)")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def duration_by_user_type_and_gender(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a grouped bar plot comparing average trip duration in minutes across

    user types and member genders, displays the plot directly, and optionally saves
    it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'user_type',
          'trip_duration_min', and 'member_gender' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=df,
        x="user_type",
        y="trip_duration_min",
        hue="member_gender",
        estimator="mean",
    )

    plt.title("Average Trip Duration by User Type and Gender")
    plt.xlabel("User Type")
    plt.ylabel("Average Trip Duration (minutes)")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def variable_correlation(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a pairplot matrix for numerical variables using a random sample

    for optimal visualization performance, displays the plot directly, and
    optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing numerical features.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    # Select numerical variables for correlation analysis
    num_cols = df.select_dtypes(include="number").columns

    # Take a sample for faster visualization
    sample_df = df.sample(3000, random_state=42)

    # Explore relationships between numerical variables
    pair_grid = sns.pairplot(sample_df, vars=num_cols, height=2)

    if save_path:
        pair_grid.savefig(save_path, bbox_inches="tight")

    plt.show()





def specific_numeric_correlation(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a annotated heatmap showing the correlation matrix for specific

    numeric columns, displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the specified numeric columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    specific_numeric_cols = [
        "member_age",
        "trip_duration_min",
        "start_station_latitude",
        "start_station_longitude",
        "end_station_latitude",
        "end_station_longitude",
    ]

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        df[specific_numeric_cols].corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
    )

    plt.title("Correlation Between Specific Numerical Variables")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()






def data_stat_correlation(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a heatmap correlation matrix for key numerical variables

    (duration_sec, member_birth_year, member_age, bike_id), displays the plot
    directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the target columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    cols_for_corr = [
        "duration_sec",
        "member_birth_year",
        "member_age",
        "bike_id",
    ]

    # Safely convert column types without altering the original DataFrame
    corr_df = df[cols_for_corr].copy()
    corr_df["bike_id"] = corr_df["bike_id"].astype(float)
    corr_matrix = corr_df.corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".3f",
        cmap="vlag",
        vmin=-1,
        vmax=1,
        linewidths=1,
        square=True,
        cbar_kws={"shrink": 0.8},
    )

    plt.title(
        "Correlation Matrix of Key Numeric Variables", fontsize=16, pad=20
    )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()




def pairplot_by_user_type(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a pairplot of key numerical variables grouped by user type,

    displays the plot directly, and optionally saves it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'duration_sec',
          'member_age', 'start_time_sec', and 'user_type' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    num_cols = [
        "duration_sec",
        "member_age",
        "start_station_latitude",
        "start_station_longitude",
        "start_time_sec",
    ]

    df_multivariate = df[
        num_cols + ["user_type", "member_gender"]
    ].dropna()

    pair_grid = sns.pairplot(
        data=df_multivariate,
        vars=["duration_sec", "member_age", "start_time_sec"],
        hue="user_type",
        palette="tab10",
        diag_kind="kde",
        plot_kws={"alpha": 0.4, "s": 25},
    )

    plt.suptitle(
        "Pairplot of Key Numerical Variables Grouped by User Type",
        y=1.02,
        fontsize=14,
    )

    if save_path:
        pair_grid.savefig(save_path, bbox_inches="tight")

    plt.show()






def age_vs_duration_by_user_and_gender(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Generates a FacetGrid scatter plot comparing member age and trip duration

    across user types and genders, displays the plot directly, and optionally saves
    it to a file.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'member_age',
          'duration_sec', 'user_type', and 'member_gender' columns.
        save_path (Optional[str]): Optional file path to save the generated
          plot.

    Returns:
        None
    """
    g = sns.FacetGrid(
        data=df,
        col="user_type",
        hue="member_gender",
        height=5,
        aspect=1.2,
        palette="Dark2",
    )

    g.map(sns.scatterplot, "member_age", "duration_sec", alpha=0.5)
    g.add_legend(title="Gender")
    g.set_axis_labels("Member Age (Years)", "Duration (Seconds)")
    g.figure.subplots_adjust(top=0.8)
    g.figure.suptitle(
        "Member Age vs Duration Across User Types & Genders", fontsize=14
    )

    if save_path:
        g.savefig(save_path, bbox_inches="tight")

    plt.show()