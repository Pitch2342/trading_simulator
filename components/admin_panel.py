import streamlit as st
import os
from datetime import datetime
from components.price_chart import render_full_price_preview
from components.csv_uploader import render_csv_uploader, download_sample_csv
from utils.portfolio_manager import reset_all_portfolios, update_player_portfolios
from utils.portfolio_manager import initialize_portfolios
from utils.session_manager import reset_simulation_state
from utils.visual_configs import CURRENCY_INDICATOR

def handle_data_source_selection():
    """Handle data source selection between predefined tickers and uploaded CSV"""
    st.markdown("### Data Source")
    
    data_source = st.radio(
        "Choose data source",
        options=['predefined', 'uploaded'],
        format_func=lambda x: "Predefined Tickers" if x == 'predefined' else "Upload Custom CSV",
        index=0 if st.session_state.data_source == 'predefined' else 1,
        horizontal=True
    )
    
    if data_source != st.session_state.data_source:
        st.session_state.data_source = data_source
        reset_simulation_state()
        st.rerun()
    
    if data_source == 'predefined':
        handle_ticker_selection()
    else:
        handle_csv_upload()

def handle_ticker_selection():
    """Handle ticker selection and reset simulation state accordingly"""
    available_tickers = [f.replace(".csv", "") for f in os.listdir('data') if f.endswith('.csv')]
    selected_ticker = st.selectbox(
        "Select Ticker",
        options=available_tickers,
        index=available_tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in available_tickers else 0,
        help="Choose which stock ticker to simulate"
    )
    
    if selected_ticker != st.session_state.selected_ticker:
        st.session_state.selected_ticker = selected_ticker
        st.session_state.current_day_index = 0
        st.session_state.portfolios = initialize_portfolios(st.session_state.num_players, st.session_state.starting_cash)
        st.session_state.uploaded_data = None  # Clear uploaded data when switching to predefined
        reset_simulation_state()
        st.rerun()

def handle_csv_upload():
    """Handle CSV file upload and validation"""
    # Show download sample button first
    download_sample_csv()
    
    # Render CSV uploader
    uploaded_df = render_csv_uploader()
    
    if uploaded_df is not None:
        # Store the uploaded data in session state
        if st.session_state.uploaded_data is None or not uploaded_df.equals(st.session_state.uploaded_data):
            st.session_state.uploaded_data = uploaded_df
            st.session_state.current_day_index = 0
            st.session_state.portfolios = initialize_portfolios(st.session_state.num_players, st.session_state.starting_cash)
            reset_simulation_state()
            st.success("📊 Custom data loaded successfully! You can now start the simulation.")
            st.rerun()

