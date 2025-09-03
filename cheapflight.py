import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class FlightFinder:
    def __init__(self):
        # Sample flight data
        self.flights_data = [
            {"id": 1, "from": "New York (NYC)", "to": "Los Angeles (LAX)", "price": 299, "duration": "5h 30m", "airline": "SkyLine", "departure": "08:00", "arrival": "13:30", "stops": 0},
            {"id": 2, "from": "New York (NYC)", "to": "Los Angeles (LAX)", "price": 189, "duration": "7h 15m", "airline": "BudgetAir", "departure": "14:20", "arrival": "21:35", "stops": 1},
            {"id": 3, "from": "New York (NYC)", "to": "Chicago (CHI)", "price": 156, "duration": "2h 45m", "airline": "QuickFly", "departure": "09:15", "arrival": "12:00", "stops": 0},
            {"id": 4, "from": "New York (NYC)", "to": "Miami (MIA)", "price": 178, "duration": "3h 10m", "airline": "SunWings", "departure": "11:30", "arrival": "14:40", "stops": 0},
            {"id": 5, "from": "Los Angeles (LAX)", "to": "Chicago (CHI)", "price": 245, "duration": "4h 20m", "airline": "MidAir", "departure": "16:45", "arrival": "21:05", "stops": 0},
            {"id": 6, "from": "Los Angeles (LAX)", "to": "Miami (MIA)", "price": 267, "duration": "4h 55m", "airline": "CoastLine", "departure": "07:20", "arrival": "12:15", "stops": 0},
            {"id": 7, "from": "Chicago (CHI)", "to": "Miami (MIA)", "price": 198, "duration": "3h 25m", "airline": "WindyCity", "departure": "13:40", "arrival": "17:05", "stops": 0},
            {"id": 8, "from": "Los Angeles (LAX)", "to": "New York (NYC)", "price": 312, "duration": "5h 45m", "airline": "EastBound", "departure": "06:30", "arrival": "12:15", "stops": 0},
            {"id": 9, "from": "Chicago (CHI)", "to": "New York (NYC)", "price": 169, "duration": "2h 50m", "airline": "MetroJet", "departure": "18:20", "arrival": "21:10", "stops": 0},
            {"id": 10, "from": "Miami (MIA)", "to": "Chicago (CHI)", "price": 203, "duration": "3h 30m", "airline": "NorthStar", "departure": "10:15", "arrival": "13:45", "stops": 0},
            {"id": 11, "from": "New York (NYC)", "to": "Los Angeles (LAX)", "price": 225, "duration": "6h 40m", "airline": "ValueFly", "departure": "22:10", "arrival": "04:50", "stops": 1},
            {"id": 12, "from": "Miami (MIA)", "to": "Los Angeles (LAX)", "price": 289, "duration": "5h 20m", "airline": "WestCoast", "departure": "15:30", "arrival": "20:50", "stops": 0}
        ]
        
        self.df = pd.DataFrame(self.flights_data)
        
    def get_unique_cities(self):
        """Get all unique cities from the flight data"""
        from_cities = set(self.df['from'].tolist())
        to_cities = set(self.df['to'].tolist())
        all_cities = sorted(list(from_cities.union(to_cities)))
        return all_cities
    
    def find_flights(self, from_city, to_city):
        """Find all flights from one city to another, sorted by price"""
        filtered_flights = self.df[
            (self.df['from'] == from_city) & (self.df['to'] == to_city)
        ].sort_values('price')
        
        return filtered_flights
    
    def find_cheapest_flight(self, from_city, to_city):
        """Find the cheapest flight between two cities"""
        flights = self.find_flights(from_city, to_city)
        if not flights.empty:
            return flights.iloc[0]
        return None
    
    def create_price_chart(self, flights, from_city, to_city):
        """Create a bar chart showing flight prices"""
        if flights.empty:
            return None
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create color map - cheapest flight gets different color
        colors = ['#10B981' if i == 0 else '#3B82F6' for i in range(len(flights))]
        
        bars = ax.bar(range(len(flights)), flights['price'], color=colors, alpha=0.8)
        
        # Add price labels on bars
        for i, (bar, price) in enumerate(zip(bars, flights['price'])):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                   f'${price}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(f'Flight Prices: {from_city} → {to_city}', fontsize=16, fontweight='bold')
        ax.set_xlabel('Airlines', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        
        # Set x-axis labels to airline names
        ax.set_xticks(range(len(flights)))
        ax.set_xticklabels(flights['airline'], rotation=45)
        
        # Add grid for better readability
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig

# Initialize the flight finder
@st.cache_data
def get_flight_finder():
    return FlightFinder()

def main():
    st.set_page_config(
        page_title="✈️ Flight Finder",
        page_icon="✈️",
        layout="wide"
    )
    
    st.title("✈️ Cheapest Flight Finder")
    st.markdown("Find the best deals on flights between major cities!")
    
    finder = get_flight_finder()
    cities = finder.get_unique_cities()
    
    # Create tabs
    tab1, tab2 = st.tabs(["🔍 Flight Search", "📊 Analytics"])
    
    with tab1:
        st.header("Search Flights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            from_city = st.selectbox(
                "🛫 Departure City:",
                cities,
                key="from_city"
            )
        
        with col2:
            # Filter out the departure city from destinations
            available_destinations = [city for city in cities if city != from_city]
            to_city = st.selectbox(
                "🛬 Destination City:",
                available_destinations,
                key="to_city"
            )
        
        if st.button("Search Flights", type="primary"):
            flights = finder.find_flights(from_city, to_city)
            cheapest = finder.find_cheapest_flight(from_city, to_city)
            
            if cheapest is not None:
                # Display cheapest flight in a highlighted box
                st.success("🎯 **CHEAPEST FLIGHT FOUND!**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("✈️ Airline", cheapest['airline'])
                    st.metric("💰 Price", f"${cheapest['price']}")
                
                with col2:
                    st.metric("⏰ Duration", cheapest['duration'])
                    stops_text = "Direct" if cheapest['stops'] == 0 else f"{cheapest['stops']} stop(s)"
                    st.metric("🔄 Stops", stops_text)
                
                with col3:
                    st.metric("🕐 Departure", cheapest['departure'])
                    st.metric("🕐 Arrival", cheapest['arrival'])
                
                st.divider()
                
                # Display all flights
                st.subheader(f"📋 All Flights ({len(flights)} found)")
                
                # Prepare data for display
                display_flights = flights.copy()
                display_flights['stops_text'] = display_flights['stops'].apply(
                    lambda x: "Direct" if x == 0 else f"{x} stop(s)"
                )
                display_flights['rank'] = range(1, len(display_flights) + 1)
                
                # Reorder columns for display
                display_cols = ['rank', 'airline', 'price', 'duration', 'departure', 'arrival', 'stops_text']
                display_flights = display_flights[display_cols]
                display_flights.columns = ['Rank', 'Airline', 'Price ($)', 'Duration', 'Departure', 'Arrival', 'Stops']
                
                st.dataframe(
                    display_flights,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Price visualization
                st.subheader("📊 Price Comparison")
                fig = finder.create_price_chart(flights, from_city, to_city)
                if fig:
                    st.pyplot(fig)
                
            else:
                st.error(f"❌ Sorry, no flights found from {from_city} to {to_city}")
    
    with tab2:
        st.header("📊 Flight Route Analytics")
        
        df = finder.df
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Cheapest Flight", f"${df['price'].min()}")
        with col2:
            st.metric("💸 Most Expensive", f"${df['price'].max()}")
        with col3:
            st.metric("📊 Average Price", f"${df['price'].mean():.2f}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✈️ Airlines")
            airline_stats = df.groupby('airline').agg({
                'price': ['count', 'mean']
            }).round(2)
            airline_stats.columns = ['Flights', 'Avg Price ($)']
            st.dataframe(airline_stats)
        
        with col2:
            st.subheader("🛣️ Popular Routes")
            routes = df.groupby(['from', 'to']).agg({
                'price': ['count', 'min']
            }).round(2)
            routes.columns = ['Flights', 'Cheapest ($)']
            routes = routes.sort_values('Flights', ascending=False)
            st.dataframe(routes)

if __name__ == "__main__":
    main()
