import pandas as pd
from datetime import datetime
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
    
    def display_flight_details(self, flight):
        """Display detailed information about a flight"""
        print(f"\n{'='*60}")
        print(f"🎯 CHEAPEST FLIGHT FOUND!")
        print(f"{'='*60}")
        print(f"✈️  Airline: {flight['airline']}")
        print(f"🛫 Route: {flight['from']} → {flight['to']}")
        print(f"💰 Price: ${flight['price']}")
        print(f"⏰ Duration: {flight['duration']}")
        print(f"🕐 Departure: {flight['departure']}")
        print(f"🕐 Arrival: {flight['arrival']}")
        stops_text = "Direct" if flight['stops'] == 0 else f"{flight['stops']} stop(s)"
        print(f"🔄 Stops: {stops_text}")
        print(f"{'='*60}")
    
    def display_all_flights(self, flights):
        """Display all flights in a formatted table"""
        if flights.empty:
            print("\n❌ No flights found for this route.")
            return
            
        print(f"\n📋 ALL FLIGHTS ({len(flights)} found)")
        print("-" * 120)
        print(f"{'Rank':<4} {'Airline':<12} {'Price':<8} {'Duration':<10} {'Departure':<10} {'Arrival':<10} {'Stops':<8}")
        print("-" * 120)
        
        for idx, (_, flight) in enumerate(flights.iterrows(), 1):
            price_indicator = "🏆" if idx == 1 else "  "
            stops_text = "Direct" if flight['stops'] == 0 else f"{flight['stops']} stop"
            print(f"{price_indicator}{idx:<3} {flight['airline']:<12} ${flight['price']:<7} {flight['duration']:<10} {flight['departure']:<10} {flight['arrival']:<10} {stops_text:<8}")
    
    def create_price_visualization(self, flights, from_city, to_city):
        """Create a bar chart showing flight prices"""
        if flights.empty:
            return
            
        plt.figure(figsize=(12, 6))
        
        # Create color map - cheapest flight gets different color
        colors = ['#10B981' if i == 0 else '#3B82F6' for i in range(len(flights))]
        
        bars = plt.bar(range(len(flights)), flights['price'], color=colors, alpha=0.8)
        
        # Add price labels on bars
        for i, (bar, price) in enumerate(zip(bars, flights['price'])):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                    f'${price}', ha='center', va='bottom', fontweight='bold')
        
        plt.title(f'Flight Prices: {from_city} → {to_city}', fontsize=16, fontweight='bold')
        plt.xlabel('Airlines', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        
        # Set x-axis labels to airline names
        plt.xticks(range(len(flights)), flights['airline'], rotation=45)
        
        # Add grid for better readability
        plt.grid(axis='y', alpha=0.3)
        
        # Highlight cheapest flight
        cheapest_idx = flights['price'].idxmin()
        cheapest_pos = flights.index.get_loc(cheapest_idx)
        plt.annotate('CHEAPEST!', xy=(cheapest_pos, flights.iloc[0]['price']), 
                    xytext=(cheapest_pos, flights.iloc[0]['price'] + 50),
                    arrowprops=dict(arrowstyle='->', color='green', lw=2),
                    fontsize=12, fontweight='bold', color='green', ha='center')
        
        plt.tight_layout()
        plt.show()
    
    def run_interactive_search(self):
        """Run the interactive flight search interface"""
        print("\n" + "="*60)
        print("✈️  WELCOME TO CHEAPEST FLIGHT FINDER")
        print("="*60)
        
        cities = self.get_unique_cities()
        
        while True:
            print(f"\n📍 Available Cities:")
            for i, city in enumerate(cities, 1):
                print(f"  {i}. {city}")
            
            try:
                # Get departure city
                print(f"\n🛫 Select departure city (1-{len(cities)}) or 0 to exit:")
                from_choice = int(input("Enter number: "))
                
                if from_choice == 0:
                    print("👋 Thank you for using Flight Finder!")
                    break
                    
                if 1 <= from_choice <= len(cities):
                    from_city = cities[from_choice - 1]
                else:
                    print("❌ Invalid choice. Please try again.")
                    continue
                
                # Get destination city
                available_destinations = [city for city in cities if city != from_city]
                print(f"\n🛬 Available destinations from {from_city}:")
                for i, city in enumerate(available_destinations, 1):
                    print(f"  {i}. {city}")
                
                print(f"\nSelect destination city (1-{len(available_destinations)}):")
                to_choice = int(input("Enter number: "))
                
                if 1 <= to_choice <= len(available_destinations):
                    to_city = available_destinations[to_choice - 1]
                else:
                    print("❌ Invalid choice. Please try again.")
                    continue
                
                # Search for flights
                print(f"\n🔍 Searching flights from {from_city} to {to_city}...")
                
                all_flights = self.find_flights(from_city, to_city)
                cheapest = self.find_cheapest_flight(from_city, to_city)
                
                if cheapest is not None:
                    # Display cheapest flight
                    self.display_flight_details(cheapest)
                    
                    # Display all flights
                    self.display_all_flights(all_flights)
                    
                    # Ask if user wants to see visualization
                    show_viz = input("\n📊 Would you like to see a price comparison chart? (y/n): ")
                    if show_viz.lower() == 'y':
                        self.create_price_visualization(all_flights, from_city, to_city)
                else:
                    print(f"\n❌ Sorry, no flights found from {from_city} to {to_city}")
                
                # Ask if user wants to search again
                continue_search = input(f"\n🔄 Would you like to search for another route? (y/n): ")
                if continue_search.lower() != 'y':
                    print("👋 Thank you for using Flight Finder!")
                    break
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    def get_route_analytics(self):
        """Display analytics about all available routes"""
        print("\n" + "="*60)
        print("📊 FLIGHT ROUTE ANALYTICS")
        print("="*60)
        
        # Price statistics
        print(f"\n💰 Price Statistics:")
        print(f"   Cheapest flight: ${self.df['price'].min()}")
        print(f"   Most expensive: ${self.df['price'].max()}")
        print(f"   Average price: ${self.df['price'].mean():.2f}")
        
        # Airline statistics
        print(f"\n✈️  Airlines:")
        airline_counts = self.df['airline'].value_counts()
        for airline, count in airline_counts.items():
            avg_price = self.df[self.df['airline'] == airline]['price'].mean()
            print(f"   {airline}: {count} flights (avg: ${avg_price:.2f})")
        
        # Route statistics
        print(f"\n🛣️  Popular Routes:")
        routes = self.df.groupby(['from', 'to']).size().sort_values(ascending=False)
        for (from_city, to_city), count in routes.head().items():
            cheapest_price = self.df[(self.df['from'] == from_city) & 
                                   (self.df['to'] == to_city)]['price'].min()
            print(f"   {from_city} → {to_city}: {count} flights (cheapest: ${cheapest_price})")


def main():
    """Main function to run the flight finder application"""
    finder = FlightFinder()
    
    print("Choose an option:")
    print("1. Interactive Flight Search")
    print("2. View Route Analytics")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        finder.run_interactive_search()
    elif choice == '2':
        finder.get_route_analytics()
    elif choice == '3':
        print("👋 Goodbye!")
    else:
        print("Invalid choice. Please run the program again.")


if __name__ == "__main__":
    main()
