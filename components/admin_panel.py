import streamlit as st
from components.price_chart import render_full_price_preview
from utils.portfolio_manager import reset_all_portfolios, update_player_portfolios

def render_admin_panel(df, breakpoints):
    """Render the admin settings panel"""
    with st.expander("⚙️ Admin Settings", expanded=False):
        st.markdown("### Simulation Configuration")
        
        admin_col1, admin_col2, admin_col3 = st.columns(3)
        
        with admin_col1:
            # Starting cash setting
            new_starting_cash = st.number_input(
                "Starting Cash ($)",
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
                st.success(f"All portfolios reset with ${st.session_state.starting_cash:,.2f} starting cash")
                st.rerun()
        
        with admin_col2:
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
        
        with admin_col3:
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

        # Add price chart preview section with toggle
        st.markdown("---")
        preview_col1, preview_col2 = st.columns([3, 1])
        
        with preview_col1:
            st.markdown("### Price Chart Preview")
            st.markdown(f"**{len(breakpoints)} decision points** identified in the data")
        
        with preview_col2:
            show_preview = st.toggle("Show Preview", value=False)
        
        # Render the full price chart preview only if toggle is enabled
        if show_preview:
            preview_fig = render_full_price_preview(df, breakpoints)
            st.plotly_chart(preview_fig, use_container_width=True)
        
        # Display current settings
        st.markdown("---")
        st.markdown("### Current Settings")
        settings_col1, settings_col2, settings_col3 = st.columns(3)
        with settings_col1:
            st.metric("Starting Cash", f"${st.session_state.starting_cash:,.2f}")
        with settings_col2:
            st.metric("Simulation Duration", f"{st.session_state.time_to_run_sec}s")
        with settings_col3:
            st.metric("Players", st.session_state.num_players) 