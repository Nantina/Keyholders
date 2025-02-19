import streamlit as st 
import requests
import pandas as pd
import httpx
import asyncio
import plotly.graph_objects as go
import json
# import analyze_my_sentiment as an


async def call_api(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def fetch_data():
    url1 = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    url2 = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    CMC_API_KEY = '0200541f-023d-4600-8a00-54faa54de95b'

    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        # Run both requests in parallel
        btc_task = client.get(url2, headers=headers, params={"symbol": "BTC"})
        fg_task = client.get(url1,headers=headers)

        btc_response, fg_response = await asyncio.gather(btc_task, fg_task)

        # Extract Bitcoin Price
        btc_price = btc_response.json()["data"]["BTC"]["quote"]
        # Extract Fear & Greed Index
        fg_index = fg_response.json()["data"]

        # Use pandas for a better format
        df_fg = pd.DataFrame(fg_index)
        df_fg['timestamp'] = pd.to_datetime(df_fg['timestamp'],unit='s')

        # print(f"Bitcoin Price: ${btc_price}")
        # print(f"Fear & Greed Index: {fg_index}")

        # print(df_fg)

        return df_fg

st.sidebar.title("Navigation")


page  = st.sidebar.radio("Go to",["Dashboard", "Market Analysis", "Analytics","Trading Journal"])



if page == "Dashboard":
    st.title("Trading Sentiment Analysis")
    
    # my_feel = asyncio.run(call_api("http://fastapi:8000/me"))
    # market_feel = asyncio.run(call_api("http://fastapi:8000/market"))
    # insight = asyncio.run(call_api("http://fastapi:8000/me_market"))
    # Ensure API Call Happens Only Once
    if "my_feel" not in st.session_state:
        st.session_state.my_feel = asyncio.run(call_api("http://fastapi:8000/me"))
    if "market_feel" not in st.session_state:
        st.session_state.market_feel = asyncio.run(call_api("http://fastapi:8000/market"))
    if "insight" not in st.session_state:
        st.session_state.insight = asyncio.run(call_api("http://fastapi:8000/me_market"))
    # dummy 
    # my_feel = "yey"
    # market_feel = "nay"
    # insight = "let's go"

    st.write("**Market right now:**",f"{st.session_state.market_feel}")
    # if st.button("Submit Trade"):
    #     with st.spinner("Getting to know you..."):
    #         response = asyncio.run(call_api("http://fastapi:8000/me"))
            
    #     st.success(f"Your thoughts : {response}")
    #     st.write(f"I know you feel {response}")

    st.write("**Your past trades:**",f"{st.session_state.my_feel}")


    st.write("**Advice**:" , f"{st.session_state.insight}")
    
    with st.expander("Adjust trade:"):
        trade_objective = st.selectbox("Asset to trade",["Bitcoin","Coming soon..."],help="Right now all insights are for Bitcoin")
        trade_type = st.selectbox("Trade Type", ["buy","sell"])
        sentiment = st.slider("Sentiment Score", -1.0, 1.0, 0.0,help="Explain how confident you are for next trade")
        risk = st.slider("Risk", -1.0, 1.0, 0.0,help="Risk factor you want to take")
        investment = st.number_input("Investment amount")
        comment = st.text_area("Thoughts for trade")
    
        if st.button("Ask AI"):
            # Fetch sentiment data from FastAPI
            # response = requests.get("http://fastapi:8000/sentiments")
            data = {
                
                "trade_type": trade_type,
                "price": investment,
                "risk": risk,
                
                "thoughts": comment,
                
                    }
            st.json(data)

            # response = requests.post("http://fastapi:8000/ask", json=json.dumps(data))
            # That should be the answer of gpt-4o-mini
            st.write(200)
            st.success("This is nicely crafted, interesting way to capitalize on current events! Don't forget to put alerts about sudden market changes.")

elif page == "Analytics":
    st.title("Trade Analytics")
    st.write("Analyze trader performance")

    profit_loss_value = 72  # Example value

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=profit_loss_value,
        title={"text": "Total Profit/Loss ($)"},
        gauge={"axis": {"range": [-500, 500]}, "bar": {"color": "green" if profit_loss_value >= 0 else "red"}}
    ))

    st.plotly_chart(fig)

    df = asyncio.run(fetch_data())
    st.write("**Personal emotional sentiment based on last trades:**")
    # Create Plotly Figure
    fig1 = go.Figure()


    # Add Fear & Greed Index Line (Color Coded)
    fig1.add_trace(go.Scatter(
        x=df['timestamp'], y=df["value"], mode="lines", 
        name="Fear & Greed Index", 
        line=dict(color="green"),  # Adjust based on sentiment
    ))

    # Add Background Coloring (Extreme Greed & Fear)
    fig1.add_shape(type="rect", x0=df['timestamp'].min(), x1=df['timestamp'].max(),
                y0=df["value"].max() * 0.8, y1=df["value"].max(),
                fillcolor="lightgreen", opacity=0.3, line_width=0)
    fig1.add_shape(type="rect", x0=df['timestamp'].min(), x1=df['timestamp'].max(),
                y0=df["value"].max() * 0.2, y1=df["value"].max() * 0.4,
                fillcolor="lightcoral", opacity=0.3, line_width=0)

    # Add Title & Axis Labels
    fig1.update_layout(
        title="📉 My Fear & Greed Index Over Time",
        xaxis_title="Date",
        yaxis_title="Fear & Greed Index",
        template="plotly_white"
    )
    # Display Plot in Streamlit
    st.plotly_chart(fig1,help="This is the actual fear and greed index, but we can pretend that is the trader's")