def render_admin_panel(df, breakpoints, force_expanded=False):
    """Render the admin settings panel"""
    with st.expander("⚙️ Admin Settings", expanded=force_expanded):
        st.markdown("### Simulation Configuration")
        
        # Add data source selection at the top
        data_source_col1, data_source_col2 = st.columns([1, 2])
        with data_source_col1:
            handle_data_source_selection()
        
        # Only show the rest of the admin panel if we have valid data or if we're in upload mode
        if df is not None or st.session_state.data_source == 'uploaded':
            admin_col1, admin_col2 = st.columns(2)
            
            with admin_col1:
                # Starting cash setting
                new_starting_cash = st.number_input(
                    "Starting Cash ({CURRENCY_INDICATOR})",
                    min_value=1000,
                    max_value=1000000,
                    value=st.session_state.starting_cash,
                    step=1000,
                    help="Set the starting cash amount for all players"
                )
                
                if new_starting_cash != st.session_state.starting_cash:
                    st.session_state.starting_cash = new_starting_cash
                    
                if st.button("Apply Starting Cash", help="Apply new starting cash to all players (resets portfolios)"):
                    reset_all_portfolios()
                    st.success(f"All portfolios reset with {CURRENCY_INDICATOR}{st.session_state.starting_cash:,.2f} starting cash")
                    st.rerun()
            
            with admin_col2:
                # Number of players setting
                new_num_players = st.number_input(
                    "Number of Players",
                    min_value=1,
                    max_value=4,
                    value=st.session_state.num_players,
                    step=1,
                    help="Set the number of players in the simulation"
                )
                
                if new_num_players != st.session_state.num_players:
                    st.session_state.num_players = new_num_players
                    new_portfolios, new_player_names = update_player_portfolios(new_num_players)
                    st.session_state.portfolios = new_portfolios
                    st.session_state.player_names = new_player_names
                    st.success(f"Number of players set to {st.session_state.num_players}")
                    st.rerun()

            # Player Names Configuration
            st.markdown("---")
            st.markdown("### Player Names")
            player_cols = st.columns(st.session_state.num_players)
            
            for player_num in range(1, st.session_state.num_players + 1):
                with player_cols[player_num - 1]:
                    new_player_name = st.text_input(
                        f"Player {player_num} Name",
                        value=st.session_state.player_names[player_num],
                        key=f"admin_player_name_{player_num}",
                        help=f"Set custom name for Player {player_num}"
                    )
                    if new_player_name != st.session_state.player_names[player_num]:
                        st.session_state.player_names[player_num] = new_player_name
                        st.rerun()
            
            # UI Settings Configuration
            st.markdown("---")
            st.markdown("### UI Settings")
            ui_col1, ui_col2 = st.columns(2)
            
            with ui_col1:
                new_font_size = st.number_input(
                    "Chart Hover Font Size",
                    min_value=8,
                    max_value=24,
                    value=st.session_state.chart_hoverlabel_font_size,
                    step=1,
                    help="Set the font size for chart hover labels (applies to all charts)"
                )
                
                if new_font_size != st.session_state.chart_hoverlabel_font_size:
                    st.session_state.chart_hoverlabel_font_size = new_font_size
                    st.success(f"Chart hover font size set to {new_font_size}px")
                    st.rerun()
            
            with ui_col2:
                # Time to run setting
                new_time_to_run = st.number_input(
                    "Simulation Duration (seconds)",
                    min_value=1,
                    max_value=300,
                    value=st.session_state.time_to_run_sec,
                    step=1,
                    help="Total time for the simulation to run from start to finish"
                )
                
                if new_time_to_run != st.session_state.time_to_run_sec:
                    st.session_state.time_to_run_sec = new_time_to_run
                    st.success(f"Simulation duration set to {st.session_state.time_to_run_sec} seconds")

            # Quick Actions
            st.markdown("---")
            st.markdown("### Quick Actions")
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("🔄 Reset Simulation", help="Reset simulation to beginning with current settings"):
                    st.session_state.current_day_index = 0
                    st.session_state.auto_progress = False
                    st.session_state.waiting_for_trade = False
                    st.session_state.trade_made = False
                    reset_all_portfolios()
                    st.success("Simulation reset to beginning")
                    st.rerun()
            
            with action_col2:
                if st.button("👥 Reset Player Names", help="Reset all player names to default"):
                    for i in range(1, st.session_state.num_players + 1):
                        st.session_state.player_names[i] = f"Player {i}"
                    st.success("Player names reset to default")
                    st.rerun()

            # Add price chart preview section with toggle (only if we have data)
            if df is not None:
                st.markdown("---")
                preview_col1, preview_col2 = st.columns([3, 1])
                
                with preview_col1:
                    st.markdown("### Price Chart Preview")
                    if st.session_state.data_source == 'uploaded':
                        data_source_info = "Custom uploaded data"
                    else:
                        data_source_info = f"Ticker: {st.session_state.selected_ticker}"
                    st.markdown(f"**{data_source_info}** • **{len(breakpoints)} decision points** identified")
                
                with preview_col2:
                    show_preview = st.toggle("Show Preview", value=False)
                
                # Render the full price chart preview only if toggle is enabled
                if show_preview:
                    preview_fig = render_full_price_preview(df, breakpoints)
                    st.plotly_chart(preview_fig, use_container_width=True)
            
            # Display current settings
            st.markdown("---")
            st.markdown("### Current Settings")
            settings_col1, settings_col2, settings_col3, settings_col4 = st.columns(4)
            with settings_col1:
                st.metric("Starting Cash", f"{CURRENCY_INDICATOR}{st.session_state.starting_cash:,.2f}")
            with settings_col2:
                st.metric("Simulation Duration", f"{st.session_state.time_to_run_sec}s")
            with settings_col3:
                st.metric("Players", st.session_state.num_players)
            with settings_col4:
                data_source_label = "Custom CSV" if st.session_state.data_source == 'uploaded' else "Predefined"
                st.metric("Data Source", data_source_label)
            
            # Download Summary Image
            st.markdown("---")
            st.markdown("### Export & Download")
            
            if st.button("📊 Generate Portfolio Summary Image", 
                        help="Generate and download a comprehensive image with portfolio stats and performance charts"):
                try:
                    from utils.visualization import create_portfolio_summary_image
                    import base64
                    
                    # Create the summary image
                    image_base64 = create_portfolio_summary_image(
                        df, 
                        st.session_state.current_day_index,
                        st.session_state.portfolios,
                        st.session_state.player_names,
                        st.session_state.num_players
                    )
                    
                    # Generate timestamp for filename
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                    
                    # Create download button with new naming scheme
                    st.download_button(
                        label="💾 Download Image",
                        data=base64.b64decode(image_base64),
                        file_name=f"trading_sim_{timestamp}_{st.session_state.num_players}.png",
                        mime="image/png",
                        help="Click to download the portfolio summary image"
                    )
                    
                    st.success("✅ Summary image generated successfully! Click the download button above to save it.")
                    
                except Exception as e:
                    st.error(f"❌ Error generating summary image: {str(e)}")
                    st.exception(e) 