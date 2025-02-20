from datetime import datetime
import numpy as np
from shiny.express import ui, input, render
import pandas as pd
from pathlib import Path
from faicons import icon_svg
import plotly.express as px
from shinywidgets import render_plotly
from shiny import reactive
from state_choices import STATE_CHOICES

new_listings_df = pd.read_csv(
    Path(__file__).parent / "Metro_new_listings_uc_sfrcondo_month.csv"
)
median_listing_price_df = pd.read_csv(
    Path(__file__).parent / "Metro_mlp_uc_sfrcondo_sm_month.csv"
)
for_sale_inventory_df = pd.read_csv(
    Path(__file__).parent / "Metro_invt_fs_uc_sfrcondo_sm_month.csv"
)


def string_to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def filter_by_date(df: pd.DataFrame, date_range: tuple):
    rng = sorted(date_range)
    # print("Columns in DataFrame:", df.columns)  # Debugging line to check column names
    dates = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.date
    return df[(dates >= rng[0]) & (dates <= rng[1])]


# for_sale_inventory_df2 = for_sale_inventory_df["StateName"].fillna("United States")
# for_sale_inventory_df2 = for_sale_inventory_df["StateName"].drop_duplicates()
# for_sale_inventory_df2 = for_sale_inventory_df2.sort_values().tolist()

ui.page_opts(title="USA housing App")


with ui.sidebar():

    ui.input_select("state", "Filter by state", choices=STATE_CHOICES)
    ui.input_slider(
        "date_range",
        "Fliter by Data Range",
        min=string_to_datetime("2018-3-31"),
        max=string_to_datetime("2024-4-30"),
        value=[string_to_datetime(x) for x in ["2018-3-31", "2024-4-30"]],
    )

with ui.layout_column_wrap():
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "current median list price"

        @render.ui
        def price():
            date_columns = median_listing_price_df.columns[6:]
            states = median_listing_price_df.groupby("StateName").mean(
                numeric_only=True
            )
            dates = states[date_columns].reset_index()
            states = dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )

            country = median_listing_price_df[
                median_listing_price_df["RegionType"] == "country"
            ]
            country_dates = country[date_columns].reset_index()
            country_dates["StateName"] = "United States"
            country = country_dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )
            res = pd.concat([states, country])
            res = res[res["Date"] != "index"]
            df = res[res["StateName"] == input.state()]
            last_value = df.iloc[-1, -1]
            return f"${last_value:,.0f}"

    with ui.value_box(showcase=icon_svg("house")):
        "Home inventory % change"

        @render.ui
        def inventory():
            date_columns = for_sale_inventory_df.columns[6:]
            states = for_sale_inventory_df.groupby("StateName").sum(numeric_only=True)
            dates = states[date_columns].reset_index()
            states = dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )

            country = for_sale_inventory_df[
                for_sale_inventory_df["RegionType"] == "country"
            ]
            country_dates = country[date_columns].reset_index()
            country_dates["StateName"] = "United States"
            country = country_dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )
            res = pd.concat([states, country])
            res = res[res["Date"] != "index"]
            df = res[res["StateName"] == input.state()]
            last_value = df.iloc[-1, -1]
            second_last_value = df.iloc[-2, -1]
            percentage_change = (
                (last_value - second_last_value) / second_last_value
            ) * 100
            sign = "+" if percentage_change >= 0 else "-"
            return f"{sign}{percentage_change:.2f}%"


with ui.navset_card_underline(title="Median list price"):
    with ui.nav_panel("Plot", icon=icon_svg("chart-line")):

        @render_plotly
        def list_price_plot():
            price_grouped = median_listing_price_df.groupby("StateName").mean(
                numeric_only=True
            )
            date_columns = median_listing_price_df.columns[6:]
            price_grouped_dates = price_grouped[date_columns].reset_index()
            price_df_for_viz = price_grouped_dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )

            price_df_for_viz = filter_by_date(price_df_for_viz, input.date_range())

            if input.state() == "United States":
                df = price_df_for_viz[price_df_for_viz["StateName"] != ""]
            else:
                df = price_df_for_viz[price_df_for_viz["StateName"] == input.state()]

            fig = px.line(
                df,
                x="Date",
                y="Value",
                color="StateName",
            )
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
            return fig

    with ui.nav_panel("Table", icon=icon_svg("table")):

        @render.data_frame
        def list_price_data():
            if input.state() == "United States":
                df = median_listing_price_df[median_listing_price_df["StateName"] != ""]
            else:
                df = median_listing_price_df[
                    median_listing_price_df["StateName"] == input.state()
                ]
            return render.DataGrid(df)


with ui.navset_card_underline(title="Sale Plot price"):
    with ui.nav_panel("Plot", icon=icon_svg("chart-line")):

        @render_plotly
        def for_sale_plot():
            for_sale_grouped = for_sale_inventory_df.groupby("StateName").sum(
                numeric_only=True
            )
            date_columns = for_sale_inventory_df.columns[6:]
            for_sale_grouped_dates = for_sale_grouped[date_columns].reset_index()
            for_sale_df_for_viz = for_sale_grouped_dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )

            for_sale_df_for_viz = filter_by_date(
                for_sale_df_for_viz, input.date_range()
            )

            if input.state() == "United States":
                df = for_sale_df_for_viz[for_sale_df_for_viz["StateName"] != ""]
            else:
                df = for_sale_df_for_viz[
                    for_sale_df_for_viz["StateName"] == input.state()
                ]

            fig = px.line(
                df,
                x="Date",
                y="Value",
                color="StateName",
            )
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
            return fig

    with ui.nav_panel("Table", icon=icon_svg("table")):

        @render.data_frame
        def for_sale_data():
            if input.state() == "United States":
                df = for_sale_inventory_df[for_sale_inventory_df["StateName"] != ""]
            else:
                df = for_sale_inventory_df[
                    for_sale_inventory_df["StateName"] == input.state()
                ]
            return render.DataGrid(df)


with ui.navset_card_underline(title="listings price"):
    with ui.nav_panel("Plot", icon=icon_svg("chart-line")):

        @render_plotly
        def listings_plot():
            listings_grouped = new_listings_df.groupby("StateName").sum(
                numeric_only=True
            )
            date_columns = new_listings_df.columns[6:]
            listings_grouped_dates = listings_grouped[date_columns].reset_index()
            listings_df_for_viz = listings_grouped_dates.melt(
                id_vars=["StateName"], var_name="Date", value_name="Value"
            )

            listings_df_for_viz = filter_by_date(
                listings_df_for_viz, input.date_range()
            )

            if input.state() == "United States":
                df = listings_df_for_viz[listings_df_for_viz["StateName"] != ""]
            else:
                df = listings_df_for_viz[
                    listings_df_for_viz["StateName"] == input.state()
                ]

            fig = px.line(
                df,
                x="Date",
                y="Value",
                color="StateName",
            )
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
            return fig

    with ui.nav_panel("Table", icon=icon_svg("table")):

        @render.data_frame
        def listings_data():
            if input.state() == "United States":
                df = new_listings_df[new_listings_df["StateName"] != ""]
            else:
                df = new_listings_df[new_listings_df["StateName"] == input.state()]
            return render.DataGrid(df)