elif page == "Market Analysis":
    st.title("Market sentiment analysis")
    left_column, right_column = st.columns(2)

    if left_column.button("What is market's sentiment?"):
        st.success("Our powerfull AI will now search the web in order to get market sentiment about Bitcoin")
        st.write("Right now these are mock tweets made with gpt-4o-mini")
        # get ai analysis
        response = requests.get("http://fastapi:8000/fear_greed")
        if response.status_code == 200:
            data = response.json()
            st.write(data)

    if right_column.button("Want to follow with a trade?"): # put it inside the previous if
        st.success("You can go back to dashboard for AI assistance ")


elif page == "Trading Journal":
    st.title("My trading journal")
    st.write("Explore your past entries or create a new")

    st.write("History of trades")
    response = requests.get("http://fastapi:8000/history")
    if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)

                # Format columns (if needed)
                df["datetime"] = pd.to_datetime(df["datetime"])  # Convert to readable date-time
                df = df.sort_values(by="datetime", ascending=False)  # Sort by latest trade first

                # print(df)

                # Trade type filter
                trade_types = ["All"] + list(df["trade_type"].unique())
                selected_type = st.selectbox("Filter by trade type:", trade_types)

                # Apply filter
                if selected_type != "All":
                    df = df[df["trade_type"] == selected_type]


                # Function to color profit/loss
                def color_profit_loss(value):
                    if value > 0:
                        return f"🟢 **+{value:.2f} USD**"
                    elif value < 0:
                        return f"🔴 **{value:.2f} USD**"
                    return "⚪ **0.00 USD**"

                df["profit_loss_display"] = df["profit_loss"].apply(color_profit_loss)

                # Show the improved table
                st.dataframe(df[["datetime", "trade_type", "price", "amount", "total_cost_or_revenue", "profit_loss_display", "thoughts"]], use_container_width=True)

            else: 
                st.warning("Empty db")
    
    # st.dataframe(df,use_container_width=True)
    left_column, right_column = st.columns(2)

    # button for submitting a new entry
    if left_column.button("Submit",help="Under construction"):


        st.success("Entry submitted!")

    # if right_column.button("History"):

    #     st.success("Past trades")

    if right_column.button("Populate with mock data",help="For demo purposes,might fail"):
        response = requests.get("http://fastapi:8000/submit-mock")
        if response.status_code == 200:
            
            st.write("This endpoint is dependant on gpt-4o-mini and sometimes fails")
            st.warning("Mock data failed...")

    if st.button("Analyze",help="Let the ai agent summarize your past intuition"):
        
        response = requests.get("http://fastapi:8000/my_analysis")
        if response.status_code == 200:
            data = response.json()
            st.write(data)
        